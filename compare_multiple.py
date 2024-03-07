import polars as pl

from typing import List, Dict, Any


def _parse_line(line: str) -> Dict[str, Any]:
    """
    Parse each individual line of the PQR schema.

    Args:
        line (str): Text-based string representing a line in the PQR file.
    Returns:
        Dict[str, Any]: Dictionary representation of a row.
    """
    parts = line.split()  # Splitting by whitespace
    print(parts)
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


def get_polars_pqr_dataframe(file_path: str) -> pl.DataFrame:
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
            if line == "TER\n" or line == "END" or line == "":
                continue
            elif (line.strip() and not line.startswith('#')):
                parsed_data = _parse_line(line)
                parsed_lines.append(parsed_data)

    return pl.DataFrame(parsed_lines)


def analyze_pqr_dataframes(dfs: List[pl.DataFrame]) -> None:
    """
    Analyzes PQR dataframes for total number of atoms, number of same atoms,
    and coordinate deviations.

    Args:
        dfs (List[pl.DataFrame]): List of DataFrames to analyze.
    """
    file_types = ["protein", "complex", "pocket-ligand"]
    for i, (file_type, df) in enumerate(zip(file_types, dfs)):
        total_atoms = df.height
        same_atoms = df.group_by("atomName").agg(pl.count("atomName").alias("count"))
        coord_deviation_x = df.select(pl.col("X").std()).get_column("X").to_numpy()[0]
        coord_deviation_y = df.select(pl.col("Y").std()).get_column("Y").to_numpy()[0]
        coord_deviation_z = df.select(pl.col("Z").std()).get_column("Z").to_numpy()[0]

        print(f"DataFrame {i+1} [{file_type}]:")
        print(f"Total Number of Atoms: {total_atoms}")
        print("Number of Same Atoms:")
        print(same_atoms)
        print("Coordinate Deviations:")
        print(f"X: {coord_deviation_x:.2f}, Y: {coord_deviation_y:.2f}, Z: {coord_deviation_z:.2f}")
        print("-" * 40)


if __name__ == "__main__":
    file_path_10gs = "./data/generated/10gs"
    protein_10gs = f"{file_path_10gs}/protein.pqr"
    complex_10gs = f"{file_path_10gs}/protein-ligand.pqr"
    pocket_ligand_10gs = f"{file_path_10gs}/pocket-ligand.pqr"
    files_10gs = [protein_10gs, complex_10gs, pocket_ligand_10gs]
    dfs_10gs = []

    for file in files_10gs:
        df: pl.DataFrame = get_polars_pqr_dataframe(file)
        dfs_10gs.append(df)

    analyze_pqr_dataframes(dfs_10gs)
