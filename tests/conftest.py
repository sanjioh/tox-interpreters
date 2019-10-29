from types import SimpleNamespace

import pytest

from tox_interpreters.hooks import InterpreterSelector


@pytest.fixture
def envconfig():
    return SimpleNamespace(envname='pythonenv')


@pytest.fixture
def selector():
    return InterpreterSelector()
