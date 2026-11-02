"""Day 001: Generators. Implement both functions lazily (no building full lists)."""
from collections.abc import Iterable, Iterator
from typing import TypeVar

T = TypeVar("T")


def chunked(items: Iterable[T], size: int) -> Iterator[list[T]]:
    """Yield successive lists of at most `size` items from `items`.

    - The last chunk may be shorter.
    - Works with any iterable, including infinite ones (must be lazy).
    - Empty input yields nothing.
    - Raise ValueError if size < 1 (when iteration starts is fine).

    >>> list(chunked([1, 2, 3, 4, 5], 2))
    [[1, 2], [3, 4], [5]]
    """
    raise NotImplementedError


def running_unique(items: Iterable[T]) -> Iterator[T]:
    """Yield each distinct item the first time it is seen, preserving order.

    Items are hashable. Must be lazy: it should work on an infinite iterable
    when consumed with islice.

    >>> list(running_unique([3, 1, 3, 2, 1]))
    [3, 1, 2]
    """
    raise NotImplementedError
