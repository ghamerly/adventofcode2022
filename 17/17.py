#!/usr/bin/env python3

# https://adventofcode.com/2022/day/17 - "Pyroclastic Flow"
# Author: Greg Hamerly

import sys

PIECES = \
'''####

.#.
###
.#.

..#
..#
###

#
#
#
#

##
##'''

class Piece:
    def __init__(self, p):
        self.p = set(p)
        # (r, c) represents the top left position
        self.r = self.c = 0
        rows = [r for r, c in self.p]
        cols = [c for r, c in self.p]
        assert rows and cols, (rows, cols, p)
        assert 0 == min(rows) == min(cols), (rows, cols)
        # pre-compute the right and bottom edges
        self.right_edge = max(cols)
        self.bottom_edge = max(rows)

    def __repr__(self):
        return f'p={self.p}, rc={self.r, self.c}'

    def render_into(self, grid, char='#'):
        for r, c in self.p:
            grid[(r + self.r, c + self.c)] = char

    def erase_from(self, grid):
        for r, c in self.p:
            del grid[(r + self.r, c + self.c)]

    def left(self):   return self.c
    def right(self):  return self.c + self.right_edge
    def top(self):    return self.r
    def bottom(self): return self.r + self.bottom_edge

    def in_grid(self, dr, dc, grid):
        for r, c in self.p:
            if (self.r + r + dr, self.c + c + dc) in grid:
                return True
        return False

    def move_lr(self, direction, grid):
        if direction == '>':
            if self.right() < 6 and not self.in_grid(0, 1, grid):
                self.c += 1
                return True
        elif self.left() > 0 and not self.in_grid(0, -1, grid):
            self.c -= 1
            return True
        return False

    def move_down(self, grid):
        if self.bottom() + 1 >= 0 or self.in_grid(1, 0, grid):
            return False

        self.r += 1
        return True

    def copy_shape(self): return Piece(self.p)

def draw_grid(grid, replacement=None):
    min_r, max_r = min([r for r, c in grid]), max([r for r, c in grid])
    min_c, max_c = min([c for r, c in grid]), max([c for r, c in grid])

    if replacement is None:
        f = lambda c: '.' if c is None else c
    else:
        f = lambda c: '.' if c is None else replacement

    for r in range(min_r, max_r + 1):
        row = [f(grid.get((r, c))) for c in range(0, 7)]
        print('|' + ''.join(row) + '|')
    print('+-------+')

def get_pieces():
    global PIECES

    pieces = [set()]
    r = 0
    for line in PIECES.split('\n'):
        if not line:
            pieces.append(set())
            r = 0
        else:
            for c, char in enumerate(line):
                if char == '#':
                    pieces[-1].add((r, c))
            r += 1
    
    return list(map(Piece, pieces))

def simulate(pieces, directions, steps):
    grid = {}
    max_top = -1
    direction_ndx = 0
    heights = []

    chars = '0123456789'

    for i in range(steps):
        piece = pieces[i % len(pieces)].copy_shape()

        # Starting positions according to the rules: 2 units from the left wall,
        # 3 above the top of the highest piece. Note that we are using reversed
        # coordinates in the vertical direction, so we progress from negative
        # numbers towards 0 as we "drop".
        piece.r = max_top - (piece.bottom() - piece.top()) - 3
        piece.c = 2

        #print(f'piece {i}: {piece}')

       #piece.render_into(grid)
       #draw_grid(grid)
       #piece.erase_from(grid)

        iteration = 0
        while True:
            iteration += 1
            d = directions[direction_ndx % len(directions)]
            piece.move_lr(d, grid)
            direction_ndx += 1 

            if not piece.move_down(grid):
                max_top = min(max_top, piece.top() - 1)
                heights.append(-max_top-1)
                #print(f'max_top = {max_top}')
                piece.render_into(grid, chars[i % len(chars)])
                break

    return heights

def part1(pieces, directions):
    heights = simulate(pieces, directions, 2022)
    return heights[-1]

def part2(pieces, directions):
    '''This feels pretty hacky with all these constants. The basic idea is:
    - simulate for a long enough time to get to a repeating pattern
    - identify how long the pattern is
    - use modular arithmetic to find out an even way to divide the majority of
      the tower by the pattern so we can find the height of the top portion, and
      add in the remaining base height.
    
    Because I hate the constants so much, I am naming them, to my shame.

    These things could be generalized, but it's not worth it at this point.'''

    np = len(pieces)

    BAD_CONSTANT_SIMULATION_ROUNDS = 20000
    BAD_CONSTANT_BUFFER_ROUNDS = 1000
    BAD_CONSTANT_MAX_SKIP = 1000
    BAD_CONSTANT_PATTERN_ROUNDS = 10

    heights = simulate(pieces, directions, BAD_CONSTANT_SIMULATION_ROUNDS * np)
    buffer = np * BAD_CONSTANT_BUFFER_ROUNDS

    # look for a value "skip" where every skip rounds (of all 5 pieces) gives
    # the same height difference
    for skip in range(1, BAD_CONSTANT_MAX_SKIP):
        start = buffer + skip * np
        vals = {heights[i] - heights[i - skip * np] for i in range(start, len(heights))}
        if len(vals) == 1:
            break

    skip_blocks = skip * np
    skip_height = heights[buffer] - heights[buffer - skip_blocks]

    # find a starting point s, where s is within the range of the repeating
    # pattern, and (1000000000000 - s) % skip_blocks == 0, so that we can just
    # apply the repeating pattern for the remainder.

    n = 1000000000000
    remainder = n % skip_blocks
    s = skip_blocks * BAD_CONSTANT_PATTERN_ROUNDS + remainder
    remaining_pieces = n - s
    assert remaining_pieces % skip_blocks == 0

    # sanity check -- make sure we're actually in the repeating region
    for i in range(s, s + 1000):
        assert heights[i] - heights[i - skip_blocks] == skip_height

    base_height = heights[s-1]
    repeating_height = (remaining_pieces // skip_blocks) * skip_height

    return base_height + repeating_height

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    pieces = get_pieces()
    directions = lines[0]

    print('part 1:', part1(pieces, directions))
    print('part 2:', part2(pieces, directions))

if __name__ == '__main__':
    main()
