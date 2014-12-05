#!/bin/bash

# extract-document.sh - Extracts and pretty-prints the contents of an
# OOXML or ODF document file.
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
# * Add usage notice

die () {
    echo >&2 "$@"
    exit 1
}

DOCUMENT_PATH=$1

# check document exists
[ -n "$DOCUMENT_PATH" ] || die "No file name provided"
[ -e $DOCUMENT_PATH ]   || die "File $DOCUMENT_PATH does not exist"

# get name
EXT=${DOCUMENT_PATH##*.}
EXTRACT_DIR=`basename -s .$EXT $DOCUMENT_PATH`

# extract document
unzip $DOCUMENT_PATH -d $EXTRACT_DIR

# clean XML
cd $EXTRACT_DIR
find ./ -name "*.rels" -o -name "*.xml" -exec \
    tidy -q -m -i -xml -utf8 '{}' +

