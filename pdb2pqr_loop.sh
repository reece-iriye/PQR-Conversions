#!/bin/bash

# Base directory containing the atom folders and pdb files.
SOURCE_DIR="data/pdbbind"

# Base directory for the output PQR files.
OUTPUT_DIR="data/generated"

# Loop through all subdirectories of SOURCE_DIR
for ATOM_FOLDER in "$SOURCE_DIR"/*; do
    if [ -d "$ATOM_FOLDER" ]; then
        # Extract the atom name from the folder path
        ATOM_NAME=$(basename "$ATOM_FOLDER")

        # Define the input and output file paths
        INPUT_FILE="${ATOM_FOLDER}/${ATOM_NAME}_protein.pdb"
        OUTPUT_FOLDER="${OUTPUT_DIR}/${ATOM_NAME}"
        OUTPUT_FILE="${OUTPUT_FOLDER}/${ATOM_NAME}_protein.pqr"

        # Check if the input file exists
        if [ -f "$INPUT_FILE" ]; then
            # Create the output directory if it doesn't exist
            mkdir -p "$OUTPUT_FOLDER"

            # Run pdb2pqr on the input file, specifying the force field and output file
            pdb2pqr --ff=AMBER "$INPUT_FILE" "$OUTPUT_FILE"

            echo "Processed $INPUT_FILE -> $OUTPUT_FILE"
        else
            echo "Input file not found: $INPUT_FILE"
        fi
    fi
done

echo "All files processed."
