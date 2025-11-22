#!/usr/bin/env python3
import argparse
import zipfile
import sys
import xml.dom.minidom
import difflib
from pathlib import Path

def get_pretty_xml_content(zip_path, internal_path="word/document.xml"):
    """
    Extracts an XML file from a zip archive and returns its pretty-printed content as a list of strings.
    """
    try:
        with zipfile.ZipFile(zip_path, 'r') as z:
            try:
                with z.open(internal_path) as f:
                    xml_content = f.read()
                    dom = xml.dom.minidom.parseString(xml_content)
                    pretty_xml = dom.toprettyxml(indent="  ")
                    # Split into lines and remove empty lines for cleaner diff
                    return [line + '\n' for line in pretty_xml.split('\n') if line.strip()]
            except KeyError:
                print(f"Error: '{internal_path}' not found in '{zip_path}'.")
                return None
    except zipfile.BadZipFile:
        print(f"Error: '{zip_path}' is not a valid zip file.")
        return None
    except Exception as e:
        print(f"Error reading '{zip_path}': {e}")
        return None

def diff_documents(file1, file2):
    path1 = Path(file1).resolve()
    path2 = Path(file2).resolve()

    if not path1.exists():
        print(f"Error: File '{path1}' does not exist.")
        sys.exit(1)
    if not path2.exists():
        print(f"Error: File '{path2}' does not exist.")
        sys.exit(1)

    print(f"Comparing 'word/document.xml' in '{path1.name}' and '{path2.name}'...")

    content1 = get_pretty_xml_content(path1)
    content2 = get_pretty_xml_content(path2)

    if content1 is None or content2 is None:
        sys.exit(1)

    diff = difflib.unified_diff(
        content1, 
        content2, 
        fromfile=f"{path1.name}/word/document.xml", 
        tofile=f"{path2.name}/word/document.xml"
    )

    diff_output = "".join(diff)
    
    if diff_output:
        print(diff_output)
    else:
        print("No differences found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare 'word/document.xml' between two OOXML documents.")
    parser.add_argument("file1", help="Path to the first document (zip file)")
    parser.add_argument("file2", help="Path to the second document (zip file)")
    
    args = parser.parse_args()
    
    diff_documents(args.file1, args.file2)
