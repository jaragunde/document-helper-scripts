# LibreOffice Document Helper Scripts

This repository contains a collection of scripts to help with extracting, inspecting, and repacking LibreOffice/OOXML documents (such as `.docx`, `.xlsx`, `.pptx`, and `.odt`).

## Python Scripts

These are the recommended scripts for general usage as they handle cross-platform compatibility and XML beautification robustly.

### `extract-document.py`

Extracts a zip-based document (like a `.docx` file) to a directory and beautifies the XML contents for easier inspection.

**Usage:**
```bash
python3 extract-document.py <path_to_document>
```

**Features:**
- Extracts contents to a folder named after the file (e.g., `mydoc.docx` -> `mydoc`).
- Automatically finds `.xml` and `.xml.rels` files and formats them (pretty-prints) to make them human-readable.

### `pack-document.py`

Repacks a directory back into a zip-based document.

**Usage:**
```bash
python3 pack-document.py <directory_path> [output_name]
```

**Features:**
- Detects the document type based on folder structure (`word` -> `.docx`, `xl` -> `.xlsx`, etc.).
- Creates a new file with a `-repacked` suffix by default (e.g., `mydoc-repacked.docx`).
- Can specify a custom output filename.

### `diff-documents.py`

Compares the internal XML content of two documents based on their extension:
- `.docx`: `word/document.xml`
- `.pptx`: `ppt/presentation.xml`
- `.xlsx`: `xl/workbook.xml`

**Usage:**
```bash
python3 diff-documents.py <doc1> <doc2> [internal_file_path]
```

**Features:**
- Automatically selects the correct XML file to compare based on extension.
- Can optionally specify a specific file inside the zip to compare (e.g., `word/styles.xml`).
- Pretty-prints XML before comparing to ignore formatting differences.
- Outputs a unified diff.

## Bash Scripts

These scripts are provided as alternatives or for specific workflows on Linux systems.

### `extract-document.sh`
A Bash implementation of the extraction logic.
**Requires:** `unzip`, `tidy`
**Usage:** `./extract-document.sh <document>`

### `create-document.sh`
Simple script to zip a directory into `document.docx`.
**Usage:** `./create-document.sh <directory>`

### `diff-documents.sh`
Extracts and compares two documents, showing the diff of `document.xml`.
**Requires:** `unzip`, `tidy`
**Usage:** `./diff-documents.sh <doc1> <doc2>`

## Prerequisites

- **Python 3**
- **Standard Utilities** (for Bash scripts): `zip`, `unzip`, `tidy` (usually available via package managers like `apt` or `brew`).
