# residue_structure_colour_scripts
Ever wanted to colour a 3D protein structure as a structure heatmap, programatically? Well now you can.

## Quick usage

The script takes the following basic arguments inside the ChimeraX command line:
```python
runscript "chimeraX_colour_residues.py" <column name containing hex values> <directory containing structures> <tab-delimited file containing desired values>
```

## Usage

### File requirements
- Desired 3D structure you want to colour residues for
- Input tab-delimited file with residue numbers and hex colours

The important columns are `Residue_position` and then columns containing hex values to colour each residue by. In this case, `lddt_colour` and `conservation_colour`, but they can be named anything. Example:

|Residue_position|lDDT_score|aa_conservation_score|aa_ident_conservation_score|lddt_colour|conservation_colour|
|---|---|---|---|---|---|
|1|0.817692|0.076093514|0.230769231|#007778|#FCEBA8|
|2|0.914752|0.449472097|0.653846154|#00686F|#F7B275|
|3|0.962377|0.430844646|0.596153846|#00616A|#F7B376|
|4|0.974145|1|1|#006069|#E24C80|
|..|..|..|..|..|..|
|228|0.866805|0.531900452|0.692307692|#007073|#F5A370|


### Steps
1. Open ChimeraX
2. Click Tools > make sure Command Line Interface (CLI) is ticked
3. Inside CLI, type the following:
```python
# Colour by lDDT score
runscript "chimeraX_colour_residues.py" "lddt_colour" "structures" "lddt_conservation_scores.tsv"

# Colour by conservation score
runscript "chimeraX_colour_residues.py" "conservation_colour" "structures" "lddt_conservation_scores.tsv"
```

## Author

- Ben Vezina
  - ORCIRD: https://orcid.org/0000-0003-4224-2537
  - Google Scholar: https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao


## Dependancies

- ChimeraX
- Python
