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
    n = len(iterable)
    r = n if r is None or r > n else r
    lst = list(range(n))
    changes = list(range(n, n-r, -1))
    yield tuple(iterable[i] for i in lst[:r])
    while True:
        i = r - 1
        flag = True
        while i >= 0:
            changes[i] -= 1
            if changes[i] == 0:
                lst.append(lst.pop(i))
                changes[i] = n - i
            else:
                j = n - changes[i]
                lst[j], lst[i] = lst[i], lst[j]
                flag = False
                yield tuple(iterable[k] for k in lst[:r])
            i -= 1
        if flag:
            break

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
    while lst[0] != n - r + 1:
        i = r
        while i > 1 and lst[i - 1] == n - r + i:
            i -= 1
        lst[i - 1:] = list(range(lst[i-1] + 1, lst[i-1] + r - i + 2))
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
