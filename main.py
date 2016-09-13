#!/usr/bin/env python3

import sys


def print_help():
    print('Usage: catline file [ a:b | a b ]')

    
def print_line(linenum, fname, content):
    # fname is not used, but could be used in different implementations.
    print(' {}'.format(linenum).ljust(7), '| ', content)


def catline(fname, start, end):
    with open(fname, 'r') as f:
        for idx, line in enumerate(f):
            if end != -1 and end <= idx:
                break
            if start <= idx:
                print_line(idx, fname, line.rstrip())


def find_start_and_end(start, end):
    if isinstance(start, str):
        if ':' in start:
            start, end = start.split(':')
            start, end = int(start), int(end)
        else:
            start = int(start)

    if isinstance(end, str):
        end = int(end)

    return start, end


def catline_args(fname, start=0, end=-1):
    start, end = find_start_and_end(start, end)
    catline(fname, start, end)

    
def main():
    if len(sys.argv) == 4 or len(sys.argv) == 3 or len(sys.argv) == 2:
        catline_args(*sys.argv[1:])
    else:
        print_help()

if __name__ == '__main__':
    main()
