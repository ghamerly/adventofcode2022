#!/usr/bin/env python3

# https://adventofcode.com/2022/day/11 - "Monkey in the Middle"
# Author: Greg Hamerly

import collections
import sys

def part1(monkeys):
    '''For this part, the divisor is 3, which keeps all the values easily within
    a reasonable range. Also, we only run for 20 rounds.'''
    for r in range(20):
        for m in monkeys:
            m.round(monkeys, 3)

    inspections = sorted([m.num_inspections for m in monkeys])
    return inspections[-1] * inspections[-2]

def part2(monkeys):
    '''For this part, the divisor is 1 (not 3), so we use a modulus of all of
    the test divisors to keep us in a sane integer range. All of the test
    divisors happen to be prime numbers, but I don't believe that matters. There
    aren't too many monkeys, so the modulus is fairly small.

    This modulus trick works because we need to know the answer to the question
    "is x divisible by y", but we can replace x with (x % m), so long as it
    gives the same answer. And if m is the product of all the possible y values
    (test divisors), then it is like asking "is (x % y) divisible by y", which
    does give the same answer. This is an oversimplification, but explaining
    modular arithemtic at 1AM is not easy for me.'''

    modulus = 1
    for m in monkeys:
        modulus *= m.divisor

    # for comparing on the sample data
    #keyframes = [1, 20] + [i * 1000 for i in range(1, 11)]

    for r in range(10000):
        for m in monkeys:
            m.round(monkeys, 1, modulus)
       #if (r + 1) in keyframes:
       #    print(f'{r+1}: {[m.num_inspections for m in monkeys]}')

    inspections = sorted([m.num_inspections for m in monkeys])
    return inspections[-1] * inspections[-2]

class Monkey:
    def __init__(self, lines):
        self.id = int(lines[0].split()[1].rstrip(':'))
        self.items = collections.deque([int(x.rstrip(',')) for x in lines[1].split()[2:]])
        # use eval to turn the given statement into a function
        self.operation = eval('lambda old: ' + ' '.join(lines[2].split()[-3:]))
        self.divisor = int(lines[3].split()[-1])
        self.true_dest = int(lines[4].split()[-1])
        self.false_dest = int(lines[5].split()[-1])
        self.num_inspections = 0
        #print(vars(self))

    def round(self, monkeys, divisor, modulus=None):
        while self.items:
            self.num_inspections += 1
            new = self.operation(self.items.popleft()) // divisor
            if modulus:
                new = new % modulus
            dest = self.false_dest if new % self.divisor else self.true_dest
            monkeys[dest].items.append(new)
            #print(f'monkey {self.id} has item {old} => {new}, thrown to {dest}')

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    monkeys_1 = []
    monkeys_2 = []
    for i in range(0, len(lines), 7):
        monkeys_1.append(Monkey(lines[i:i+7]))
        monkeys_2.append(Monkey(lines[i:i+7]))

    print('part 1:', part1(monkeys_1))
    print('part 2:', part2(monkeys_2))

if __name__ == '__main__':
    main()
