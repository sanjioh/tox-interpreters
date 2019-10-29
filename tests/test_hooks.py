from tox_interpreters.hooks import tox_get_python_executable


def test_python_executable_found(envconfig):
    interpreter = '/path/to/python'
    envconfig.interpreter = interpreter
    assert tox_get_python_executable(envconfig) == interpreter


def test_python_executable_not_found(envconfig):
    envconfig.interpreter = None
    assert tox_get_python_executable(envconfig) is None
