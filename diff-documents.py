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

def diff_documents(file1, file2, internal_path=None):
    path1 = Path(file1).resolve()
    path2 = Path(file2).resolve()

    if not path1.exists():
        print(f"Error: File '{path1}' does not exist.")
        sys.exit(1)
    if not path2.exists():
        print(f"Error: File '{path2}' does not exist.")
        sys.exit(1)

    # Check extensions
    ext1 = path1.suffix.lower()
    ext2 = path2.suffix.lower()

    if ext1 != ext2:
        print(f"Error: Files must have the same extension. Got '{ext1}' and '{ext2}'.")
        sys.exit(1)

    # Determine internal path based on extension if not provided
    if internal_path is None:
        if ext1 == ".docx":
            internal_path = "word/document.xml"
        elif ext1 == ".pptx":
            internal_path = "ppt/presentation.xml"
        elif ext1 == ".xlsx":
            internal_path = "xl/workbook.xml"
        else:
            print(f"Error: Unsupported file extension '{ext1}'. Supported: .docx, .pptx, .xlsx")
            sys.exit(1)

    print(f"Comparing '{internal_path}' in '{path1.name}' and '{path2.name}'...")

    content1 = get_pretty_xml_content(path1, internal_path)
    content2 = get_pretty_xml_content(path2, internal_path)

    if content1 is None or content2 is None:
        sys.exit(1)

    diff = difflib.unified_diff(
        content1, 
        content2, 
        fromfile=f"{path1.name}/{internal_path}",
        tofile=f"{path2.name}/{internal_path}"
    )

    diff_output = "".join(diff)
    
    if diff_output:
        print(diff_output)
    else:
        print("No differences found.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare internal XML content between two OOXML documents (docx, pptx, xlsx).")
    parser.add_argument("file1", help="Path to the first document (zip file)")
    parser.add_argument("file2", help="Path to the second document (zip file)")
    parser.add_argument("internal_path", nargs="?", help="Optional path to the file inside the zip to diff")
    
    args = parser.parse_args()
    
    diff_documents(args.file1, args.file2, args.internal_path)
