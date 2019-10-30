"""Plugin hooks."""
import re

import pluggy
from tox import reporter

hookimpl = pluggy.HookimplMarker('tox')


class InterpreterSelector:
    """Select a base interpreter for virtual environment creation."""

    def select(self, testenv_config, value):
        """
        Select a Python interpreter.

        Selection is performed by checking the envname against a list of
        regular expressions provided by the user. Regexes are associated
        to interpreter paths; the path associated to the first matching
        regex will be returned.
        In case of no match, this method returns None.
        In case of invalid configuration, this method raises ValueError.
        """
        for config_line in value:
            regex, path = self._split(config_line)
            self._validate_config(regex, path)
            if re.match(regex, testenv_config.envname):
                return path
        return None

    @staticmethod
    def _split(line, sep='='):
        regex, path = line.split(sep, 1)
        return regex.strip(), path.strip()

    @staticmethod
    def _validate_config(regex, path):
        if not (regex and path):
            raise ValueError('Neither regex nor path are allowed to be empty')


@hookimpl
def tox_addoption(parser):  # noqa: D103
    help_text = (
        'list of <regex>=<path> lines -- the testenv name will be checked '
        'against all the regexes, in order: the first match determines the '
        'Python interpreter that will be used as base Python to create the '
        'virtual environment; in case of no match, the standard interpreter '
        'resolution applies',
    )
    parser.add_testenv_attribute(
        name='interpreter',
        type='line-list',
        default=[],
        help=help_text,
        postprocess=InterpreterSelector().select,
    )


@hookimpl
def tox_get_python_executable(envconfig):  # noqa: D103
    envname = envconfig.envname
    interpreter = envconfig.interpreter
    if interpreter:
        reporter.verbosity0(
            '{} base interpreter: {}'.format(envname, interpreter), bold=True,
        )
    else:
        reporter.verbosity0(
            '{} base interpreter: delegating to standard resolution'.format(
                envname,
            ),
            bold=True,
        )
    return interpreter
