#!/usr/bin/env python3
import argparse
import zipfile
import sys
import xml.dom.minidom
from pathlib import Path

def beautify_xml_files(directory):
    """
    Searches for .xml and .xml.rels files in the directory and beautifies them.
    """
    print(f"Looking for XML files to beautify in '{directory}'...")
    for file_path in directory.rglob("*"):
        # Check for suffixes. Note: .xml.rels ends with .rels, but user asked for "suffix xml or xml.rels"
        # We can check string ending.
        if file_path.is_file() and (file_path.name.endswith(".xml") or file_path.name.endswith(".xml.rels")):
            try:
                # Parse the XML file
                dom = xml.dom.minidom.parse(str(file_path))

                # specific fix for minidom adding too much whitespace:
                # We can just use toprettyxml, but often it adds extra newlines.
                # Let's do a simple strip of empty lines to make it cleaner.
                pretty_xml_as_string = dom.toprettyxml(indent="  ")

                # Filter out empty lines
                pretty_xml_as_string = "\n".join([line for line in pretty_xml_as_string.split('\n') if line.strip()])

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(pretty_xml_as_string)

                print(f"Beautified: {file_path.relative_to(directory.parent)}")
            except Exception as e:
                print(f"Warning: Could not beautify '{file_path.name}': {e}")

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

    if destination_dir.exists():
        response = input(f"Directory '{destination_dir}' already exists. Overwrite? (y/N): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            sys.exit(0)

    try:
        print(f"Extracting '{zip_path.name}' to '{destination_dir}'...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
            
        print("Extraction complete.")

        beautify_xml_files(destination_dir)

    except Exception as e:
        print(f"An error occurred during extraction: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract a zip file to a directory with the same name.")
    parser.add_argument("file_path", help="Path to the zip file to extract")
    
    args = parser.parse_args()
    
    extract_zip(args.file_path)
