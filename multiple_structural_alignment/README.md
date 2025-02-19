# Aligning multiple protein structures

## Quick usage

The script takes the following basic arguments inside the ChimeraX command line:
```python
runscript "chimeraX_align_structures.py" <directory containing structures>
```

## Usage

### File requirements
- Desired 3D structures you want to align, within a single directory

### Steps
1. Open ChimeraX
2. Click Tools > make sure Command Line Interface (CLI) is ticked
3. Inside CLI, type the following:
```python
# Align all structures inside a directory and save the output
runscript "chimeraX_align_structures.py" "structures"
```

## Authors

- Ben Vezina
  - ORCIRD: https://orcid.org/0000-0003-4224-2537
  - Google Scholar: https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao


## Dependancies

- ChimeraX
- Python
