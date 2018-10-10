# Fortune

## Introduction

`fortune` is a stripped-down implementation of the classic BSD Unix
`fortune` command. It combines the capabilities of the `strfile` command
(which produces the fortune index file) and the `fortune` command (which
displays a random fortune). It reads the traditional `fortune` program's
text file format.

This repository contains a *fortune cookie database*. It contains more than
2,800 quotes collected by Brian M. Clapper since about 1990 or so.


## Usage

When used as a command line tool:

    Usage: fortune [OPTIONS] [fortune_files ...]

    Options:
    -h, --help     show this help message and exit
    -v, --verbose  when updating the index file, emit verbose messages
    -u, --update   update the index file, instead of printing a fortune.
    -V, --version  show version and exit.
    -n NUM         number of fortune cookies to show

If you omit the fortune files/paths, `fortune` looks at the `FORTUNE_FILE`
environment variable. If that environment variable isn't set, `fortune`
looks in `/usr/local/share/games/fortunes`, otherwise, it aborts.

When used as a Python library:

```python
from fortune import Fortune
generator = Fortune('/path/to/fortunes')
print(generator())
```


## Fortune Cookie File Format

A fortune cookie file is a text file full of quotes. The format is simple:
The file consists of paragraphs separated by lines containing a single '%'
character. For example:

    A little caution outflanks a large cavalry.
        -- Bismarck
    %
    A little retrospection shows that although many fine, useful software
    systems have been designed by committees and built as part of multipart
    projects, those software systems that have excited passionate fans are
    those that are the products of one or a few designing minds, great
    designers. Consider Unix, APL, Pascal, Modula, the Smalltalk interface,
    even Fortran; and contrast them with Cobol, PL/I, Algol, MVS/370, and
    MS-DOS.
        -- Fred Brooks, Jr.
    %
    A man is not old until regrets take the place of dreams.
        -- John Barrymore


## The Index File

For efficiency and speed, `fortune` uses an index file to store the offsets
and lengths of every fortune in the text fortune file. So, before you can use
`fortune` to read a random fortune, you have to generate the data file. With
the traditional BSD `fortune` program, you used the _strfile_(8) command
to generate the index. With _this_ fortune program, however, you the indexes
are automatically generated in the user's home directory, inside `~/.fortune`.

You should run `fortune -u` whenever you change the text fortune file(s),
so a new index can be generated.


## Generating a Random Fortune

You can generate a random fortune simply by running the `fortune` utility
with the path to your text fortunes file:

```sh
fortune /path/to/fortunes
```


## Differences

This version of `fortune` does not provide some of the more advanced
capabilities of the original BSD program. For instance, it lacks:

- the ability to mark offensive and inoffensive fortunes
- the ability to separate long and short quotes
- the ability to print all fortunes matching a regular expression

It does, however, provide the most important function: The ability to display
a random quote from a set of quotes.


## License and Copyright Info

This is free software, released under the following BSD-like license:

    Copyright (c) 2018 German Mendez Bravo (Kronuz)
    Copyright (c) 2008 Brian M. Clapper

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions are met:

    - Redistributions of source code must retain the above copyright notice,
        this list of conditions and the following disclaimer.

    - The end-user documentation included with the redistribution, if any,
        must include the following acknowlegement:

        This product includes software developed by Brian M. Clapper
        (bmc@clapper.org, http://www.clapper.org/bmc/). That software is
        copyright (c) 2008 Brian M. Clapper.

        Alternately, this acknowlegement may appear in the software itself, if
        and wherever such third-party acknowlegements normally appear.

    THIS SOFTWARE IS PROVIDED AS IS AND ANY EXPRESSED OR IMPLIED WARRANTIES,
    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND
    FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL BRIAN M.
    CLAPPER BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
    CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
    SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
    INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
    CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
    ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
    POSSIBILITY OF SUCH DAMAGE.

This fortune file database is provided under the Creative Commons Attribution
4.0 International License. For details, please see
<http://creativecommons.org/licenses/by/4.0/legalcode>.
