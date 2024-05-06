# **Converting Ligand files to PQR Format**

Instructions for PQR file generation for protein-ligland binding using data from [PDB-Bind+](https://www.pdbbind-plus.org.cn/data/search). Requires PDB files to be downloaded into a `data/pdbbind/<PDB_ID>` directory, where `<PDB_ID>` reflects the complex that is being analyzed. See how I organized the `10gs` directory.

## **Code Set-Up**

Create a `conda` environment, activate the environment, and install all the required packages. The `pdb2pqr` package works in Python 3.8 - Python 3.11 as of 2/18/2024, so any version in this range is good to work with.

```{bash}
conda create -n <CONDA_ENV_NAME> python=3.8  # can choose from 3.8-3.11, I use 3.8 since it's very compatible with PyTorch
conda activate <CONDA_ENV_NAME>
pip install -r requirements.txt
```

After running the commands above, you should have access to the `pdb2pqr` command line arguments, as well as `obabel` command line arguments, which are necessary for most the scripts in this repository. Try running the following command to see if the arguments work:

```{bash}
pbq2pqr --help
obabel --help
```

## **Instructions for Converting PDB to PQR**

To generate PQR file for a protein from the Protein Data Bank with a certain PDB ID, run the command below and make sure to specify the `<PDB_ID>` and `<FILENAME>`, and if needed, use a different forcefield:

```{bash}
pdb2pqr --ff=AMBER ./data/pdbbind/<PDB_ID>/<FILENAME>.pdb ./data/generated/<PDB_ID>/<FILENAME>.pqr
```

Also, instructions for `pdb2pqr` command line tools can be found [here](https://pdb2pqr.readthedocs.io/en/latest/using/index.html).

The format that this repository uses contains a bunch of stored `.pdb` files directly from the PDB-Bind+ website. You are more than welcome to save these instead to a custom directory.

Running the `pdb2pqr` command above generates our PQR files!

### **Examples**

With the `10gs` protein, I ran the following commands:
```{bash}
# Run PDB2PQR on protein alone, ligand alone, then the complex
pdb2pqr --ff=AMBER ./data/pdbbind/10gs/protein.pdb ./data/generated/10gs/protein.pqr
pdb2pqr --ff=AMBER ./data/pdbbind/10gs/pocket-ligand.pdb ./data/generated/10gs/pocket-ligand.pqr
```

The files are then saved to my file system.

## **Instructions for Converting SDF Files to PQR**

Ensure that Open Babel is properly configured and accessible from the command line.

### **Run the Script**

To run the script in the cloned repository, run this step:

```bash
python convert_sdf_to_pqr.py --input-dir <input_directory> \
                             --output-dir <output_directory> \
                             --FF <forcefield>
```
- `<input_directory>` should be the directory containing the SDF files you want to process. If not specified, it defaults to `data/pdbbind`.
- `<output_directory>` is the directory where the generated PQR files will be saved. If not specified, it defaults to `data/generated`.
- `<forcefield>` is the forcefield used for calculating charges for the PQR files. It defaults to `AMBER`.


### Example

Here's an example command to run the script:

```bash
python convert_sdf_to_pqr.py --input-dir data/pdbbind --output-dir data/output
```

## **Instructions for Creating Protein-Ligand Complex PQR Files from Individual Protein PQR and Ligand PQR Files**



