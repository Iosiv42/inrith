""" Union of intervals. """

from typing import Iterable
from operator import attrgetter
import random

from interval import Interval, Common, Endpoint


class IntervalsUnion:
    """ Union of some intervals. Provides disjointness. """

    intervals_delimiter = " ∪ "

    # TODO need to keep intervals endnotes as is.
    def __init__(self, intervals: Iterable[Interval]):
        """ Reduce over intervals to form the union. """
        unique_intervals = tuple(set(i.as_closed() for i in intervals))
        endpoints = self.__get_endpoints(unique_intervals)

        # TODO such a tardy algorithm with O(n**2) complexity.
        # Think can be improved to O(n*log(n)) with interval trees.
        self.intervals = []
        curr_inf = None
        for endpoint in endpoints:
            in_count = 0
            for i in unique_intervals:
                in_count += endpoint.value in i.as_closed()

            if in_count == 1:
                if endpoint.is_inf():
                    curr_inf = endpoint.value
                elif endpoint.is_sup():
                    self.intervals.append(Interval(curr_inf, endpoint.value))
                    curr_inf = None

            if curr_inf is None:
                curr_inf = endpoint.value

    def __repr__(self):
        return self.intervals_delimiter.join(str(i) for i in self.intervals)

    def __get_endpoints(self, intervals: Iterable[Interval]) -> list[Endpoint]:
        endpoints = set()
        for i in intervals:
            endpoints.update(i.endpoints())
        endpoints = sorted(list(endpoints), key=attrgetter("value"))
        return endpoints


if __name__ == "__main__":
    intervals = []
    for _ in range(100):
        inf = random.randint(-100, 100)
        sup = inf + random.randint(0, 3)
        intervals.append(Interval(inf, sup))

    print(IntervalsUnion(intervals))
