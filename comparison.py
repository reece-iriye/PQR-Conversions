import sys
from typing import List, Tuple, Any


def _is_subset(subset: List[Any], superset: List[Any]) -> bool:
    """
    Check if subset is a subset of superset.
    """
    return all(item in superset for item in subset)


def _contains_exclusively(sublist: List[Any], mainlist: List[Any]) -> bool:
    """
    Check if sublist contains exclusively lines from mainlist.
    """
    return all(item in mainlist for item in sublist)


def compare_files(
    protein_file_path: str,
    ligand_file_path: str,
    complex_file_path: str,
) -> Tuple[bool, bool, int]:
    """
    Compare contents of three text files containing protein, ligand, and complex data.
    
    Parameters:
        protein_file_path (str): The file path of the protein data file.
        ligand_file_path (str): The file path of the ligand data file.
        complex_file_path (str): The file path of the complex data file.
    
    Returns:
        Tuple[bool, bool, int]: A tuple containing:
            - The first boolean indicates whether the protein and ligand data are subsets of the complex data.
            - The second boolean indicates whether the complex data exclusively contains lines from both protein and ligand data.
            - The integer representing the count of lines that are not part of the subset if both comparisons are false. 
    Raises:
        FileNotFoundError: If one or more files specified by the file paths do not exist.
    """
    try:
        with (
            open(protein_file_path, 'r') as protein_file, 
            open(ligand_file_path, 'r') as ligand_file, 
            open(complex_file_path, 'r') as complex_file,
        ):
            protein_lines: List[str] = protein_file.readlines()
            ligand_lines: List[str] = ligand_file.readlines()
            complex_lines: List[str] = complex_file.readlines()

            protein_atom_lines = [line for line in protein_lines if line.startswith("ATOM")]
            ligand_atom_lines = [line for line in ligand_lines if line.startswith("ATOM")]
            complex_atom_lines = [line for line in complex_lines if line.startswith("ATOM")]
            
            
            # Check if protein_atom_lines and ligand_atom_lines are subsets of complex_atom_lines
            are_subsets = (
                _is_subset(protein_atom_lines, complex_atom_lines) and 
                _is_subset(ligand_atom_lines, complex_atom_lines)
            )

            # Check if complex_atom_lines contains exclusively lines from protein_atom_lines and ligand_atom_lines
            exclusively_from_both = (
                _contains_exclusively(
                    sublist=protein_atom_lines + ligand_atom_lines, 
                    mainlist=complex_atom_lines,
                )
            )

            if not are_subsets and not exclusively_from_both:
                count_not_in_subset = len([
                    line 
                    for line in complex_atom_lines 
                    if line not in protein_atom_lines + ligand_atom_lines
                ])
                return are_subsets, exclusively_from_both, count_not_in_subset
            else:
                return are_subsets, exclusively_from_both, 0
            
    except FileNotFoundError:
        print("One or more files does not exist.")


if __name__ == "__main__":
    PROTEIN_FILE_PATH: str = sys.argv[1]
    LIGAND_FILE_PATH: str  = sys.argv[2]
    COMPLEX_FILE_PATH: str = sys.argv[3]

    are_subsets, exclusively_from_both, count_not_in_subset = compare_files(
        protein_file_path = PROTEIN_FILE_PATH, 
        ligand_file_path = LIGAND_FILE_PATH, 
        complex_file_path = COMPLEX_FILE_PATH,
    )
    print("Are Subsets?:", str(are_subsets))
    print("Are Exclusively from both?:", str(exclusively_from_both))
    print("Total not in subset: ", str(count_not_in_subset))
    
