#!/usr/bin/env python3

# https://adventofcode.com/2022/day/18 - "Boiling Boulders"
# Author: Greg Hamerly

import sys

def neighbors(p):
    delta = ((-1,0,0), (1,0,0), (0,-1,0), (0,1,0), (0,0,-1), (0,0,1))
    return [(p[0] + d[0], p[1] + d[1], p[2] + d[2]) for d in delta]

def part1(points):
    '''We know the surface area of all cubes is 6 * num_cubes; then subtract 1
    for each neighbor that is also in the set of points. This is code-golfed quite
    a bit from where I started.'''
    return 6 * len(points) - sum([len(set(neighbors(p)) & points) for p in points])

def part2(points):
    '''Get the surface area of the original points, then flood-fill the outside,
    and get the surface area again. Use the difference, and the known surface
    area of the filled parallelepiped, to compute the answer of the "extra"
    internal surface area.'''

    x_vals = [p[0] for p in points]
    y_vals = [p[1] for p in points]
    z_vals = [p[2] for p in points]

    min_x, max_x = min(x_vals) - 1, max(x_vals) + 1
    min_y, max_y = min(y_vals) - 1, max(y_vals) + 1
    min_z, max_z = min(z_vals) - 1, max(z_vals) + 1

    def in_bounds(p):
        return min_x <= p[0] <= max_x and min_y <= p[1] <= max_y and min_z <= p[2] <= max_z

    # very code-golfed flood fill
    filled_points = set(points)
    q = {(min_x, min_y, min_z)}
    while q:
        q = set(filter(in_bounds, sum(map(neighbors, q), []))) - filled_points
        filled_points.update(q)

    # we know the external surface area of the parallelepiped, since it's a
    # regular rectangle on 6 sides
    filled_external_area = 2 * (
            (max_x-min_x+1) * (max_y-min_y+1) + \
            (max_x-min_x+1) * (max_z-min_z+1) + \
            (max_y-min_y+1) * (max_z-min_z+1))

    # find the surface area (internal and external) of both the original and
    # filled points; use this to give us the answer.
    return part1(points) - (part1(filled_points) - filled_external_area)

def mogrify(line):
    return tuple(map(int, line.split(',')))

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    points = set(map(mogrify, lines))

    print('part 1:', part1(points))
    print('part 2:', part2(points))

if __name__ == '__main__':
    main()
