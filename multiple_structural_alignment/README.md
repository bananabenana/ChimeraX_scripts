# Aligning multiple protein structures and optionally highlight key residues
This script allows you to perform a protein structural alignment in Chimera across as many structures as you want. Simply put them in a directory and run this tool.
![all_52_aligned](https://github.com/user-attachments/assets/d0202aec-7022-4f28-b4fd-6d911bb51324)

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
- (Optional) tab-delimited file with `Residue_position` and `colour` columns

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

## Outputs
- Each input `.pdb` file will be output as an aligned (reorientated) file inside an `aligned` directory
- `chimeraX_rmsd_results.tsv` which looks like this:

|reference_structure|aligned_structure|matchmaker_alignment_score|atom_pairs|rmsd_angstrom|pruned_atom_pairs|pruned_rmsd_angstrom|
|---|---|---|---|---|---|---|
|protein_1.pdb, chain A (#1)|protein_2.pdb, chain A (#2)|1193.1|228|0.342|227|0.307|
|protein_1.pdb, chain A (#1)|protein_3.pdb, chain A (#3)|1071.6|226|1.152|221|0.225|
|protein_1.pdb, chain A (#1)|protein_4.pdb, chain A (#4)|1064.8|226|1.387|220|0.353|


## Citation
Please cite: Vezina, B., Morampalli, B.R., Nguyen, HA. et al. The rise and global spread of IMP carbapenemases (1996-2023): a genomic epidemiology study. Nat Commun (2025). https://doi.org/10.1038/s41467-025-66874-7


## Authors

- Ben Vezina
  - ORCIRD: https://orcid.org/0000-0003-4224-2537
  - Google Scholar: https://scholar.google.com.au/citations?user=Rf9oh94AAAAJ&hl=en&oi=ao


## Dependancies

- ChimeraX
- Python
