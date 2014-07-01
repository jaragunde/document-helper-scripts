#!/bin/bash

# create-document.sh - Creates an OOXML document file from a set of
# uncompressed sources.
# Copyright (C) 2013 Igalia, S.L. <info@igalia.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# TODO:
# * Support file paths with spaces
# * Parameter to specify the output document name.
# * Check that any spacing is removed from the XML sources.

die () {
    echo >&2 "$@"
    exit 1
}

DOCUMENT_FILES_PATH=$1
CURRENT_PATH=`pwd`

# check document exists
[ -n "$DOCUMENT_FILES_PATH" ] || die "No path provided"
[ -e $DOCUMENT_FILES_PATH ]   || die "Directory $DOCUMENT_FILES_PATH does not exist"

# remove old document
if [ -e document.docx ]; then
  echo "Existing file document.docx removed"
  rm document.docx
fi

# compress files
cd $DOCUMENT_FILES_PATH
zip -r $CURRENT_PATH/document.docx * --exclude \*~
