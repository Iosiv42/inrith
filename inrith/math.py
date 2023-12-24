""" Math function applicable to intervals. """

import math

from .interval import Interval
from .interval_union import IntervalUnion


def log(
    interval: Interval | IntervalUnion, base: float = math.e
) -> Interval | IntervalUnion:
    NotImplemented
