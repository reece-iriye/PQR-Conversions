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

