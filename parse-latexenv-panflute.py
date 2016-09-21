#!/usr/bin/env python3

"""
Pandoc filter to (recursively) parse the content of certain
user-specified environments.
"""

import sys
import re
import panflute as pf

TO_CONVERT = ['columns']
# @TODO tighten regex for environment names.
# I'm assuming pandoc has stripped the leading/trailing newlines and
# the first/last are the begin/end environment (pretty sure that's how it works)
pattern = re.compile(r"""\A\\begin\{(.*)\}(.*)\\end\{\1\}\Z""", re.DOTALL)


def parseRawLatexBlock(elem, doc):
    if type(elem) == pf.RawBlock and elem.format == "latex":
        contents = elem.text
        m = pattern.match(contents)
        env = m.group(1)
        if m and env in TO_CONVERT:
            sys.stderr.write('Parsing contents of ' + env + '\n')
            env = '{' + env + '}'
            return ([pf.RawInline(text='\\begin' + env, format='latex')] +
                    pf.convert_text(m.group(2)) +
                    [pf.RawInline(text='\\end' + env, format='latex')])

if __name__ == "__main__":
    pf.toJSONFilter(parseRawLatexBlock)
