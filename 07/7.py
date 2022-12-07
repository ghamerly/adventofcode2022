#!/usr/bin/env python3

# https://adventofcode.com/2022/day/7 - "No Space Left On Device"
# Author: Greg Hamerly

import collections
import sys

def fullpath(path):
    return '/' + '/'.join(path)

def total_size(structure, path, directory_sizes):
    '''Recursively find the size of each directory in the structure.'''
    assert path in structure, path

    # total up all subdirectories
    size = sum([total_size(structure, d, directory_sizes) for d in structure[path]['dirs']])
    # add in the files
    size += sum([s for s, filename in structure[path]['files']])
    # record the size of this directory
    directory_sizes.append(size)

    # return the total size
    return size

def find_directory_sizes(lines):
    '''Parse the data (input to the problem) into a dict-based directory
    structure. Then call total_size() to total up the size of all the
    directories, and return that list.'''
    f = lambda: { 'files': [], 'dirs': [] }
    structure = collections.defaultdict(f) # path => list of files / dirs
    path = []
    cwd = ''
    for line in lines:
        if line.startswith('$'):
            parts = line.split()
            cmd = parts[1]
            args = parts[2:]

            if cmd == 'cd':
                if args[0] == '..':
                    path.pop()
                elif args[0] == '/':
                    paths = []
                else:
                    path.append(args[0])
                cwd = fullpath(path)
                structure[cwd] # allocate
            else:
                assert cmd == 'ls'
        else: # this line is not a command; it is the output of an "ls" line
            a, b = line.split()
            if a == 'dir':
                child = fullpath(path + [b])
                structure[child] # allocate
                structure[cwd]['dirs'].append(child)
            else:
                structure[cwd]['files'].append((int(a), b))
        
    directory_sizes = []
    total_size(structure, '/', directory_sizes)
    return directory_sizes

def part1(directory_sizes):
    return sum([d for d in directory_sizes if d <= 100000])

def part2(directory_sizes):
    all_files = max(directory_sizes) # size of all files
    disk_size = 70000000 # given in the problem
    needed = 30000000 # given in the problem
    free = disk_size - all_files
    remaining_needed = needed - free

    # find the smallest directory at least as large as "remaining_needed"
    return min([d for d in directory_sizes if d >= remaining_needed])

def main():
    regular_input = __file__.split('/')[-1][:-len('.py')] + '.in'
    file = regular_input if len(sys.argv) <= 1 else sys.argv[1]
    print(f'using input: {file}')
    with open(file) as f:
        lines = [line.rstrip('\n') for line in f]

    directory_sizes = find_directory_sizes(lines)

    print('part 1:', part1(directory_sizes))
    print('part 2:', part2(directory_sizes))

if __name__ == '__main__':
    main()
