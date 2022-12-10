#!/usr/bin/env python3

# https://adventofcode.com/2022/day/10 - "Cathode-Ray Tube"
# Author: Greg Hamerly

import sys

def get_cycle_values(data):
    register = 1
    cycle = 0

    cycle_values = {cycle: register}
    for cmd in data:
        if cmd == 'noop':
            if cycle not in cycle_values:
                cycle_values[cycle] = register
            cycle += 1
            cycle_values[cycle] = register
        else:
            for c in [cycle+1, cycle+2]:
                cycle_values[c] = register
            cycle += 2
            register += int(cmd.split()[1])

    assert set(range(cycle+1)) == set(cycle_values), (set(range(cycle+1))^set(cycle_values))

    return cycle_values

def part1(cycle_values):
    return sum([k * cycle_values[k] for k in [20, 60, 100, 140, 180, 220]])

def part2(cycle_values):
    crt = ['.'] * 240

    for c in cycle_values:
        if c == 0:
            continue
        # these next two lines of code were perhaps the most fiddly
        if abs(((c-1) % 40) - cycle_values[c]) <= 1:
            crt[c-1] = '#'

    for i in range(0, 240, 40):
        print(''.join(crt[i:i+40]))

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    cycle_values = get_cycle_values(lines)

    print('part 1:', part1(cycle_values))
    print('part 2:', part2(cycle_values))

if __name__ == '__main__':
    main()
