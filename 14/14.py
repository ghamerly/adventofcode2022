#!/usr/bin/env python3

# https://adventofcode.com/2022/day/14 - "Regolith Reservoir"
# Author: Greg Hamerly

import sys

def simulate(grid, is_done, keep_extra_sand):
    highest = max([r for r, c in grid])
    original_size = len(grid)
    while not is_done(grid):
        sand = (0, 500) # given starting point

        while sand[0] < highest + 1:
            for dc in (0, -1, 1):
                next_sand = (sand[0] + 1, sand[1] + dc)
                if next_sand not in grid:
                    break

            if next_sand in grid:
                grid.add(sand)
                break
            else:
                sand = next_sand
        else:
            if keep_extra_sand:
                grid.add(sand)
            else:
                break

    return len(grid) - original_size

def part1(grid):
    return simulate(grid, lambda g: False, False)

def part2(grid):
    return simulate(grid, lambda g: (0, 500) in g, True)

def mogrify(line):
    # split on the arrows, then split each pair, and swap the row and column
    return [tuple(map(int, c.split(',')[::-1])) for c in line.split(' -> ')]

def iterate(a, b):
    '''If a <= b, then iterate over the range [a,b]; otherwise iterate over [b,a].'''
    start, end = (a, b + 1) if a <= b else (b, a + 1)
    yield from range(start, end)

def fill_grid(paths):
    grid = set()
    for path in paths:
        for i in range(1, len(path)):
            prev, cur = path[i-1], path[i]
            for r in iterate(prev[0], cur[0]):
                for c in iterate(prev[1], cur[1]):
                    grid.add((r, c))
    return grid

def plot_grid(grid):
    min_row, max_row = min([r for r, c in grid]), max([r for r, c in grid])
    min_col, max_col = min([c for r, c in grid]), max([c for r, c in grid])

    for r in range(min_row, max_row + 1):
        row = ['#' if (r, c) in grid else '.' for c in range(min_col, max_col + 1)]
        print(''.join(row))

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    paths = list(map(mogrify, lines))
    grid = fill_grid(paths)
    #plot_grid(grid)

    g = set(grid)
    print('part 1:', part1(g))
    #plot_grid(g)

    g = set(grid)
    print('part 2:', part2(g))
    #plot_grid(g)

if __name__ == '__main__':
    main()
