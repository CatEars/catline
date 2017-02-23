from pygments import lexers, formatters, highlight, styles

# useless comment

def iter_lines(fname, start, end):
    with open(fname, 'r') as f:
        for idx, line in enumerate(f):
            if end != -1 and end <= idx:
                break
            if start <= idx:
                yield line
    
class NormalWriter: # Base class / interface

    def __init__(self, fname, start, end):
        self._start = start
        self._end = end
        self.fname = fname
        self.lines = []

    def init_writer(self):
        self.lines = list(x.rstrip() for x in iter_lines(self.fname, self._start, self._end))

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
        return self._start + len(self.lines) - 1
                
# A class for wrapping the functionality requested from pygments
class PygmentWrapper:

    def __init__(self, fname, start, end):
        self._start = start
        self._end = end
        self.fname = fname

    def get_lexer(self):
        return lexers.get_lexer_for_filename(self.fname)
        
    def init_writer(self):
        self.lexer = self.get_lexer()
        self.formatter = formatters.get_formatter_by_name('terminal')
        self.lines = "".join(iter_lines(self.fname, 0, -1))
        self.lines = highlight(self.lines, self.lexer, self.formatter).split('\n')

        # Make sure that self._end and self._start are valid
        if self._end == -1:
            self._end = len(self.lines)
        else:
            self._end = min(self._end, len(self.lines))
        self._start = min(self._start, len(self.lines))
        
    def format_line(self, linenum):
        if 0 <= linenum < len(self.lines):
            return self.lines[linenum]
        return None

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        if self._end == -1:
            return len(self.lines)
        else:
            return self._end


### Matchers for fast pygment wrapper ###

def match_py(fname):
    return lexers.get_lexer_by_name('python') if fname.endswith('.py') else None

def match_cpp(fname):
    m = fname.endswith
    if m('.cpp') or m('hpp') or m('.cc') or m('hh') or \
       m('.cxx') or m('.hxx') or m('.c++') or m('.h++') or \
       m('.c') or m('.h'): # Also add c
        return lexers.get_lexer_by_name('c++')
    return None

def match_java(fname):
    return lexers.get_lexer_by_name('java') if fname.endswith('.java') else None

class FastPygmentWrapper(PygmentWrapper):
    """Doesn't do any fancy matching, just uses the most common of languages
    with their most common fileendings."""

    MATCHERS = [match_py, match_cpp, match_java]

    def get_lexer(self):
        for matcher in FastPygmentWrapper.MATCHERS:
            if matcher(self.fname):
                return matcher(self.fname)
        return lexers.TextLexer()
