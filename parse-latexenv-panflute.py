#!/usr/bin/env python3

# panflute requires python 3.2 or later
"""
Pandoc filter to (recursively) parse the content of certain
user-specified environments.
"""

import sys
import os
import re
import panflute as pf

TO_CONVERT = ['columns', 'block']
# @TODO tighten regex for environment names.
# I'm assuming pandoc has stripped the leading/trailing newlines and
# the first/last are the begin/end environment (pretty sure that's how it works)
# Also want regex to gobble any [] and {} after the begin.
# Need to check valid syntax.
pattern = re.compile(r"""\A\\begin\{(.*)\}(.*)\\end\{\1\}\Z""", re.DOTALL)


def parseRawLatexBlock(elem, doc):
    if type(elem) == pf.RawBlock and elem.format == "latex":
        contents = elem.text
        m = pattern.match(contents)
        if m and m.group(1) in TO_CONVERT:
            env = '{' + m.group(1) + '}'
            #sys.stderr.write('Parsing contents of ' + env + '\n')

            # Ideally we will run pandoc with all the filters that were invoked
            # originally. But panflute does not know that.
            # Perhaps if parse-latexenv-panflute runs *first* then the other
            #  filters will be fine to run after? If it passes JSON output
            #  to the next filter I think we will be fine, but if it passes
            #  (say) LaTeX then we won't.

            #  I need to apply pandoc to the contents with this filter.
            return ([pf.RawBlock(text='\\begin' + env, format='latex')] +
                    pf.convert_text(m.group(2), extra_args=['--filter={}'.format(os.path.realpath(__file__))]) +
                    [pf.RawBlock(text='\\end' + env, format='latex')])

             # This is OK, *but* any arguments to the begin{} are dropped.
             # So \begin{block}{Title} --> \begin{block} and a *literal* {Title}
             # So perhaps I automatically gobble up any [] {} after the begin
             #  and if you don't want it gobbled you'll just have to put a space
             #  in between (what does LaTeX do about this sort of thing anyway?)

if __name__ == "__main__":
    pf.toJSONFilter(parseRawLatexBlock)
