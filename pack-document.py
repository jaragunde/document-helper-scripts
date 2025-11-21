#!/usr/bin/env python3
import argparse
import zipfile
import sys
import os
from pathlib import Path

def pack_directory(directory_path):
    """
    Creates a zip file with the contents of the specified directory.
    The zip file will be named like the original directory, with the suffix "-repacked".
    """
    dir_path = Path(directory_path).resolve()

    if not dir_path.exists():
        print(f"Error: The directory '{dir_path}' does not exist.")
        sys.exit(1)

    if not dir_path.is_dir():
        print(f"Error: '{dir_path}' is not a directory.")
        sys.exit(1)

    # Determine the output zip file path
    # Name: <directory_name>-repacked.zip
    # Location: Same parent directory as the input directory
    zip_filename = f"{dir_path.name}-repacked.zip"
    zip_path = dir_path.parent / zip_filename

    try:
        print(f"Packing contents of '{dir_path}' into '{zip_path}'...")

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the directory
            for root, dirs, files in os.walk(dir_path):
                for file in files:
                    file_path = Path(root) / file
                    # Calculate the archive name (relative to the source directory)
                    # This ensures files are at the root of the zip, not inside a folder named <directory_name>
                    archive_name = file_path.relative_to(dir_path)
                    
                    print(f"Adding: {archive_name}")
                    zipf.write(file_path, archive_name)

        print(f"Packing complete. Created: {zip_path}")

    except Exception as e:
        print(f"An error occurred during packing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pack a directory into a zip file with suffix '-repacked'.")
    parser.add_argument("directory_path", help="Path to the directory to pack")
    
    args = parser.parse_args()
    
    pack_directory(args.directory_path)
