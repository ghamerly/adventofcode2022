#!/usr/bin/env python3

# https://adventofcode.com/2022/day/15 - "Beacon Exclusion Zone"
# Author: Greg Hamerly

# This runs pretty slowly (with python3), but is much better with pypy3.

import re
import sys

def part1(data, y_val):
    '''Count the number of locations that don't contain a beacon along the row
    corresponding to the given y_val.'''

    left = right = None # min/max x values
    beacons = {(bx, by) for bx, by, _, _, _ in data} # make a quick lookup for just beacons
    for bx, by, sx, sy, dist in data:
        l = sx - dist
        r = sx + dist
        left = min(left or l, l)
        right = max(right or r, r)

    # sweep across all possible x values for the given y_val
    ans = 0
    for x in range(left - 1, right + 2):
        if (x, y_val) in beacons:
            continue

        # see if this (x, y) is within the shadow of a sensor-beacon; if so,
        # mark it as an available location
        for bx, by, sx, sy, dist in data:
            if abs(x - sx) + abs(y_val - sy) <= dist:
                ans += 1
                break

    return ans

def part2(data, max_x, max_y):
    # clamp a given value to the range [0, max_x]
    clamp = lambda x: max(0, min(max_x, x))

    # keep track of all possible answers (should be exactly 1 at the end)
    answers = []

    # loop over all y values
    for y in range(0, max_y+1):
        # For this y, compute all the possible x-ranges that are masked out by
        # the beacons. These ranges represent x values we don't need to check,
        # so we can search much faster by skipping large ranges.
        x_ranges = []
        for bx, by, sx, sy, dist in data:
            dy = dist - abs(y - sy)
            if dy >= 0:
                # compute and clamp the manhattan distance that form the range of x
                # values that are masked out for this beacon on this y value
                x_ranges.append([clamp(sx - dy), clamp(sx + dy)])

        # now sort and merge the ranges
        x_ranges.sort()
        merged_x_ranges = [x_ranges[0]]
        for i in range(1, len(x_ranges)):
            if x_ranges[i][0] <= merged_x_ranges[-1][1] + 1:
                # the next range overlaps with the previous one; merge them
                merged_x_ranges[-1][1] = max(merged_x_ranges[-1][1], x_ranges[i][1])
            else:
                # the ranges are disjoint; create a new range
                merged_x_ranges.append(x_ranges[i])

        # now check for gaps between ranges, or at the extreme ends
        for i in range(1, len(merged_x_ranges)):
            for x in range(merged_x_ranges[i-1][1]+1, merged_x_ranges[i][0]):
                answers.append((x, y))
        for x in range(0, merged_x_ranges[0][0]):
            answers.append((x, y))
        for x in range(merged_x_ranges[-1][1] + 1, max_x + 1):
            answers.append((x, y))

    assert len(answers) == 1, answers
    x, y = answers[0]
    return x * 4000000 + y

pattern = re.compile('.*x=(?P<sx>-?[0-9]+), y=(?P<sy>-?[0-9]+):.* x=(?P<bx>-?[0-9]+), y=(?P<by>-?[0-9]+)')
def mogrify(line):
    # pull out the sensor and beacon locations as tuples (bx, by, sx, sy) using
    # the regex above
    bx, by, sx, sy = [int(v) for k, v in sorted(pattern.match(line).groupdict().items())]
    dist = abs(bx - sx) + abs(by - sy)
    return (bx, by, sx, sy, dist)

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    data = list(map(mogrify, lines))

    y_val = 2000000
    max_x = max_y = 4000000

    # just for testing
    if file == 'sample.in':
        y_val = 10
        max_x = max_y = 20

    print('part 1:', part1(data, y_val))
    print('part 2:', part2(data, max_x, max_y))

if __name__ == '__main__':
    main()
