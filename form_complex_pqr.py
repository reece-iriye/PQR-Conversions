import argparse
import os
from pathlib import Path
from typing import List, Tuple, Optional


def combine_pqr_files(ligand_file: str, protein_file: str, output_file: str) -> None:
    """
    Combine lines starting with "ATOM" or "HETATM" from ligand and protein PQR files.

    Parameters
    ----------
    ligand_file : str
        The path to the ligand PQR file.
    protein_file : str
        The path to the protein PQR file.
    output_file : str
        The path where the combined PQR file will be saved.
    """
    with open(ligand_file, "r") as ligand, open(protein_file, "r") as protein, open(output_file, "w") as output:
        for line in protein:
            if line.startswith(("ATOM", "HETATM")):
                output.write(line)
        for line in ligand:
            if line.startswith(("ATOM", "HETATM")):
                output.write(line)


def find_pqr_pair(directory: str) -> Tuple[str, str]:
    """
    Find protein-ligand pair of PQR files in the given directory.

    Parameters
    ----------
    directory : str
        The directory to search for PQR file pairs.

    Returns
    -------
    Tuple[str, str]
        A tuple
    """
    ligand_file: Optional[str] = None
    for file in os.listdir(directory):
        if file.endswith("_ligand.pqr"):
            ligand_file = os.path.join(directory, file)
            break
    if ligand_file is None:
        raise FileExistsError(f"No ligand PQR file exists in {directory}.")

    protein_file: Optional[str] = None
    for file in os.listdir(directory):
        if file.endswith("_protein.pqr"):
            protein_file = os.path.join(directory, file)
            break
    if protein_file is None:
        raise FileExistsError(f"No protein PQR file exists in {directory}.")

    return (protein_file, ligand_file)


def process_directory(root_dir: str) -> None:
    """
    Process PQR file pair in the given directory.

    Parameters
    ----------
    root_dir : str
        The root directory to start processing from.
    """
    relative_dir = root_dir.split("/")[-1]
    protein_file, ligand_file = find_pqr_pair(root_dir)
    output_file = os.path.join(root_dir, f"{relative_dir}_combined.pqr")
    combine_pqr_files(ligand_file, protein_file, output_file)
    print(f"Combined {ligand_file} and {protein_file} into {output_file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Combine ligand and protein PQR files.")
    parser.add_argument("directory",
        help="The directory containing the PQR files from the same protein to process.")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    process_directory(args.directory)
