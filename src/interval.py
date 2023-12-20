""" Real-valued interval. """

from enum import IntEnum, Enum
from typing import Callable, Self


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
        lower_bound: int | float,
        upper_bound: int | float,
        endnotes: Endnotes = Endnotes.AUTO,
        *,
        left_open: bool = None,
        right_open: bool = None,
    ):
        self.inf, self.sup = lower_bound, upper_bound
        if isinstance(lower_bound, float) != isinstance(upper_bound, float):
            self.inf = float(lower_bound)
            self.sup = float(upper_bound)

        if left_open is None or right_open is None:
            self.__handle_endnotes(endnotes)
        else:
            self.left_open = left_open
            self.right_open = right_open

    def binary_operator(
        self, other: Self, operator: Callable[[int | float], float]
    ) -> Self:
        """ Performs binary operator on self interval and another one.
            It'll return correct results if and only if function is monotone
            for each operand in union of given intervals.
        """

        vals = tuple(
            operator(i, j) for i in self.endpoints() for j in other.endpoints()
        )

        return Interval(
            min(vals), max(vals),
            left_open=self.left_open or other.left_open,
            right_open=self.right_open or other.right_open,
        )

    def endpoints(self) -> tuple[int | float]:
        """ Return the endpoints of self in form (infimum, supremum). """
        return (self.inf, self.sup)

    def __contains__(self, value: int | float):
        cond1 = self.inf <= value <= self.sup
        cond2 = not (value == self.inf and self.left_open)
        cond3 = not (value == self.sup and self.right_open)

        if cond1 and cond2 and cond3:
            return True
        return False

    def __repr__(self):
        if self == Common.EMPTY:
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
            print("da")
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
    print(i2 & i1)
