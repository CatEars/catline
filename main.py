#!/usr/bin/env python3

import sys
import os

from pygments import lexers, formatters, highlight

def iter_lines(fname, start, end):
    with open(fname, 'r') as f:
        for idx, line in enumerate(f):
            if end != -1 and end <= idx:
                break
            if start <= idx:
                yield line.rstrip()

# A class for wrapping the functionality requested from pygments
class PygmentWrapper:

    def __init__(self, fname, start, end):
        self._start = start
        self._end = end
        self.fname = fname

    def init_writer(self):
        self.lexer = lexers.get_lexer_for_filename(self.fname)
        self.formatter = formatters.get_formatter_by_name('terminal')
        self.lines = list(iter_lines(self.fname, self._start, self._end))
        
    def format_line(self, linenum):
        idx = linenum - self._start
        if 0 <= idx < len(self.lines):
            return highlight(self.lines[idx], self.lexer, self.formatter).rstrip()
        return None

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._start + len(self.lines)

def match_py(fname):
    return lexers.get_lexer_by_name('python') if fname.endswith('.py') else None

def match_cpp(fname):
    m = fname.endswith
    if m('.cpp') or m('hpp') or m('.cc') or m('hh') or \
       m('.cxx') or m('.hxx') or m('.c++') or m('.h++'):
        return lexers.get_lexer_by_name('c++')
    return None

def match_java(fname):
    return lexers.get_lexer_by_name('java') if fname.endswith('.java') else None

class FastPygmentWrapper(PygmentWrapper):
    """Doesn't do any fancy matching, just uses the most common of languages
    with their most common fileendings."""

    MATCHERS = [match_py, match_cpp, match_java]
    
    @staticmethod
    def get_lexer_for_filename(fname):
        for matcher in FastPygmentWrapper.MATCHERS:
            if matcher(fname):
                return matcher(fname)
        return lexers.TextLexer()
    
    def init_writer(self):
        self.lexer = FastPygmentWrapper.get_lexer_for_filename(self.fname)
        self.formatter = formatters.get_formatter_by_name('terminal')
        self.lines = list(iter_lines(self.fname, self._start, self._end))
    
class NormalWriter:

    def __init__(self, fname, start, end):
        self._start = start
        self._end = end
        self.fname = fname
        self.lines = []

    def init_writer(self):
        self.lines = list(iter_lines(self.fname, self._start, self._end))

    def format_line(self, linenum):
        idx = linenum - self._start
        if 0 <= idx < len(self.lines):
            return self.lines[idx]
        return None

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._start + len(self.lines)
    
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
    writer = FastPygmentWrapper(fname, start, end)
    catline(writer, fname, start, end)

    
def main():
    if len(sys.argv) == 4 or len(sys.argv) == 3 or len(sys.argv) == 2:
        catline_args(*sys.argv[1:])
    else:
        print_help()

if __name__ == '__main__':
    main()
