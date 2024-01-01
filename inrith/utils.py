""" Utils. """

import itertools
import pickle
from typing import Callable, SupportsFloat
from functools import cache

BinaryFunction = Callable[[SupportsFloat, SupportsFloat], SupportsFloat]


@cache
def bin_op(operator: BinaryFunction) -> Callable:
    """ Returns function that takes 2 intervals and performs binary operator
        to them and produce new one. Binary operator must be monotonic
        at domain of intervals to return proper results.
    """

    from .interval import Interval

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


@cache
def ifunc(func: Callable[[SupportsFloat, ...], SupportsFloat]) -> Callable:
    """ Return function that takes 1 interval and performs some unary function
        to it and returns new one. func must be monotone and bijective
        at the domain of interval to return proper results.
    """

    from .interval import Interval

    def wrapper(interval: Interval, *args) -> Interval:
        vals = tuple(func(i, *args) for i in interval.infsup())
        return Interval(
            min(vals), max(vals),
            left_open=interval.left_open,
            right_open=interval.right_open,
        )

    return wrapper


def copy(obj):
    return pickle.loads(pickle.dumps(obj))
