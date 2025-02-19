import os
import csv
import sys
from pathlib import Path
from chimerax.core.commands import run

# Check if the correct number of arguments is provided.
if len(sys.argv) != 4:
    raise ValueError("Usage: runscript 'chimeraX_lDDT_colour.py' <column_header> <pdb_directory> <lddt_file>")

# Get command-line arguments.
col_header = sys.argv[1]
pdb_dir = Path(sys.argv[2])
lddt_file = Path(sys.argv[3])

# Verify pdb_dir exists.
if not pdb_dir.is_dir():
    raise ValueError(f"PDB directory not found: {pdb_dir}")

# Verify lddt_file exists.
if not lddt_file.is_file():
    raise ValueError(f"lDDT file not found: {lddt_file}")

# Load the first PDB file from the specified directory.
pdb_files = [f for f in pdb_dir.iterdir() if f.suffix == ".pdb"]
if not pdb_files:
    raise ValueError("No PDB files found in the directory.")

first_pdb_path = pdb_files[0]
print(f"Opening PDB file: {first_pdb_path}")
run(session, f'open "{first_pdb_path.as_posix()}"')
print("PDB file opened successfully.")

# Add an outline to the structure.
run(session, 'graphics silhouettes true')

# Parse the lDDT file.
print(f"Parsing lDDT file: {lddt_file}")
residue_colors = {}
try:
    with lddt_file.open('r') as file:
        reader = csv.DictReader(file, delimiter='\t')
        for row in reader:
            residue_position = int(row['Residue_position'])
            if col_header not in row:
                raise KeyError(f"Column '{col_header}' not found in the TSV file.")
            lddt_color = row[col_header]
            residue_colors[residue_position] = lddt_color
    print(f"Parsed {len(residue_colors)} residues with colors.")
except Exception as e:
    print(f"Error parsing lDDT file: {e}")
    sys.exit(1)

# Color residues based on the specified column values.
print(f"Coloring residues based on '{col_header}' values...")
for residue_position, lddt_color in residue_colors.items():
    run(session, f'color #1:{residue_position} {lddt_color} target r')
print("Residue coloring complete.")

print("All steps completed.")
