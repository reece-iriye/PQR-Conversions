import polars as pl
import numpy as np

from argparse import ArgumentParser
from math import isclose
import sys
from typing import List, Dict, Any, Optional


def _parse_pqr_line(line: str) -> Dict[str, Any]:
    """
    Parse each individual line of the PQR schema.

    Args:
        line (str): Text-based string representing a line in the PQR file.
    Returns:
        Dict[str, Any]: Dictionary representation of a row.
    """
    parts = line.split()  # Splitting by whitespace
    return {
        'recordName': parts[0],
        'serial': int(parts[1]),
        'atomName': parts[2],
        'residueName': parts[3],
        'residueNumber': float(parts[4]),
        'X': float(parts[5]),
        'Y': float(parts[6]),
        'Z': float(parts[7]),
        'charge': float(parts[8]),
        'radius': float(parts[9]),
    }


def _parse_mol2_atom_line(line: str) -> Dict[str, Any]:
    """
    Parse each individual line of the ATOM section in the MOL2 file.

    Args:
        line (str): Text-based string representing a line in the MOL2 file.
    Returns:
        Dict[str, Any]: Dictionary representation of a row.
    """
    parts = line.split()
    return {
        "atom_id": int(parts[0]),
        "atom_name": parts[1],
        "x": float(parts[2]),
        "y": float(parts[3]),
        "z": float(parts[4]),
        "atom_type": parts[5],
        "subst_id": int(parts[6]) if len(parts) > 6 else None,
        "subst_name": parts[7] if len(parts) > 7 else None,
        "charge": float(parts[8]) if len(parts) > 8 else None,
        "status_bit": parts[9] if len(parts) > 9 else None,
    }


def convert_pqr_to_polars_dataframe(file_path: str) -> pl.DataFrame:
    """
    Represent PQR file in the form of a Polars DataFrame.

    Args:
        file_path (str): File path of PQR file.
    Returns:
        polars.DataFrame
    """
    parsed_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            # Stop iterating if we reach terminating point of PQR file
            if line.startswith("TER") or line.startswith("END") or not line:
                continue
            elif line.strip() and not line.startswith('#'):
                parsed_data = _parse_pqr_line(line)
                parsed_lines.append(parsed_data)

    return pl.DataFrame(parsed_lines)


def convert_mol2_to_polars_dataframe(file_path: str) -> pl.DataFrame:
    """
    Represent MOL2 file in the form of a Polars DataFrame.

    Args:
        file_path (str): File path of MOL2 file.
    Returns:
        polars.DataFrame
    """
    parsed_lines = []
    parsing_atoms = False

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()
            if line.startswith("@<TRIPOS>ATOM"):
                parsing_atoms = True
                continue
            elif line.startswith("@<TRIPOS>") and not line.startswith("@<TRIPOS>ATOM"):
                parsing_atoms = False
                continue

            if parsing_atoms and line:
                parsed_data = _parse_mol2_atom_line(line)
                parsed_lines.append(parsed_data)

    return pl.DataFrame(parsed_lines)


def create_atom_info_mapping(pqr_df: pl.DataFrame) -> Dict[str, float]:
    """
    Create a dictionary mapping from atom names to their radii.

    Args:
        pqr_df (polars.DataFrame): Polars DataFrame from a PQR file.

    Returns:
        dict: A dictionary where each key is an atom name and the value is the radius of that atom.

    Note:
        It seems that atomic radii are all equivalent with the exception of Hydrogen atoms.
        This may be because of the x-ray reading and predicted Hydrogen locations.
    """
    atom_info = {}
    for row in pqr_df.to_dicts():
        atom_name = row["atomName"]

        # If not hydrogen, strip trailing numbers (e.g., 'CA1' -> 'CA')
        if not atom_name.startswith("H"):
            atom_name = ''.join(filter(str.isalpha, atom_name))

        radius = row["radius"]

        if atom_name in atom_info and not isclose(atom_info[atom_name], radius, rel_tol=1e-5):
            print(f"Warning: Multiple radius values found for {atom_name}. Using the first encountered value.")
        elif not atom_name.startswith("H"):
            atom_info[atom_name] = radius

    return atom_info


def append_ligand_to_protein_pqr(
    protein_df: pl.DataFrame,
    ligand_df: pl.DataFrame,
    atom_info: Dict[str, float],
) -> pl.DataFrame:
    """
    Append ligand atoms from the MOL2 file to the protein structure from the PQR file.

    Args:
        protein_df (polars.DataFrame): DataFrame of the protein PQR file.
        ligand_df (polars.DataFrame): DataFrame of the ligand MOL2 file.
        atom_info (Dict[str, float]): Mapping of atom names to radii.

    Returns:
        polars.DataFrame: Combined DataFrame of protein and ligand with all necessary columns.
    """
    # Normalize atom names in ligand to match protein atom naming for radius mapping
    ligand_df = ligand_df.with_columns([
        pl.col("atom_name") \
          .map_elements(lambda x: ''.join(filter(str.isalpha, x)), return_dtype=pl.Utf8) \
          .alias("normalized_atom_name")
    ])

    # Map radius to each atom in the ligand
    ligand_df = ligand_df.with_columns(
        pl.col("normalized_atom_name") \
          .map_elements(lambda x: atom_info.get(x, np.nan), return_dtype=pl.Float64) \
          .alias("radius")
    )

    # Convert necessary columns to appropriate types to match the protein dataframe
    ligand_df_formatted = ligand_df.select([
        pl.lit("HETATM").alias("recordName"),
        pl.col("atom_id").cast(pl.Int64).alias("serial"),  # Cast to match the protein dataframe type
        pl.col("atom_name").alias("atomName"),
        pl.lit("LIG").alias("residueName"),
        pl.lit(1).cast(pl.Float64).alias("residueNumber"),  # Cast to match the protein dataframe type
        pl.col("x").alias("X"),
        pl.col("y").alias("Y"),
        pl.col("z").alias("Z"),
        pl.col("charge").cast(pl.Float64),  # Cast to match the protein dataframe type
        pl.col("radius")
    ])

    # Append ligand DataFrame to protein DataFrame
    combined_df = pl.concat([protein_df, ligand_df_formatted])

    # Assign new sequential serial numbers
    combined_df = combined_df.with_columns(
        pl.arange(1, combined_df.height + 1) \
          .alias("serial")
    )

    return combined_df


def write_pqr(dataframe: pl.DataFrame, file_path: str) -> None:
    """
    Write the contents of a Polars DataFrame to a PQR file.

    Args:
        dataframe (polars.DataFrame): DataFrame to write to a PQR file.
        file_path (str): Path of the file to write.
    """
    with open(file_path, 'w') as file:
        for row in dataframe.to_dicts():
            file.write(
                "{:<6}{:>5} {:>4} {:3} {:>4} {:>11.3f} {:>8.3f} {:>8.3f} {:>8.4f} {:>7.4f}\n".format(
                    row['recordName'], row['serial'], row['atomName'], row['residueName'],
                    int(row['residueNumber']), row['X'], row['Y'], row['Z'], row['charge'], row['radius']
                )
            )


def main() -> None:
    LIGAND_MOL2_FILE: str = sys.argv[1]
    PROTEIN_PQR_FILE: str = sys.argv[2]
    COMPLEX_PQR_FILE: str = sys.argv[3]
    OUTPUT_PQR_FILE: str  = sys.argv[4]

    df_ligand_mol2 = convert_mol2_to_polars_dataframe(LIGAND_MOL2_FILE)
    df_protein_pqr = convert_pqr_to_polars_dataframe(PROTEIN_PQR_FILE)
    df_complex_from_pdbbind_pqr = convert_pqr_to_polars_dataframe(COMPLEX_PQR_FILE)

    atom_info_mapping = create_atom_info_mapping(df_complex_from_pdbbind_pqr)

    df_combined = append_ligand_to_protein_pqr(df_protein_pqr, df_ligand_mol2, atom_info_mapping)
    write_pqr(df_combined, OUTPUT_PQR_FILE)
    print(f"Combined PQR file written to {OUTPUT_PQR_FILE}")

    """
    Note:
        ATOM	atomic coordinate record containing the X,Y,Z orthogonal Å coordinates
                for atoms in standard residues (amino acids and nucleic acids).
        HETATM	atomic coordinate record containing the X,Y,Z orthogonal Å coordinates
                for atoms in nonstandard residues. Nonstandard residues include inhibitors,
                cofactors, ions, and solvent. The only functional difference from ATOM
                records is that HETATM residues are by default not connected to other residues.
                Note that water residues should be in HETATM records.

    Source:
        https://www.cgl.ucsf.edu/chimera/docs/UsersGuide/tutorials/pdbintro.html#:~:text=The%20only%20functional%20difference%20from,should%20be%20in%20HETATM%20records.&text=indicates%20the%20end%20of%20a%20chain%20of%20residues.
    """


if __name__ == "__main__":
    main()
