#!/usr/bin/env python3

# https://adventofcode.com/2022/day/6 - "Tuning Trouble"
# Author: Greg Hamerly

import sys

def first_marker_of_length(line, length):
    for i in range(length, len(line)):
        if len(set(line[i-length:i])) == length:
            return i

def part1(line):
    return first_marker_of_length(line, 4)

def part2(line):
    return first_marker_of_length(line, 14)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    for i, line in enumerate(lines):
        print(f'line {i}')
        print('part 1:', part1(line))
        print('part 2:', part2(line))

if __name__ == '__main__':
    main()
