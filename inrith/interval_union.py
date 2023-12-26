""" Union of real-valued intervals. """

from typing import Iterable
from operator import attrgetter

from .interval import Interval, Endpoint

INTERVALS_DELIMITER = " ∪ "


class IntervalUnion:
    """ Union of some intervals. Provides disjointness. """

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
        return INTERVALS_DELIMITER.join(map(str, self.intervals))

    def __iter__(self):
        for i in self.intervals:
            yield i

    def __getitem__(self, index: int):
        return self.intervals[i]

    def __get_endpoints(self, intervals: Iterable[Interval]) -> list[Endpoint]:
        endpoints = set()
        for i in intervals:
            endpoints.update(i.endpoints())
        return sorted(endpoints, key=attrgetter("value"))


if __name__ == "__main__":
    intervals = (
        Interval(-1, 2),
        Interval(1, 2),
    )

    print(IntervalUnion(intervals))
