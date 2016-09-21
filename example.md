# My slide show

## Slide one

Blah blah blah blah blah blah blah.

\begin{columns}
\column{.5\textwidth}
\begin{columns}
\column{.9\textwidth}
This *should* be parsed.
\end{columns}
\begin{block}{A statement of dislike}
Consider the following quote:

> I do not like green eggs and ham!  
> I **do not like them**, Sam-I-am!
\end{block}

The above is markdown in an `\begin{block}`/`\end{block}` environment.
It should set the quote as a quote, on two lines (there is a double-space at the end of the first quote), with the appropriate words in bold. All in a block.


\column{.5\textwidth}

The below is a specification of a block by using a third-level header. The beamer output should convert this to a block automatically (as well as emphasize the appropriate words and add a line break. I didn't set this one as a block quote).

### A change of heart
I *do* so like green eggs and ham!  
Thank you! Thank you, Sam-I-am!
\end{columns}
