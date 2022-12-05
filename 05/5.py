#!/usr/bin/env python3

# https://adventofcode.com/2022/day/5 - "Supply Stacks"
# Author: Greg Hamerly

# comments:
# - Initially the parsing looked like it would be tedious, but it was easy.
# - However, I had multiple delays due to language-related failures today:
#   - My template stripped out all leading and trailing spaces, which led to
#     failing at parsing the input at first (since leading spaces are
#     significant). Somehow, this still allowed me to succeed at the first task,
#     which led to confusion and delay when I failed on the second task. This
#     ended up being a red herring while debugging with the sample input (it
#     affected correctness on the sample, but not on the actual input).
#   - The real bug was that I forgot that Python was modifying the stacks I
#     built in part 1, so that in part 2 they were not starting from the correct
#     configuration. That took way longer to remember than it should have. I
#     just had to make a copy of each set of stacks first.
# - Had I started with part 1 on the sample input, perhaps I would not have been
#   as confused when I got part 2 wrong.

import sys

def part1(stacks, commands):
    for num, src, dest in commands:
        for _ in range(num):
            assert stacks[src]
            stacks[dest].append(stacks[src].pop())
    return ''.join([stack[-1] for stack in stacks])

def part2(stacks, commands):
    for num, src, dest in commands:
        assert len(stacks[src]) >= num
        stacks[dest].extend(stacks[src][-num:])
        stacks[src] = stacks[src][:-num]
    return ''.join([stack[-1] for stack in stacks])

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    num_stacks = (len(lines[0]) + 1) // 4
    stacks = [[] for _ in range(num_stacks)]
    i = 0
    for i, line in enumerate(lines):
        # stop when we hit the numbers indicating stack indexes
        if '1' in line:
            break

        for c in range(1, len(line), 4):
            if line[c] != ' ':
                stacks[(c - 1) // 4].append(line[c])

    # what remains after the blank line are the commands
    #commands = lines[i+2:]
    f = lambda line: line.split()
    commands = [(int(p[1]), int(p[3])-1, int(p[5])-1) for p in map(f, lines[i+2:])]

    # the stacks were built upside-down; flip them around
    for i in range(len(stacks)):
        stacks[i] = stacks[i][::-1]

    # gah; this was my biggest mistake
    copy = lambda s: [ss[:] for ss in s]

    print('part 1:', part1(copy(stacks), commands))
    print('part 2:', part2(copy(stacks), commands))

if __name__ == '__main__':
    main()
