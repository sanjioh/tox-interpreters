# tox-interpreters

[![GitHub Actions](https://github.com/sanjioh/tox-interpreters/workflows/CI/badge.svg)](https://github.com/sanjioh/tox-interpreters/actions)
[![codecov](https://codecov.io/gh/sanjioh/tox-interpreters/branch/master/graph/badge.svg)](https://codecov.io/gh/sanjioh/tox-interpreters)
[![version](https://img.shields.io/pypi/v/tox-interpreters)](https://pypi.org/project/tox-interpreters)
[![python](https://img.shields.io/pypi/pyversions/tox-interpreters)](https://pypi.org/project/tox-interpreters)
[![license](https://img.shields.io/pypi/l/tox-interpreters)](https://pypi.org/project/tox-interpreters)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## What?

`tox-interpreters` enables overriding the logic `tox` follows in
resolving base Python interpreters when it comes to virtual environment
creation.
It does so by allowing the user to bind test env names to the
interpreters of their choice, by means of regular expressions.

## Why?

I usually run `tox` from a permanent and isolated virtual environment,
and I keep Python interpreters in multiple versions installed at the
system level for `tox` itself to use whenever it needs to create a test
environment.

It turns out that if the required Python version for a new environment
matches the one `tox` is running from, `tox` will use its *own* Python
interpreter as base to perform the creation, despite its belonging to a
virtual environment - the system level interpreter will *not* be used.

The standard way of fixing this would be by setting `basepython` to the
absolute path of the interpreter to be used for a specific environment.
Unfortunately this becomes impractical as soon as a generative envlist
with factors is involved.

Of course this is just one of the many possible use cases. Generally
speaking, `tox-interpreters` aims at providing full consistency and
flexibility in virtual environment creation across Python versions, by
allowing the user to choose the base interpreter to be used depending on
the name of the test environment.

## Installation

`tox-interpreters` has been developed as a `tox` plugin, therefore it
has to be installed along with `tox` itself.

```shell
$ pip install tox-interpreters
```

## Usage

To use `tox-interpreters`, add the setting `interpreter` to the
`[testenv]` section of your `tox` configuration file (typically
`tox.ini`), as follows:

```ini
[testenv]
interpreter =
    py37.*=/path/to/python3.7
    py38.*=/path/to/python3.8
```

The `interpreter` setting accepts a list of `<regex>=<interpreter>`
lines as value. Each line binds a regular expression to an interpreter.

Whenever a new test environment needs to be created, the selection of
the base Python interpreter is performed by checking the name of the
environment against all the regular expressions, in order. The
interpreter bound to the first matching regex will be used.

In case of no match, the selection logic falls back to the standard
behaviour of `tox` - that is, everything works just as if
`tox-interpreters` wasn't installed at all.

Interpreters can be specified by their absolute path or just by their
file name. In the latter case, the path to the file needs to be in the
`PATH` environment variable for virtual environment creation to succeed.

```ini
[testenv]
interpreter =
    py37.*=/path/to/python3.7
    py38.*=python3.8
```

## License

See: [LICENSE][1]

[1]: https://github.com/sanjioh/tox-interpreters/blob/master/LICENSE
