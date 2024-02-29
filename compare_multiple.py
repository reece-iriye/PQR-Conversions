import polars as pl

from typing import Dict, Any

def parse_line(line: str) -> Dict[str, Any]:
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
    parsed_lines = []

    with open(file_path, 'r') as file:
        for line in file:
            # Stop iterating if we reach terminating point of PQR file
            if line == "TER\n" or line == "END" or line == "":
                continue
            elif (line.strip() and not line.startswith('#')):
                parsed_data = parse_line(line)
                parsed_lines.append(parsed_data)

    # Create a DataFrame
    return pl.DataFrame(parsed_lines)


if __name__ == "__main__":
    file_path = "./data/generated/10gs/pocket-ligand.pqr"
    df: pl.DataFrame = get_polars_pqr_dataframe(file_path)
    print(df)
