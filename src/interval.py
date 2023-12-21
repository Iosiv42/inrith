""" Real-valued interval. """

from enum import IntEnum, Enum
from typing import Callable, Self
from itertools import product
import math


class Endnotes(IntEnum):
    """ Type of interval's endpoints. """
    OPENED = 2
    CLOSED = 0
    RIGHT_OPEN = 1
    LEFT_OPEN = -1
    AUTO = 7


class Interval:
    """ Class describing real-valued interval. """

    left_brackets = {True: "(", False: "["}
    right_brackets = {True: ")", False: "]"}
    value_delimiter = ", "

    def __init__(
        self,
        infimum: int | float,
        supremum: int | float,
        endnotes: Endnotes = Endnotes.AUTO,
        *,
        left_open: bool = None,
        right_open: bool = None,
    ):
        assert infimum <= supremum, "lower_bound has to be <= upper_bound"

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

    def binary_operator(
        self, other: Self, operator: Callable[[int | float], float]
    ) -> Self:
        """ Performs binary operator on self interval and another one.
            It'll return correct results if and only if function is monotone
            for each operand in union of given intervals.
        """

        vals = tuple(map(operator, product(self.infsup(), other.infsup())))
        left_open = self.left_open or other.left_open
        right_open = self.right_brackets or other.right_open

        return Interval(
            min(vals), max(vals),
            left_open=left_open,
            right_open=right_open,
        )

    def endpoints(self) -> tuple[int | float]:
        """ Return the endpoints of self in form (infimum, supremum). """
        return (self.inf, self.sup)

    def infsup(self) -> tuple[int | float]:
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

    def diameter(self) -> int | float:
        """ Return diameter (length, width) of interval. """
        return self.sup - self.inf

    def center(self) -> int | float:
        """ Return center (midpoint) of interval. """
        if self.empty():
            return float("nan")
        return 0.5 * (self.inf + self.sup)

    def function(
        self, func: Callable[[int | float, ...], int | float], *args
    ) -> Self:
        """ Passes interval through func. func has to be
            monotonic and bijective at range of interval.
        """
        vals = tuple(map(lambda i: func(i, *args), self.infsup()))
        return Interval(
            min(vals), max(vals),
            left_open=self.left_open, right_open=self.right_open
        )

    def log(self, base: int | float = math.e) -> Self:
        """ Calculate logarithm of interval with handling for negative values. """
        if self.inf <= 0 and self.sup > 0:
            inf = float("inf") * math.copysign(1., 1 - base)
            return Interval(inf, math.log(self.sup, base))
        if self.sup <= 0:
            return Common.EMPTY
        return self.function(math.log, base)

    def __contains__(self, value: int | float):
        # Don't know such a good way to do this without ifs and using less code.
        # It'd better if there's way to get operators depending of openness of interval.
        cond1 = self.inf <= value <= self.sup
        cond2 = not (value == self.inf and self.left_open)
        cond3 = not (value == self.sup and self.right_open)

        return cond1 and cond2 and cond3

    def __repr__(self):
        if (self.left_open or self.right_open) and self.inf == self.sup:
            return "∅"

        lb = self.left_brackets[self.left_open]
        rb = self.right_brackets[self.right_open]
        return f"{lb}{self.inf}{self.value_delimiter}{self.sup}{rb}"

    def __eq__(self, other: Self):
        return all((
            self.inf == other.inf,
            self.sup == other.sup,
            self.left_open == other.left_open,
            self.right_open == other.right_open,
        ))

    def __add__(self, other: Self) -> Self:
        return self.binary_operator(other, type(self.inf).__add__)

    def __sub__(self, other: Self) -> Self:
        return self.binary_operator(other, type(self.inf).__sub__)

    def __mul__(self, other: Self) -> Self:
        return self.binary_operator(other, type(self.inf).__mul__)

    def __truediv__(self, other: Self) -> Self:
        return self.binary_operator(other, type(self.inf).__truediv__)

    def __and__(self, other: Self) -> Self:
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

    def __handle_endnotes(self, endnotes: Endnotes) -> None:
        """ Handle type of interval's endpoints and set right and left openness."""
        match endnotes:
            case Endnotes.CLOSED:
                self.right_open = False
                self.left_open = False
            case Endnotes.OPENED:
                self.right_open = True
                self.left_open = True
            case Endnotes.RIGHT_OPEN:
                self.right_open = True
                self.left_open = False
            case Endnotes.LEFT_OPEN:
                self.right_open = False
                self.left_open = True
            case Endnotes.AUTO:
                self.left_open = self.inf == -float("inf")
                self.right_open = self.sup == float("inf")
            case _:
                raise ValueError("Cannot decide endpoints type.")


class Common:
    """ Common intervals. """
    EMPTY = Interval(0, 0, Endnotes.OPENED)
    REALS = Interval(float("-inf"), float("inf"))


if __name__ == "__main__":
    i1 = Interval(0, float("inf"))
    i2 = Interval(float("-inf"), 10)
    i3 = Interval(1, 2)
    print(i1, i2, i3.log())
