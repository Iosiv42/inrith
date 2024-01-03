""" Math function applicable to intervals. """

import math
from copy import deepcopy

from .utils import ifunc
from .interval_like import IntervalLike

PI, TAU = math.pi, 2*math.pi


def log(interval_like: IntervalLike, base: float = math.e) -> IntervalLike:
    """ Log function over interval like object with extra drifting. """

    i_cpy = deepcopy(interval_like)
    func = ifunc(lambda x, base: (
        math.log(x, base) if x > 0 else math.copysign(1., base - 1)*math.inf
    ))
    for idx, i in enumerate(interval_like):
        i_cpy[idx] = func(i, base)

    return i_cpy


def cos(interval_like: IntervalLike) -> IntervalLike:
    """ Cosine function over interval like object. """

    i_cpy = deepcopy(interval_like)
    func = ifunc(math.cos)
    for idx, i in enumerate(interval_like):
        i_cpy[idx] = func(i)

        next_max = TAU * math.ceil(i.inf / TAU)
        next_min = TAU * math.ceil((i.inf - PI) / TAU) + PI
        if next_max in i:
            i_cpy[idx].sup = 1.
        if next_min in i:
            i_cpy[idx].inf = -1.

    return i_cpy


def sin(interval_like: IntervalLike) -> IntervalLike:
    """ Sine function over interval like object. """
    return cos(0.5*PI - interval_like)
