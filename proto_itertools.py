"""
Itertools functions module
"""

from typing import Iterator, Optional, Generator, TypeVar, Tuple


item = TypeVar("item")


def count(start:int = 0, step: Optional[int] = None) -> Iterator[int]:
    """
    Return an infinite iterator with start and step

    Args:
        start: int, the start of the infinite stream
        step: Optional[int], the step betwwen iterates

    Return:
        Iterator[int] - an infinite stream

    """
    step = 1 if step is None else step
    i = 0
    while True:
        yield start + step * i
        i += 1


def cycle(value: Iterator[item])-> Iterator[item]:
    """
    Cycle the value infinitely

    Args:
        value: Iterator, list of values to repeat

    Returns:
        Iterator: an infinite stream of values from value
    """
    while True:
        yield from value


def repeat(value: item) -> Iterator[item]:
    """
    Cycle the value infinitely

    Args:
        value: value to repeat

    Returns:
        Iterator: an infinite stream of value
    """
    while True:
        yield value

def product(*iterates: Iterator[Iterator[item]]) -> Iterator[Tuple[item]]:
    """
    Returns a cartesian product of list

    Args:
        iterables: Iterator[Iterator[item]] - an iterator of iterators to get the cartesian

    Returns:
        Iterator[Tuple[item]] - an iterator of all combinations of items
    """
    iters = [tuple(iterate) for iterate in iterates]
    prods = [[]]
    for iterate in iters:
        prods = [x + [y] for x in prods for y in iterate]

    for iterate in prods:
        yield iterate

def permutations(iterable: Iterator[item], r:Optional[int] = None) -> Iterator[Tuple[item]]:
    """
    Get permutations of iterable

    Args:
        iterable: iterator of elements to be permuted
        items: permutations length

    Returns:
        Iterator[Tuple[item]] - all possible permutations
    """
    length = len(iterable)
    items = length if r is None or r > length else r
    item_indices = [
            indices 
            for indices in product(*([list(range(length))]*items))
            if len(set(indices)) == items]
    for indices in item_indices:
        yield tuple(iterable[i] for i in indices)

def combinations(r: int, n: int) -> Iterator[Tuple[int]]:
    """
    Get combinations of iterable

    Args:
        iterable: iterator of elements to be permuted
        items: permutations length

    Returns:
        Iterator[Tuple[int]] - all possible combinations
    """
    r = min(r, n)
    lst = list(range(1, r+1))
    yield tuple(lst)
    while lst[0] <= n - r:
        i = r - 1
        while lst[i] == n - r + i:
            i -= 1
        lst[i:] = list(range(lst[i-1]+1, lst[i-1] + r - i))
        yield tuple(lst)

def combinations_with_replacement(r:int, n: int) -> Iterator[Tuple[int]]:
    """
    Get combinations of iterable, with replacements

    Args:
        iterable: iterator of elements to be permuted
        items: permutations length

    Returns:
        Iterator[Tuple[int]] - all possible combinations
    """
    r = min(r, n)
    lst = [1] * r
    yield tuple(lst)
    while lst[0] != n:
        i = r - 1
        while  i > 0 and lst[i] == n:
            i -= 1
        lst[i:] = [lst[i] + 1] * (r - i)
        yield tuple(lst)
