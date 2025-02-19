# Aligning multiple protein structures and optionally highlight key residues
This script allows you to perform a protein structural alignment in Chimera across as many structures as you want. Simply put them in a directory and run this tool.

## Quick usage

The script takes the following basic arguments inside the ChimeraX command line:
```python
# Align all structures
runscript "chimeraX_align_structures.py" <directory containing structures>

# Align all structures and highlight key residues
runscript "chimeraX_align_structures.py" <directory containing structures> <tab-delimited file containing residues to highlight>
```

## Usage

### File requirements
- Desired 3D structures you want to align, within a single directory
- Optional tab-delimited file with `Residue_position` and `colour` columns

Example tab-delimited file:
|Residue_position|colour|
|---|---|
|30|#DB9D85|
|31|#DB9D85|
|87|#DB9D85|
|150|#DB9D85|
|196|#DB9D85|



### Steps
1. Open ChimeraX
2. Click Tools > make sure Command Line Interface (CLI) is ticked
3. Inside CLI, type the following:
```python
# Align all structures inside a directory and save the output
runscript "chimeraX_align_structures.py" "structures"

# Align all structures inside a directory and save the output
runscript "chimeraX_align_structures.py" "structures" "highlight_residues.tsv"
```

## Authors

- Ben Vezina
  - ORCIRD: https://orcid.org/0000-0003-4224-2537
  - Google Scholar: https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao


## Dependancies

- ChimeraX
- Python
