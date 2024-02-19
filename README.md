# **Protein-Ligland-Binded-PQR-Generator**

Script for PQR file generation for protein-ligland bonding PDB-Bind+ data. Requires directory structure for data.

## **Set-Up**

Create a `conda` environment, activate the environment, and install all the required packages. The `pdb2pqr` package works in Python 3.8 - Python 3.11 as of 2/18/2024, so any version in this range is good to work with.

```{bash}
conda create -n <CONDA_ENV_NAME> python=3.8  # can choose from 3.8-3.11, I use 3.8 since it's very compatible with PyTorch
conda activate <CONDA_ENV_NAME>
pip install -r requirements.txt
```

After running the commands above, you should have access to the `pdb2pqr` command line arguments. Try running the following command to see if the arguments work:

```{bash}
pbq2pqr --help
```

## **Instructions**

To generate PQR file for a protein from the Protein Data Bank with a certain PDB ID, run the command below and make sure to specify the `<PDB_ID>` and `<FILENAME>`, and if needed, use a different forcefield:

```{bash}
pdb2pqr --ff=AMBER ./data/pdbbind/<PDB_ID>/<FILENAME>.pdb ./data/generated/<PDB_ID>/<FILENAME>.pqr
```

Also, instructions for `pdb2pqr` command line tools can be found [here](https://pdb2pqr.readthedocs.io/en/latest/using/index.html).

## **Examples**

### **10gs**

Let $P$ denote the set of all atom lines in the `protein.pqr` file.

Let $L$ denote the set of all atom lines in the `pocket-ligand.pqr` file.

Let $C$ denote the set of all atom lines in the `protein-ligand.pqr` file.

**Hypothesis test:** $P \cup L = C$


With the `10gs` protein, I ran the following commands:
```{bash}
# Run PDB2PQR on protein alone, ligand alone, then the complex
pdb2pqr --ff=AMBER ./data/pdbbind/10gs/protein.pdb ./data/generated/10gs/protein.pqr
pdb2pqr --ff=AMBER ./data/pdbbind/10gs/protein-ligand.pdb ./data/generated/10gs/protein-ligand.pqr
pdb2pqr --ff=AMBER ./data/pdbbind/10gs/pocket-ligand.pdb ./data/generated/10gs/pocket-ligand.pqr

# Run script that checks if the atoms in the alone protein and ligand PQR files are strictly subsets
# of the protein-ligand file.
python comparison.py ./data/generated/10gs/protein.pqr ./data/generated/10gs/pocket-ligand.pqr ./data/generated/10gs/protein-ligand.pqr
```

Running these commands yielded the following output:

```
OUTPUT:

./data/generated/10gs/protein.pqr contains 6534 atoms.
./data/generated/10gs/pocket-ligand.pqr contains 814 atoms.
./data/generated/10gs/protein-ligand.pqr contains 6534 atoms.

Protein-ligand file contains data exclusively from protein PQR file?: False
Number of lines different in these two files: 1068

Protein-ligand file contains data exclusively from ligand PQR file?: False
Number of lines different in these two files: 355

Are Subsets?: False
Are Exclusively from both?: False
Total not in subset:  1423
```

Our hypothesis is false. The `protein-ligand.pqr` file contains altered data but still contains some of the same atomic data when binding happens between the protein from `protein.pqr` and the ligand from `ligand.pqr`.
