from unittest import mock

from tox import reporter

from tox_interpreters.hooks import tox_addoption, tox_get_python_executable


def test_config_option():
    parser = mock.Mock()
    tox_addoption(parser)
    assert parser.add_testenv_attribute.call_count == 1


def test_python_executable_found(capfd, envconfig):
    interpreter = '/path/to/python'
    envconfig.interpreter = interpreter
    reporter._INSTANCE._reset()  # pick up pytest monkeypatching of stdout
    assert tox_get_python_executable(envconfig) == interpreter
    captured = capfd.readouterr()
    assert 'pythonenv base interpreter: /path/to/python' in captured.out


def test_python_executable_not_found(capfd, envconfig):
    envconfig.interpreter = None
    reporter._INSTANCE._reset()  # pick up pytest monkeypatching of stdout
    assert tox_get_python_executable(envconfig) is None
    captured = capfd.readouterr()
    assert (
        'pythonenv base interpreter: delegating to standard resolution'
        in captured.out
    )
