#!/usr/bin/env python3

# https://adventofcode.com/2022/day/1 - "calorie counting"
# Author: Greg Hamerly

import sys

def part1(elves):
    return max(elves)

def part2(elves):
    return sum(sorted(elves)[-3:])

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    elves = [0]
    for line in lines:
        if not line:
            elves.append(0)
            continue
        else:
            elves[-1] += int(line)

    print('part 1:', part1(elves))
    print('part 2:', part2(elves))

if __name__ == '__main__':
    main()
