#!/usr/bin/env python3

# https://adventofcode.com/2022/day/8 - "Treetop Tree House"
# Author: Greg Hamerly

import sys

def part1(data):
    '''Try to be somewhat efficient. This runs in O(rows*cols), or O(n) for an
    input of size n. However, this was probably overkill for this task.'''

    rows = len(data)
    cols = len(data[0])

    # create a grid of the tallest trees in each of the four directions (not
    # including the current tree)
    west  = [[-1] * (cols) for _ in range(rows)]
    east  = [[-1] * (cols) for _ in range(rows)]
    north = [[-1] * (cols) for _ in range(rows)]
    south = [[-1] * (cols) for _ in range(rows)]

    num_visible = 0
    for r in range(rows):
        for c in range(cols):
            if c > 0:
                west[r][c] = max(west[r][c-1], data[r][c-1])
            if c + 1 < cols:
                east[r][cols-c-2] = max(east[r][cols-c-1], data[r][cols-c-1])
            if r > 0:
                north[r][c] = max(north[r-1][c], data[r-1][c])
            if r + 1 < rows:
                south[rows-r-2][c] = max(south[rows-r-1][c], data[rows-r-1][c])

    # now finding the answer is easy; inspect every tree and compare it with the
    # tallest tree in each direction
    for r in range(rows):
        for c in range(cols):
            if data[r][c] > min(west[r][c], east[r][c], north[r][c], south[r][c]):
                num_visible += 1

    return num_visible


def part2(data):
    '''Don't try to be clever here, just compute the answer. If we had a really
    huge map, and there was no limit on the heights of trees (and this
    brute-force method were too slow), we could build the same four structures
    as in part1 (NSEW), and then use binary search to identify the answer in
    each of the four directions. That would run in O(n log n) instead of this
    approach which is O(n^2).  However, the height limit on trees (max 9) and
    the relatively small size of this map make this brute force approach fast
    enough.

    If we had a huge map and unlimited tree heights, we might also start pruning
    answers if we could prove that we had already found a larger max_score than
    was possible to compute for a given (r, c). But all of that is just work
    that doesn't need to be done today.'''

    rows = len(data)
    cols = len(data[0])

    # Helper function -- walk until you cannot see past a tree (or you reach the
    # edge).
    def count(r, c, dr, dc):
        i = 1
        rr = lambda x: r + x * dr
        cc = lambda x: c + x * dc
        while 0 < rr(i) < rows-1 and 0 < cc(i) < cols-1 and data[rr(i)][cc(i)] < data[r][c]:
            i += 1
        return i

    max_score = 0
    for r in range(1, rows-1):
        for c in range(1,cols-1):
            west  = count(r, c,  0, -1)
            east  = count(r, c,  0,  1)
            north = count(r, c, -1,  0)
            south = count(r, c,  1,  0)
            score = east * west * north * south
            max_score = max(max_score, score)

    return max_score

def mogrify(line):
    return list(map(int, line))

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
