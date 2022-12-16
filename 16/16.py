#!/usr/bin/env python3

# https://adventofcode.com/2022/day/16 - "Proboscidea Volcanium"
# Author: Greg Hamerly

# After solving this using search (with branch-and-bound for part 2, which takes
# about 15 minutes), I read about the solutions of other people, and realized
# that I completely missed that this was a max-flow problem which can be solved
# using flow algorithms. Bummer. If I get extra time (ha!) I will try to
# implement that solution.

import re
import sys

def floyd_warshall(graph):
    vertices = sorted(list(graph))
    apsp = {u: {v: (1 if v in graph[u] else 1e100) for v in vertices} for u in vertices}

    for w in vertices:
        apsp[w][w] = 0
        for u in vertices:
            for v in vertices:
                apsp[u][v] = min(apsp[u][v], apsp[u][w] + apsp[w][v])

    return apsp

def solve_rec(flow_rates, apsp, open_valves, pos, remaining, partial_total):
    '''Fully naive recursive search. The search space is small enough.'''
    if remaining <= 0:
        return partial_total

    best = partial_total

    for v, travel in apsp[pos].items():
        if v in open_valves:
            continue

        total = (remaining - travel - 1) * flow_rates[v]
        if total > 0:
            open_valves.append(v)
            ans = solve_rec(flow_rates, apsp, open_valves, v, \
                    remaining - travel - 1, partial_total + total)
            open_valves.pop()
            best = max(ans, best)

    return best

def solve_rec2(flow_rates, apsp, available_valves, positions, partial_total, best):
    '''Branch and bound solution. Since the structure of the solution is to
    "alternate" between the two players, bounding the best solution is a little
    tricky. So we construct the upper bound from scratch each time, rather than
    compute it incrementally with each recursion. If we added incremental bound
    updates, it would make things marginally faster.

    Note that positions is a tuple of ((p1, r1), (p2, r2)) where p1 and p2
    represent the position of each player, and r1 and r2 represent the number of
    minutes remaining (respectively).
    '''

    # calculate a naive upper bound on max_remaining -- for each valve that we
    # could still turn on, what's the most we could get out of it?
    max_remaining = 0
    for v in available_valves:
        m = max((r - apsp[p][v] - 1) * flow_rates[v] for p, r in positions)
        if m > 0:
            max_remaining += m

    # bound the search if possible
    if partial_total + max_remaining <= best[0]:
        return

    if best[0] < partial_total:
        print('found new best', best[0])
        best[0] = partial_total

    for i, (p, r) in enumerate(positions):
        if r <= 0:
            continue

        other_position = positions[1 - i]
        for j in range(len(available_valves)):
            v = available_valves[j]

            total = (r - apsp[p][v] - 1) * flow_rates[v]
            if total > 0:
                available_valves[j], available_valves[-1] = available_valves[-1], available_valves[j]
                available_valves.pop()

                next_positions = ((v, r - apsp[p][v] - 1), other_position)
                solve_rec2(flow_rates, apsp, available_valves, next_positions,
                        partial_total + total, best)

                available_valves.append(v)
                available_valves[j], available_valves[-1] = available_valves[-1], available_valves[j]


def part1(flow_rates, apsp, source):
    return solve_rec(flow_rates, apsp, [], source, 30, 0)

def part2(flow_rates, apsp, source):
    best = [0]
    available_valves = list(flow_rates)
    solve_rec2(flow_rates, apsp, available_valves, ((source, 26), (source, 26)), 0, best)
    return best[0]

pattern = re.compile('Valve (?P<src>[A-Z]+) .*=(?P<rate>[0-9]+);.*valves? (?P<dests>(?:[A-Z]+, )*[A-Z]+)')
def mogrify(line):
    m = pattern.match(line)
    assert m, line
    src, rate, dests = m.groups()
    return src, int(rate), dests.split(', ')

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    data = list(map(mogrify, lines))

    graph = {s: set(dests) for s, _, dests in data}

    # remap vertices into range [0,n)
    vertex_map = {s: i for i, s in enumerate(graph)}
    graph = {vertex_map[s]: {vertex_map[d] for d in graph[s]} for s in graph}
    flow_rates = {vertex_map[s]: r for s, r, _ in data}

    # check that the data given had bidirectional connections
    for v in graph:
        for u in graph[v]:
            assert v in graph[u]

    apsp = floyd_warshall(graph)

    # now that we have the travel costs, filter out vertices that have flows of
    # 0, because they are never worth stopping at
    to_keep = [v for v, r in flow_rates.items() if r > 0] + [vertex_map['AA']]
    apsp = {u: {v: apsp[u][v] for v in to_keep} for u in to_keep}
    flow_rates = {v: flow_rates[v] for v in to_keep}

    print('part 1:', part1(flow_rates, apsp, vertex_map['AA']))
    print('part 2:', part2(flow_rates, apsp, vertex_map['AA']))

if __name__ == '__main__':
    main()
