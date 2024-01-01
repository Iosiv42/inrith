""" Math function applicable to intervals. """

import math

from .utils import ifunc, copy


def log(interval_like, base: float = math.e):
    """ Log function over interval [union] with extra drifting. """

    i_cpy = copy(interval_like)
    func = ifunc(lambda x, base: (
        math.log(x, base) if x > 0 else math.copysign(1., base - 1)*math.inf
    ))
    for idx, i in enumerate(interval_like):
        i_cpy[idx] = func(i, base)

    return i_cpy
