import pytest
from src.utils import get_max


def test_get_max():
    assert get_max([1, 2, 3]) == 3


def test_get_max_with_empty_list():
    with pytest.raises(ValueError):
        get_max([])


def test_get_max_with_none():
    with pytest.raises(TypeError):
        get_max(None)


def test_get_max_with_string():
    assert get_max("hello") == "o"
