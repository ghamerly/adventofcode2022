#!/usr/bin/env python3

# https://adventofcode.com/2022/day/3 - "Rucksack Reorganization"
# Author: Greg Hamerly

import sys

scores_lower = { chr(ord('a') + i): i + 1 for i in range(26) }
scores_upper = { chr(ord('A') + i): i + 27 for i in range(26) }
scores = scores_lower | scores_upper

def score_common(*items):
    global scores
    common = set(items[0])
    for i in range(1, len(items)):
        common &= set(items[i])
    return sum([scores[c] for c in common])

def part1(lines):
    score = 0
    for line in lines:
        n = len(line)
        assert n % 2 == 0
        a, b = line[:n//2], line[n//2:]
        score += score_common(a, b)
    return score

def part2(lines):
    score = 0
    for i in range(0, len(lines), 3):
        a, b, c = lines[i:i+3]
        score += score_common(a, b, c)
    return score

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    print('part 1:', part1(lines))
    print('part 2:', part2(lines))

if __name__ == '__main__':
    main()
