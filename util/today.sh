#!/bin/bash

if [ $# -ne 0 ]; then
    DAY_PADDED=$1
else
    # Guess the day based on UTC date (hackish but should work for programming in
    # the moment)
    DAY_PADDED=$(date -u "+%d")
fi

if [ -d $DAY_PADDED ]; then
    echo "directory $DAY_PADDED already exists; stopping"
    exit
fi

# remove any leading zero if needed
DAY_UNPADDED=$(echo $DAY_PADDED | sed "s/^0//")

# name things
DIRNAME=$DAY_PADDED
PROGRAM=$DAY_PADDED/$DAY_UNPADDED.py
INPUT=$DAY_PADDED/$DAY_UNPADDED.in

# create the directory and the (blank) input file (paste contents manually)
mkdir $DIRNAME
touch $INPUT

# use curl to grab the title of today's challenge to put it in the program
TITLE=$(curl https://adventofcode.com/2022/day/$DAY_UNPADDED | \
    grep '<article class="day-desc">' | \
    sed -r 's/.*Day [0-9]+: //' | \
    sed 's/ ---.*//')

# create a template program
cat <<PROGRAM > $PROGRAM
#!/usr/bin/env python3

# https://adventofcode.com/2022/day/$DAY_UNPADDED - "$TITLE"
# Author: Greg Hamerly

import sys

def part1(data):
    for x in data:
        pass

def part2(data):
    for x in data:
        pass

def mogrify(line):
    return line

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    data = list(map(mogrify, lines))

    print('part 1:', part1(data))
    print('part 2:', part2(data))

if __name__ == '__main__':
    main()
PROGRAM

# mark the program executable
chmod +x $PROGRAM
