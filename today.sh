#!/bin/bash

set -e

LAST=$(ls | grep "^[0-9][0-9]$" | sort -g | tail -n 1)
LAST_UNPADDED=$(echo $LAST | sed "s/^0//")
TODAY=$((LAST_UNPADDED+1))
TODAY_PADDED=$(printf "%02d" $TODAY)
echo "copying $LAST => $TODAY_PADDED"
cp -r $LAST $TODAY_PADDED
cd $TODAY_PADDED
mv *.in $TODAY.in
mv *.py $TODAY.py
