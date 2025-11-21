#!/bin/bash

# extract-document.sh - Extracts and pretty-prints the contents of an
# OOXML or ODF document file.
# Copyright (C) 2025 Igalia, S.L. <info@igalia.com>
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

DOCUMENT1_PATH=$1
DOCUMENT2_PATH=$2

# check document exists
[ -n "$DOCUMENT1_PATH" ] || die "Two documents must be provided"
[ -n "$DOCUMENT2_PATH" ] || die "Two documents must be provided"
[ -e $DOCUMENT1_PATH ]   || die "File $DOCUMENT1_PATH does not exist"
[ -e $DOCUMENT2_PATH ]   || die "File $DOCUMENT2_PATH does not exist"

EXT1=${DOCUMENT1_PATH##*.}
DIR1=`basename -s .$EXT1 $DOCUMENT1_PATH`
unzip $DOCUMENT1_PATH -d $DIR1
cd $DIR1
find ./ -name "*.rels" -o -name "*.xml" -exec \
    tidy -q -m -i -xml -utf8 '{}' +
cd ..

EXT2=${DOCUMENT2_PATH##*.}
DIR2=`basename -s .$EXT2 $DOCUMENT2_PATH`
unzip $DOCUMENT2_PATH -d $DIR2
cd $DIR2
find ./ -name "*.rels" -o -name "*.xml" -exec \
    tidy -q -m -i -xml -utf8 '{}' +
cd ..


diff -r $DIR1/word/document.xml $DIR2/word/document.xml
