#!/usr/bin/env python3
import argparse
import zipfile
import sys
from pathlib import Path

def extract_zip(file_path):
    """
    Extracts a zip archive to a directory with the name of the file minus the suffix,
    in the same parent directory.
    """
    zip_path = Path(file_path).resolve()

    if not zip_path.exists():
        print(f"Error: The file '{zip_path}' does not exist.")
        sys.exit(1)

    if not zipfile.is_zipfile(zip_path):
        print(f"Error: The file '{zip_path}' is not a valid zip file.")
        sys.exit(1)

    # Determine the destination directory
    # zip_path.stem returns the filename without the last suffix (e.g., 'archive.zip' -> 'archive')
    # If the file has multiple suffixes (e.g. .tar.gz), stem only removes .gz. 
    # The user asked for "minus the suffix", usually implying the extension.
    destination_dir = zip_path.parent / zip_path.stem

    try:
        print(f"Extracting '{zip_path.name}' to '{destination_dir}'...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
            
        print("Extraction complete.")

    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a zip file to a directory with the same name.")
    parser.add_argument("file_path", help="Path to the zip file to extract")
    
    args = parser.parse_args()
    
    extract_zip(args.file_path)
