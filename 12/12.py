#!/usr/bin/env python3

# https://adventofcode.com/2022/day/12 - "Hill Climbing Algorithm"
# Author: Greg Hamerly
# start: Mon Dec 12 00:42:25 CST 2022
# part 1: Mon Dec 12 00:57:37 CST 2022
# part 2: Mon Dec 12 00:59:29 CST 2022

# The change in difficulty for today's part 2 was so much smaller than most
# days; you just had to reverse the natural direction of search. In fact, I
# changed the method of part 1 after the fact to use the same approach.

import sys

def bfs(grid, start, is_end, permitted_dist):
    '''Breadth-first search from start until satisfying is_end(r, c). Each step
    is allowed (or not) by permitted_dist(d).'''
    frontier = [start]
    seen = {start}
    steps = 0
    while frontier:
        new_frontier = []
        for r, c in frontier:
            if is_end(r, c):
                return steps
            for rr, cc in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]:
                if 0 <= rr < len(grid) and 0 <= cc < len(grid[0]) and \
                        (rr, cc) not in seen and \
                        permitted_dist(grid[rr][cc] - grid[r][c]):
                    seen.add((rr, cc))
                    new_frontier.append((rr, cc))

        frontier = new_frontier
        steps += 1

def part1(grid, start, end):
    '''Search from start to end.'''
    is_end = lambda r, c: (r, c) == end
    permitted_dist = lambda d: d <= 1
    return bfs(grid, start, is_end, permitted_dist)

def part2(grid, start, end):
    '''Search from the *end* to *any square with height 0*. Since we are
    searching backwards, permitted distances are -1 or *higher*.'''
    is_end = lambda r, c: grid[r][c] == 0
    permitted_dist = lambda d: d >= -1
    return bfs(grid, end, is_end, permitted_dist)

def mogrify(line):
    return [ord(c) - ord('a') for c in line]

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    grid = list(map(mogrify, lines))

    start = end = None
    for ri, row in enumerate(lines):
        if 'S' in row:
            start = (ri, row.index('S'))
        if 'E' in row:
            end = (ri, row.index('E'))

    grid[start[0]][start[1]] = 0
    grid[end[0]][end[1]] = 25

    print('part 1:', part1(grid, start, end))
    print('part 2:', part2(grid, start, end))

if __name__ == '__main__':
    main()
