#!/usr/bin/env python3

import sys
import os
import writers

    
def print_help():
    print('Usage: catline file [ a:b | a b ]')

    
def print_line(writer, linenum):
    # fname is not used, but could be used in different implementations.
    line = writer.format_line(linenum) or ''
    print(' {}'.format(linenum).ljust(7), '|', line)


def catline(writer, fname, start, end):
    if not os.path.isfile(fname):
        print('Error: {} is not recognized as a file'.format(fname))
        return
    writer.init_writer()
    for i in range(writer.start, writer.end):
        print_line(writer, i)


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
    writer = writers.FastPygmentWrapper(fname, start, end)
    catline(writer, fname, start, end)

    
def main():
    if len(sys.argv) == 4 or len(sys.argv) == 3 or len(sys.argv) == 2:
        catline_args(*sys.argv[1:])
    else:
        print_help()

        
if __name__ == '__main__':
    main()
