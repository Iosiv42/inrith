""" Interface that acts like interval or interval union. """

from typing import Protocol, Iterator
from .interval import Interval


class IntervalLike(Protocol):
    """ For convinient using in math functions. """

    def __iter__(self) -> Iterator[Interval]:
        ...

    def __getitem__(self, index: int) -> Interval:
        ...

    def __setitem__(self, index: int, val: Interval):
        ...
