#!/usr/bin/env python

"""
Pandoc filter to (recursively) parse the content of certain
user-specified environments.
"""

import sys
import re
from pandocfilters import toJSONFilter, walk, RawBlock

TO_CONVERT = ['columns']
# @TODO tighten regex for environment names.
pattern = re.compile(r"""\A\\begin\{(.*)\}(.*)\\end\{\1\}\Z""", re.DOTALL)


def parseRawLatexBlock(key, value, format, meta):
    if key == 'RawBlock':
        [fmt, contents] = value
        if fmt == 'latex':
            m = pattern.match(contents)
            if m and m.group(1) in TO_CONVERT:
                sys.stderr.write('Parsing contents of ' + m.group(1) + '\n')
                # I'm assuming pandoc has stripped the leading/trailing newlines and
                # the first/last are the begin/end environment (pretty sure that's how it works)
                # @TODO add in the LaTeX \begin and \end too
                # @UPTO here
                return RawBlock('latex', '\\begin{' + m.group(1) + '}' + m.group(2) + '\\end{' + m.group(1) + '}')
                #return walk(m.group(2), parseRawLatexBlock, format, meta)

if __name__ == "__main__":
    toJSONFilter(parseRawLatexBlock)
