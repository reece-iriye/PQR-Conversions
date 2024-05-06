# **Converting Protein-Ligand Complex files to PQR Format**

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

The `form_complex_pqr.py` script combines individual protein PQR and ligand PQR files into a single complex PQR file. It searches for pairs of PQR files in a given directory, where one file ends with `_protein.pqr` and the other ends with `_ligand.pqr`, and combines them into a new file that ends with `_combined.pqr`.

### **Running the Script Manually**

To run the script manually for a specific directory, use the following command:

```bash
python form_complex_pqr.py --directory ./data/generated/<PDB_ID>
```

Replace `./data/generated/<PDB_ID>` with the relative or absolute path to the directory containing the protein and ligand PQR files you want to combine.

### **Running the Script with a Shell Script**

To automate the process of running the `form_complex_pqr.py` script on multiple subdirectories within a root directory, you can use the provided shell script `form_complex_pqr.sh`.

First, make sure the shell script is executable by running the following command:

```bash
chmod +x form_complex_pqr.sh
```

Then, run the shell script with the `--directory` argument specifying the root directory containing the subdirectories you want to process:

```bash
./form_complex_pqr.sh --directory ./data/generated
```

The shell script will iterate through each subdirectory at level 1 of the specified root directory and run the `form_complex_pqr.py` script with each subdirectory as the `--directory` argument.

This shell script is intended to be used after running the jobs for creating the separate protein `.pqr` files and ligand `.pqr` files in the exact same directory.
