import pytest


def test_empty_config(envconfig, selector):
    assert selector.select(envconfig, []) is None


def test_nonmatching_config(envconfig, selector):
    assert selector.select(envconfig, ['env.*=/path/to/python']) is None


def test_matching_config(envconfig, selector):
    assert (
        selector.select(envconfig, ['python.*=/path/to/python'])
        == '/path/to/python'
    )


def test_first_matching_config(envconfig, selector):
    config = [
        'python.*=/path/to/python',
        'pythonen.*=/path/to/other/python',
    ]
    assert selector.select(envconfig, config) == '/path/to/python'


def test_skip_nonmatching_config(envconfig, selector):
    config = [
        'env.*=/path/to/other/python',
        'python.*=/path/to/python',
    ]
    assert selector.select(envconfig, config) == '/path/to/python'


def test_extra_whitespace(envconfig, selector):
    assert (
        selector.select(envconfig, ['python.*    =    /path/to/python'])
        == '/path/to/python'
    )


def test_extra_separators(envconfig, selector):
    assert (
        selector.select(envconfig, ['python.*=/path/t=o/python'])
        == '/path/t=o/python'
    )


def test_error_on_empty_regex(envconfig, selector):
    with pytest.raises(ValueError):
        selector.select(envconfig, ['=/path/to/python'])


def test_error_on_empty_path(envconfig, selector):
    with pytest.raises(ValueError):
        selector.select(envconfig, ['python.*='])
