#!/usr/bin/env python3

# https://adventofcode.com/2022/day/9 - "Rope Bridge"
# Author: Greg Hamerly

import sys

def display(positions, context=None):
    '''Display the positions given, along with the given context. The context is
    so that the background field doesn't repeatedly shrink and grow.'''

    context = context or set()
    min_r = min([r for r, c in positions | context])
    max_r = max([r for r, c in positions | context])
    min_c = min([c for r, c in positions | context])
    max_c = max([c for r, c in positions | context])

    def get_char(r, c):
        if (r, c) in positions:
            return '#'
        if (r, c) == (0, 0):
            return 's'
        return '.'

    out = [ [get_char(r, c) for c in range(min_c, max_c + 1)] for r in range(min_r, max_r + 1) ]

    for row in out:
        print(''.join(row))

def part1(data):
    head = (0, 0)
    tail = (0, 0)

    tail_positions = {tail}
    all_positions = {tail}

    for (dr, dc), length in data:
        for i in range(length):
            new_head = (head[0] + dr, head[1] + dc)

            dist_r = abs(new_head[0] - tail[0])
            dist_c = abs(new_head[1] - tail[1])

            assert dist_r <= 3 and dist_c <= 3 and dist_r + dist_c <= 3, (dist_r, dist_c, head, new_head, tail)

            if dist_r >= 2 or dist_c >= 2:
                # for part 1, moving "diagonally" is always going to just put
                # the tail where the head just was (since the head cannot move
                # diagonally itself). Also, we are not making a copy since we're
                # about to replace the head.
                tail = head

            head = new_head

            tail_positions.add(tail)
            all_positions.add(head)
            all_positions.add(tail)

    #display(tail_positions, all_positions)

    return len(tail_positions)

def move_knots(knots, index):
    '''Given the new position of up to knots[index], figure out what to do about
    knots[index+1] recursively.'''

    # base case (last knot)
    if index + 1 == len(knots):
        return

    dist_r = abs(knots[index][0] - knots[index+1][0])
    dist_c = abs(knots[index][1] - knots[index+1][1])

    assert dist_r <= 2 and dist_c <= 2 and dist_r + dist_c <= 4, (dist_r, dist_c, knots, index)

    new_knot = knots[index+1][:]
    if dist_r >= 2 or dist_c >= 2: # they are not touching
        # Rather than use a bunch of logic, if two subesquent knots are not
        # touching, then search for the closest location that is within the 3x3
        # box centered on (r,c).
        (r, c) = knots[index+1]
        best_dist = 100

        for nr in range(r-1, r+2):
            for nc in range(c-1, c+2):
                dist = abs(nr - knots[index][0]) + abs(nc - knots[index][1])
                if dist < best_dist:
                    best_dist = dist
                    new_knot = (nr, nc)

    # update and recurse, if needed
    if knots[index+1] != new_knot:
        knots[index+1] = new_knot
        move_knots(knots, index + 1)

def part2(data):
    knots = [(0, 0)] * 10
    tail_positions = {(0, 0)}
    all_positions = {(0, 0)}

    for (dr, dc), length in data:
        for i in range(length):
            knots[0] = (knots[0][0] + dr, knots[0][1] + dc)
            move_knots(knots, 0)
            tail_positions.add(knots[-1])
            all_positions.update(knots)

    #display(tail_positions, all_positions)

    return len(tail_positions)


def mogrify(line):
    delta = {
            'D': ( 1,  0),
            'U': (-1,  0),
            'L': ( 0, -1),
            'R': ( 0,  1)
            }
    direction, length = line.split()
    return delta[direction], int(length)

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
