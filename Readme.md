# Parse content within LaTeX environments with Pandoc

**Status:** sort of working (panflute version). But it is mixing up the last `\end{block}` and `\end{columns}` in the example. Unsure if it's a pandoc thing or a regex thing. Need to check.

TLDR: you specify particular LaTeX environments, and pandoc will parse the contents of those environments (recursively).

So e.g. if you specify `columns`, anything between `\begin{columns}` and `\end{columns}` will be parsed by pandoc again. The usual pandoc rules will apply from there downwards, so if you have e.g. content in `\begin{block}` and `\end{block}` within your `columns` environment, it will not be parsed as per the usual `raw_latex` pandoc extension.

So you could specify e.g. `columns`, `block` which would let you parse the contents of columns, of blocks, and of these things nested in each other (but not of other environments).

Considering panflute because it's easier for me to learn.

* Panflute user guide: http://scorreia.com/software/panflute/guide.html

~~~
pandoc example.md -t beamer --filter ./parse-latexenv-panflute.py # i think using python2 not python3
pandoc example.md -t json | ./parse-latexenv-panflute.py | -t beamer
~~~

## The problem

You love writing markdown in pandoc and then compiling it with LaTeX with latex or beamer. It's awesome. You don't have to remember to type `\emph{foobar}` but can instead type `*foobar*`. You've gotten used to writing lists the obvious way.

But then say you go to make a beamer document say, and you do:

~~~
## Literature

We begin with a statement.
TODO: we should make a better example.

\begin{block}
I do not like green eggs and ham.
\end{block}

And then a re-iteration.

\begin{alertblock}
**I do not like them, Sam I Am!**
\end{alertblock}

Let's discuss this.
~~~

Then your LaTeX comes out all funny, because the bold in the second block wasn't parsed (and you couldn't use the standard 'headings level 3 and under become blocks' because the in-between text would also be part of a block, hence you had to use an explicit `\begin{block}` and `\end{block}`).

This is because pandoc will not parse the contents of LaTeX blocks. Makes sense.
But since so much of beamer documents are written in environments (e.g. columns) you end up having to write in pure LaTeX anyway, which defeats the purpose of using pandoc.

Given that the column environment is also used often in beamer (especially beamerposter), you end up writing your whole document in pure LaTeX and skip all the convenience that pandoc poses.

## A solution

Solution 1: a filter where you specify LaTeX environments to be parsed (e.g. `block`) and everything inside that will be run through pandoc as if it were normal pandoc input. The markup is as above.

Pros:

* can configure specifically which environments to parse. So for example if you had a `verbatim` environment in your `block` environment and only specified that the `block` environment should be parsed, then the `verbatim` contents will be left as-is.

Cons:

* you still have to write `\begin{block}` and `\end{block}`, but it is unsurprising that you would need to revert to pure TeX for more complicated stuff anyway (columns, ...).

### Implementation

OK, so I need something to detect `RawLatex` blocks and check if the environment is in our list.
If not, then keep it as is.

If it is, strip out the begin and end (which are the first and last lines, I'm quite sure that the parser will have checked that already).

Then you need to take the contents and recursively run pandoc through them again.

I tried Haskell but it's too hard. I'm much more familiar with Python.


## Another solution

You write all your environments as code blocks and specify the environment as a class attribute.
A filter converts them all to the appropriate environment.

~~~
## Literature

We begin with a statement.

~~~ {.block}
I do not like green eggs and ham.
~~~

And then a re-iteration.

~~~ {.alertblock}
**I do not like them, Sam I Am!**
~~~

Let's discuss this.
~~~

Pros:

* there are heaps of example plugins I can copy off that do something similar already

Cons:

* my editor won't do nice syntax highlighting of the contents
* **nested code blocks don't work.** This is a dealbreaker. Let's stop there.

An adjustment would be that the user uses `<div class="alertblock">` instead of the fenced code blocks, and the [theorem example filter](https://github.com/jgm/pandocfilters/blob/master/examples/theorem.py) handles this marvellously. But typing that is longer than typing the TeX!

## Snippets

* detecting and regex-searching a RawBlock: https://github.com/jgm/pandocfilters/blob/master/examples/comments.py
* all emphasized text to be displayed in all caps: https://github.com/jgm/pandocfilters/blob/master/examples/deemph.py  I **think** this could be an example of walking recursively down the tree?
* converts all `<div class="theorem">` to latex theorem. **Q** by the time this plugin gets to it, are the contents parsed already? https://github.com/jgm/pandocfilters/blob/master/examples/theorem.py  **A** yes.
* the tikz.py shows how to detect latex blocks.
