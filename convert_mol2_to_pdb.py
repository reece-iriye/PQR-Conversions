import numpy as np

from typing import List, Dict, Any

from mol2_classes import Mol2Bond, Mol2Molecule, Mol2Atom, RADII


def read_mol2_file(mol2_file_path: str) -> Mol2Molecule:
    """
    Reads a MOL2 file and returns a populated Mol2Molecule object.
    """
    molecule = Mol2Molecule()
    with open(mol2_file_path, 'r') as file:
        molecule.read(file)
    return molecule


def assign_atom_parameters(
    molecule: Mol2Molecule,
    primary_dict: Dict[str, Any],
    secondary_dict: Dict[str, Any],
) -> None:
    """
    Assigns radii and charges to each atom in the molecule.
    """
    molecule.assign_parameters(primary_dict=primary_dict, secondary_dict=secondary_dict)


def generate_pdb_lines(molecule: Mol2Molecule) -> List[str]:
    """
    Generates PDB formatted lines from a Mol2Molecule.
    """
    pdb_lines = []
    for atom in molecule.atoms.values():
        pdb_line = f"HETATM{atom.serial:>5} {atom.name:<4} {atom.res_name:<3} L{atom.res_seq:>4}    {atom.x:>8.3f}{atom.y:>8.3f}{atom.z:>8.3f}{atom.charge:>6.2f}{atom.radius:>6.2f}"
        pdb_lines.append(pdb_line)
    return pdb_lines


def write_to_pdb_file(pdb_lines: List[str], output_file_path: str) -> None:
    """
    Writes given PDB lines to a file.
    """
    with open(output_file_path, 'w') as file:
        for line in pdb_lines:
            file.write(line + "\n")


if __name__ == "__main__":
    # Example usage for single MOL2 file
    mol2_file_path = "data/pdbbind/5tmn/5tmn_ligand.mol2"
    output_pdb_file_path = "data/generated/5tmn/5tmn_ligand.pdb"

    # Mol2 file read and write to PDB file
    molecule = read_mol2_file(mol2_file_path)
    assign_atom_parameters(molecule, primary_dict=RADII["zap9"], secondary_dict=RADII["bondi"])
    pdb_lines = generate_pdb_lines(molecule)
    write_to_pdb_file(pdb_lines, output_pdb_file_path)

    print(f"Conversion complete. PDB file written to {output_pdb_file_path}.")
