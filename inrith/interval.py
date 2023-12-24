""" Real-valued interval. """

from enum import IntEnum
from typing import Callable, Self, SupportsFloat
from itertools import product
from dataclasses import dataclass

from .utils import bin_op, ifunc


BRACKETS_FMT = {
    True: {
        -1: "(",
        1: ")",
    },
    False: {
        -1: "[",
        1: "]",
    }
}
VALUE_DELIMITER = ", "


class Endnotes(IntEnum):
    """ Type of interval's endpoints. """
    OPENED = 2
    CLOSED = 0
    RIGHT_OPEN = 1
    LEFT_OPEN = -1
    AUTO = 7


SOME_SHIT = {
    Endnotes.OPENED: (True, True),
    Endnotes.CLOSED: (False, False),
    Endnotes.RIGHT_OPEN: (False, True),
    Endnotes.LEFT_OPEN: (True, False),
}


class EndpointType(IntEnum):
    """ Types of endpoint. """
    INF = -1
    SUP = 1


@dataclass
class Endpoint:
    """ Endpoint of an interval. """
    value: SupportsFloat
    type: EndpointType

    def is_inf(self) -> bool:
        """ Is self.type is infimum? """
        return self.type == EndpointType.INF

    def is_sup(self) -> bool:
        """ Is self.type is supremum? """
        return self.type == EndpointType.SUP

    def __hash__(self):
        return hash((self.value, self.type))

    def __repr__(self):
        return f"({self.value} {self.type})"


class Interval:
    """ Class describing real-valued interval. """

    def __init__(
        self,
        infimum: SupportsFloat,
        supremum: SupportsFloat,
        endnotes: Endnotes = Endnotes.AUTO,
        *,
        left_open: bool = None,
        right_open: bool = None,
    ):
        assert infimum <= supremum, "infimum has to be <= supremum"

        self.inf, self.sup = infimum, supremum

        # It's for proper self.binary_operator working.
        if isinstance(infimum, float) != isinstance(supremum, float):
            self.inf = float(infimum)
            self.sup = float(supremum)

        if left_open is None or right_open is None:
            self.__handle_endnotes(endnotes)
        else:
            self.left_open = left_open
            self.right_open = right_open

        # If interval isn't left or right bounded than it has to be
        # left or right opened.
        self.left_open = self.left_open >= self.left_bounded()
        self.right_open = self.right_open >= self.right_bounded()

    def endpoints(self) -> tuple[Endpoint]:
        """ Return the endpoints of self in form
            (infimum endpoint, supremum endpoint).
        """
        return (Endpoint(self.inf, EndpointType.INF), Endpoint(self.sup, EndpointType.SUP))

    def infsup(self) -> tuple[SupportsFloat]:
        """ Return infimum and supremum of self in form (inf., sup.). """
        return (self.inf, self.sup)

    def as_closed(self) -> Self:
        """ Return interval as closed. """
        return Interval(self.inf, self.sup, Endnotes.CLOSED)

    def as_opened(self) -> Self:
        """ Return interval as opened. """
        return Interval(self.inf, self.sup, Endnotes.OPENED)

    def empty(self) -> bool:
        """ Return if interval is empty set. """
        return (self.left_open or self.right_open) and self.inf == self.sup

    def left_bounded(self) -> bool:
        """ Return left boundness of interval. """
        return self.inf > -float("inf") or self.empty()

    def right_bounded(self) -> bool:
        """ Return right boundness of interval. """
        return self.sup < float("inf") or self.empty()

    def bounded(self) -> bool:
        """ Return boundness of interval. """
        return self.left_bounded() and self.right_bounded()

    def diameter(self) -> SupportsFloat:
        """ Return diameter (length, width) of interval. """
        return self.sup - self.inf

    def center(self) -> SupportsFloat:
        """ Return center (midpoint) of interval. """
        if self.empty():
            return float("nan")
        return 0.5 * (self.inf + self.sup)

    def __contains__(self, value: SupportsFloat):
        # Don't know such a good way to do this without ifs and using less code.
        # It'd better if there's way to get operators depending of openness of interval.
        cond1 = self.inf <= value <= self.sup
        cond2 = not (value == self.inf and self.left_open)
        cond3 = not (value == self.sup and self.right_open)

        return cond1 and cond2 and cond3

    def __repr__(self):
        if self.empty():
            return "∅"

        lb = BRACKETS_FMT[self.left_open][-1]
        rb = BRACKETS_FMT[self.right_open][1]
        return f"{lb}{self.inf}{VALUE_DELIMITER}{self.sup}{rb}"

    def __hash__(self):
        return hash((self.inf, self.sup, self.left_open, self.right_open))

    def __eq__(self, other: Self):
        return all((
            self.inf == other.inf,
            self.sup == other.sup,
            self.left_open == other.left_open,
            self.right_open == other.right_open,
        ))

    def __add__(self, other: Self) -> Self:
        return bin_op(type(self.inf).__add__)(self, other)

    def __sub__(self, other: Self) -> Self:
        return bin_op(type(self.inf).__sub__)(self, other)

    def __mul__(self, other: Self) -> Self:
        return bin_op(type(self.inf).__mul__)(self, other)

    def __truediv__(self, other: Self) -> Self:
        return bin_op(type(self.inf).__truediv__)(self, other)

    def __rpow__(self, other: SupportsFloat) -> Self:
        return ifunc(lambda val: other**val)(self)

    def __pow__(self, other: int) -> Self:
        if self.inf < 0 and self.sup > 0 and other % 2 == 0:
            return Interval(0, max(self.inf**other, self.sup**other))
        return ifunc(lambda val: val**other)(self)

    def __and__(self, other: Self) -> Self:
        # TODO can we do something with that?
        if self <= other:
            return self
        if other <= self:
            return other
        if self.sup in other:
            return Interval(
                other.inf, self.sup,
                left_open=other.left_open, right_open=self.right_open,
            )
        if self.inf in other:
            return Interval(
                self.inf, other.sup,
                left_open=self.left_open, right_open=other.right_open,
            )
        return Common.EMPTY

    def __le__(self, other: Self) -> bool:
        # [inf,sup]_aux_cond are needed for half or opened intervals.
        # E.g. for checking [0, +oo) <= (-oo, +oo), because +oo not in (-oo, +oo).
        inf_aux_cond = (self.inf == other.inf) and (self.left_open == other.left_open)
        sup_aux_cond = (self.sup == other.sup) and (self.right_open == other.right_open)
        return (
            (self.inf in other or inf_aux_cond)
            and (self.sup in other or sup_aux_cond)
        )

    def __iter__(self):
        yield self

    def __handle_endnotes(self, endnotes: Endnotes) -> None:
        """ Handle type of interval's endpoints and set right and left openness."""
        if endnotes == Endnotes.AUTO:
            self.left_open = abs(self.inf) == float("inf")
            self.right_open = abs(self.sup) == float("inf")
        else:
            try:
                self.left_open, self.right_open = SOME_SHIT[endnotes]
            except KeyError as exc:
                raise KeyError("Unsupported endnote.") from exc


class Common:
    """ Common intervals. """
    EMPTY = Interval(0, 0, Endnotes.OPENED)
    REALS = Interval(float("-inf"), float("inf"))


if __name__ == "__main__":
    a = Interval(-2, 1)
    b = Interval(5., 7)
    x = Interval(2, 64)
    for i in a:
        print(i)
