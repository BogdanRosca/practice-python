from itertools import count, islice

import pytest

from exercise import chunked, running_unique


def test_chunked_basic():
    assert list(chunked([1, 2, 3, 4, 5], 2)) == [[1, 2], [3, 4], [5]]


def test_chunked_exact_multiple():
    assert list(chunked(range(6), 3)) == [[0, 1, 2], [3, 4, 5]]


def test_chunked_empty():
    assert list(chunked([], 3)) == []


def test_chunked_size_larger_than_input():
    assert list(chunked("ab", 10)) == [["a", "b"]]


def test_chunked_invalid_size():
    with pytest.raises(ValueError):
        list(chunked([1, 2], 0))


def test_chunked_is_lazy_on_infinite():
    first = list(islice(chunked(count(), 3), 2))
    assert first == [[0, 1, 2], [3, 4, 5]]


def test_chunked_returns_iterator():
    g = chunked([1, 2, 3], 2)
    assert iter(g) is g


def test_running_unique_basic():
    assert list(running_unique([3, 1, 3, 2, 1])) == [3, 1, 2]


def test_running_unique_empty():
    assert list(running_unique([])) == []


def test_running_unique_lazy_on_infinite():
    src = (i % 3 for i in count())
    assert list(islice(running_unique(src), 3)) == [0, 1, 2]
