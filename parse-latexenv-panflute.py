#!/usr/bin/env python3

# panflute requires python 3.2 or later
"""
Pandoc filter to (recursively) parse the content of certain
user-specified environments.
"""

import sys
import re
import panflute as pf

TO_CONVERT = ['columns', 'block']
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
            # this works but I want the Tex to be inline not block because it
            #  keeps putting stuff in its own paragraph
            # (if you try to + a RawInline it complains about expecting a block)
            # Also, pf.convert_text appears not to apply this filter.
            #  I need to apply the filter again to the text for nested environments.
            return ([pf.RawBlock(text='\\begin' + env, format='latex')] +
                    pf.convert_text(m.group(2)) +
                    [pf.RawBlock(text='\\end' + env, format='latex')])

if __name__ == "__main__":
    pf.toJSONFilter(parseRawLatexBlock)
