import os
import sys
import csv
import re
from pathlib import Path
from chimerax.core.commands import run

# Ensure correct number of arguments
if len(sys.argv) not in (2, 3):
    raise ValueError("Usage: runscript 'chimeraX_align_structures.py' <pdb_dir> [<highlight_file>]")

# Get the PDB directory
pdb_dir = Path(sys.argv[1])
if not pdb_dir.is_dir():
    raise ValueError(f"PDB directory not found: {pdb_dir}")

# Get all PDB files and sort them
pdb_files = sorted(list(pdb_dir.glob("*.pdb")))
if len(pdb_files) < 2:
    raise ValueError("There must be at least two PDB files in the directory.")

# Define log file path (temporary file)
log_file = pdb_dir / "chimeraX_log.html"

# List for storing RMSD results
alignment_results = []

# Open reference structure
first_pdb_path = str(pdb_files[0])
run(session, f'open "{first_pdb_path}"')

# Align each structure and extract log information
for i, pdb_file in enumerate(pdb_files[1:], start=2):
    run(session, f'open "{pdb_file}"')

    # Clear log before running matchmaker
    run(session, 'log clear')

    # Run matchmaker
    run(session, f'matchmaker #{i} to #1')

    # Save log to an HTML file
    run(session, f'log save "{log_file}"')

    # Read the saved HTML log file
    with open(log_file, 'r', encoding='utf-8') as f:
        log_output = f.read()

    # Parse alignment information using regex
    match_line = re.search(
        r"Matchmaker\s+(?P<ref>.+?)\s+with\s+(?P<aligned>.+?),\s+sequence alignment score\s*=\s*(?P<score>[\d\.]+)",
        log_output)

    rmsd_line = re.search(
        r"RMSD between\s+(?P<pruned_pairs>\d+)\s+pruned atom pairs is\s+(?P<pruned_rmsd>[\d\.]+)\s+angstroms;\s+\(across all\s+(?P<all_pairs>\d+)\s+pairs:\s+(?P<all_rmsd>[\d\.]+)\)",
        log_output)
    
    if not match_line or not rmsd_line:
        print(f"WARNING: Could not parse matchmaker output for {pdb_file}")
        continue

    ref_struct = match_line.group("ref")
    aligned_struct = match_line.group("aligned")
    score = match_line.group("score")
    pruned_pairs = rmsd_line.group("pruned_pairs")
    pruned_rmsd = rmsd_line.group("pruned_rmsd")
    all_pairs = rmsd_line.group("all_pairs")
    all_rmsd = rmsd_line.group("all_rmsd")

    # Store results
    alignment_results.append([ref_struct, aligned_struct, score, all_pairs, all_rmsd, pruned_pairs, pruned_rmsd])

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
# Remove last log line
log_file.unlink(missing_ok=True)

# Write results to a TSV file
tsv_output = pdb_dir / "chimeraX_rmsd_results.tsv"
with open(tsv_output, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    writer.writerow(["reference_structure", "aligned_structure", "matchmaker_alignment_score", 
                     "atom_pairs", "rmsd_angstrom", "pruned_atom_pairs", "pruned_rmsd_angstrom"])
    writer.writerows(alignment_results)

print(f"Alignment results saved to: {tsv_output}")

# Create a new directory for aligned structures and save the aligned models.
aligned_dir = pdb_dir / "aligned"
aligned_dir.mkdir(exist_ok=True)

for i, pdb_file in enumerate(pdb_files, start=1):
    output_file = aligned_dir / f"aligned_{pdb_file.name}"
    run(session, f'save "{output_file}" #{i} format pdb')
    print(f"Saved: {output_file}")
