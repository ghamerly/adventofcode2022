#!/usr/bin/env python3

# https://adventofcode.com/2022/day/2 - "Rock Paper Scissors"
# Author: Greg Hamerly

import sys

def part1(moves, compete):
    strategy = {
            'X': 'A',
            'Y': 'B',
            'Z': 'C'
            }

    score = 0
    for opponent, self in map(str.split, moves):
        self_move = strategy[self]
        score += compete(opponent, self_move)

    return score

def part2(moves, compete):
    lose = {
            'A': 'C', # rock beats scissors
            'B': 'A', # paper beats rock
            'C': 'B'  # scissors beats paper
            }

    win = {
            'C': 'A', # rock beats scissors
            'A': 'B', # paper beats rock
            'B': 'C'  # scissors beats paper
            }

    draw = { 'A': 'A', 'B': 'B', 'C': 'C' }

    strategy = {
            'X': lose,
            'Y': draw,
            'Z': win
            }

    score = 0
    for opponent, self in map(str.split, moves):
        self_move = strategy[self][opponent]
        score += compete(opponent, self_move)

    return score

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = list(map(str.strip, f))

    def compete(o, s):
        score = { 'A': 1, 'B': 2, 'C': 3 }

        result = score[s]

        wins = {
                ('C', 'A'), # scissors beaten by rock
                ('A', 'B'), # rock beaten by paper
                ('B', 'C')  # paper beaten by scissors
                }

        if o == s:
            result += 3

        elif (o, s) in wins:
            result += 6

        return result

    print('part 1:', part1(lines, compete))
    print('part 2:', part2(lines, compete))

if __name__ == '__main__':
    main()
