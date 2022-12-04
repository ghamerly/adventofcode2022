#!/bin/bash

# Run this from within the directory to be committed.

set -e

NAME=$(grep https *.py | head -n 1 | sed 's/.* "//' | sed 's/"//' | tr '[:upper:]' '[:lower:]')
DAY=$(basename $(pwd))
git add . && git commit -m "AoC 2022 day $DAY: $NAME"
