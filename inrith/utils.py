""" Utils. """

import itertools
from typing import Callable, SupportsFloat

from .interval import Interval

BinaryFunction = Callable[[SupportsFloat, SupportsFloat], SupportsFloat]


def bin_op(operator: BinaryFunction) -> Callable[[Interval, Interval], Interval]:
    """ Returns function that takes 2 intervals and performs binary operator
        to them and produce new one. Binary operator must be monotonic
        at domain of intervals to return proper results.
    """

    def wrapper(lhs: Interval, rhs: Interval) -> Interval:
        map_op = lambda v: operator(*v)
        cart_prod = itertools.product(lhs.infsup(), rhs.infsup())
        vals = tuple(map(map_op, cart_prod))
        left_open = lhs.left_open or rhs.left_open
        right_open = lhs.right_open or rhs.right_open

        return Interval(
            min(vals), max(vals),
            left_open=left_open,
            right_open=right_open,
        )

    return wrapper

def ifunc(
    func: Callable[[SupportsFloat, ...], SupportsFloat]
) -> Callable[[Interval], Interval]:
    """ Return function that takes 1 interval and performs some unary function
        to it and returns new one. func must be monotone and bijective
        at the domain of interval to return proper results.
    """

    def wrapper(interval: Interval, *args) -> Interval:
        vals = tuple(func(i, *args) for i in interval.infsup())
        return Interval(
            min(vals), max(vals),
            left_open=interval.left_open,
            right_open=interval.right_open,
        )

    return wrapper
