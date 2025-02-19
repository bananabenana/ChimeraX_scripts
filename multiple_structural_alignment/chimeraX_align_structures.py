import os
import sys
import csv
from pathlib import Path
from chimerax.core.commands import run

# Check for proper usage:
# sys.argv[0] is the script name, so we need either 2 or 3 total arguments.
if len(sys.argv) not in (2, 3):
    raise ValueError("Usage: runscript 'chimeraX_align_structures.py' <pdb_dir> [<highlight_file>]")

# Get the PDB directory from the first argument
pdb_dir = Path(sys.argv[1])
if not pdb_dir.is_dir():
    raise ValueError(f"PDB directory not found: {pdb_dir}")

# Find all pdb files in the directory and ensure there are at least two.
pdb_files = sorted(list(pdb_dir.glob("*.pdb")))
if len(pdb_files) < 2:
    raise ValueError("There must be at least two PDB files in the directory.")

# Open the first PDB file
first_pdb_path = str(pdb_files[0])
run(session, f'open "{first_pdb_path}"')

# Open and align the remaining PDB files
for i, pdb_file in enumerate(pdb_files[1:], start=2):
    run(session, f'open "{pdb_file}"')
    run(session, f'matchmaker #{i} to #1')

# Add chain outline
print("Adding chain outline")
run(session, 'graphics silhouettes true color black width 2 depthJump 0.005')

# Soften light
print("Softening light")
run(session, 'lighting soft')

# Color all ribbons white
print("Coloring residues white")
run(session, 'color #* #D3D3D3 target r')

# Optionally process the highlight TSV file if provided.
if len(sys.argv) == 3:
    highlight_file = Path(sys.argv[2])
    if not highlight_file.is_file():
        raise ValueError(f"Highlight file not found: {highlight_file}")
    
    print(f"Parsing highlight file: {highlight_file}")
    try:
        with highlight_file.open("r") as file:
            reader = csv.DictReader(file, delimiter="\t")
            # Expecting columns: Residue_position and colour
            for row in reader:
                residue_position = int(row["Residue_position"])
                colour = row["colour"]
                print(f"Highlighting residue {residue_position} with colour {colour}")
                # This will override the white coloring for these specific residues.
                run(session, f'color #*:{residue_position} {colour} target r')
    except Exception as e:
        print(f"Error processing highlight file: {e}")
        sys.exit(1)

# Create a new directory for aligned structures and save the aligned models.
aligned_dir = pdb_dir / "aligned"
aligned_dir.mkdir(exist_ok=True)

for i, pdb_file in enumerate(pdb_files, start=1):
    output_file = aligned_dir / f"aligned_{pdb_file.name}"
    run(session, f'save "{output_file}" #{i} format pdb')
    print(f"Saved: {output_file}")

print("All structures have been aligned and saved.")
