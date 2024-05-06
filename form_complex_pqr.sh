#!/bin/bash


# Parse the named argument for the root directory
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        --directory=*)
        ROOT_DIR="${key#*=}"
        shift
        ;;
        *)
        echo "Unknown argument: $1"
        exit 1
        ;;
    esac
done

# Check if the root directory is provided
if [ -z "$ROOT_DIR" ]; then
    echo "Please provide the root directory using the --directory argument."
    exit 1
fi

# Get the list of subdirectories at level 1
subdirs=$(find "$ROOT_DIR" -maxdepth 1 -mindepth 1 -type d)

# Iterate through the subdirectories and run the Python script
for subdir in $subdirs; do
    echo "Processing subdirectory: $subdir"
    python form_complex_pqr.py --directory="$subdir"
    echo "Finished processing $subdir"
    echo "---"
done
