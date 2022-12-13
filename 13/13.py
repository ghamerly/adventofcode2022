#!/usr/bin/env python3

# https://adventofcode.com/2022/day/13 - "Distress Signal"
# Author: Greg Hamerly

import sys
import json

def compare(a, b):
    '''General recursive comparator for lists and integers, as defined in the
    problem.'''
    a_list, b_list = isinstance(a, list), isinstance(b, list)

    if a_list and b_list:
        for ai, bi in zip(a, b):
            c = compare(ai, bi)
            if c is not None:
                return c

        return None if len(a) == len(b) else len(a) < len(b)

    if a_list | b_list:
        return compare(a, [b]) if a_list else compare([a], b)

    return None if a == b else a < b

def part1(pairs):
    return sum([i + 1 for i, (a, b) in enumerate(pairs) if compare(a, b)])

class ComparableList:
    '''Wrapper class so that we can provide a less-than operator for comparing
    lists.'''
    def __init__(self, lst):
        self.list = lst

    def __lt__(self, other):
        return compare(self.list, other.list)

def part2(pairs):
    '''Flatten the list of pairs, add two special lists ("divider packets"),
    wrap all objects in ComparableList objects, sort, then compute the answer
    from the indexes of the two "divider packets".'''
    dps = [[[2]], [[6]]] # divider packets
    comparables = sum([list(map(ComparableList, p)) for p in pairs], [])
    comparables.extend(map(ComparableList, dps))
    lists = [c.list for c in sorted(comparables)]
    return (lists.index(dps[0]) + 1) * (lists.index(dps[1]) + 1)

def mogrify(line):
    return json.loads(line)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    pairs = [list(map(mogrify, lines[i:i+2])) for i in range(0, len(lines), 3)]
    
    print('part 1:', part1(pairs))
    print('part 2:', part2(pairs))

if __name__ == '__main__':
    main()
