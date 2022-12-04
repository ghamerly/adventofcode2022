#!/usr/bin/env python3

# https://adventofcode.com/2022/day/4 - "Camp Cleanup"
# Author: Greg Hamerly

import sys

def interval_inside(a1, a2, b1, b2):
    return (a1 <= b1 and b2 <= a2) or (b1 <= a1 and a2 <= b2)

def overlap(a1, a2, b1, b2):
    return a1 <= b1 <= a2 or b1 <= a1 <= b2

def parse(line):
    a, b = line.split(',')
    return list(map(int, a.split('-') + b.split('-')))

def part1(intervals):
    return sum([interval_inside(*i) for i in intervals])

def part2(intervals):
    return sum([overlap(*i) for i in intervals])

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    intervals = list(map(parse, lines))

    print('part 1:', part1(intervals))
    print('part 2:', part2(intervals))

if __name__ == '__main__':
    main()
