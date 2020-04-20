import random
from typing import Callable, List, Optional, Tuple, Union

from sites import PublicTransport, Site
from timing import datetime, timedelta


class CommutingPattern:
    """
    A `CommutingPattern` defines some pattern of movement for a `Person`,
    between
    `Sites`s.
    """

    def __init__(self):
        # TODO: change some of these from list to set

        # a set of initial places, such that the pattern will be executed only
        # if the `Person` is in one of these places.
        self.initial_site_condition: Optional[List[Site]] = None

        # a set of days in the week (as integers), such that the pattern will be
        # executed only on these days. (Monday = 0, Sunday = 6)
        self.day_condition: Optional[List[int]] = None

        # a set of time intervals in the day, defined as tuples of initial and
        # final times (in minutes), such that the pattern will be executed only
        # in these time intervals.
        self.minutes_condition: Optional[Tuple[float, float]] = None

        # a time (in minutes) such that the pattern will be executed only if the
        # `Person` has been in the current place at least this amount of time
        self.time_in_site_condition: Optional[float] = None

        # a set of final sites. one of these will be chosen at random each time
        # the pattern is executed.
        self.final_site_options: List[Site] = None

        # the time it takes to arrive to the final site. this can be either a
        # float number, or a function that takes two sites and returns a number.
        self.travel_time: Union[float, Callable[[Site, Site], float]] = None

        # A pattern is executed only if all the conditions mentioned above
        # are satisfied, but there is still a probability that it won't be
        # executed. To calculate the probability that the pattern will be
        # executed in a time step, multiply the length of the time step by the
        # following number (and limit by 1.0).
        self.probability_per_minute: float = None

    def apply(self, current_site: Site, time: datetime, time_in_site: float,
              time_step: float) -> Optional[
        Tuple[Site, datetime]]:
        """
        given the current site and time, and the total time of presence in the
        current site (in minutes), and the size of the time step (minutes),
        calculate the result of executing the commuting pattern.
        If the commuting pattern is not executed, return `None`. Otherwise,
        return a tuple of (site, time), representing the destination time and
        the time of arrival to the site.
        """

        # check condition for initial location
        if (self.initial_site_condition is not None) and (
                current_site not in self.initial_site_condition):
            return None

        # check condition for day of weak
        if (self.day_condition is not None) and (
                time.weekday() not in self.day_condition):
            return None

        # check condition for time of day
        if (self.minutes_condition is not None) and (
                not (self.minutes_condition[0] <= (
                        60 * time.hour + time.minute) <=
                     self.minutes_condition[1])):
            return None

        # check condition for total time in current site
        if (self.time_in_site_condition is not None) and (
                time_in_site < self.time_in_site_condition):
            return None

        # randomly decide whether the pattern will be executed
        if (random.random() > min(1, time_step * self.probability_per_minute)):
            return None

        # we will now find the optional destination places.

        # if we are currently in a public transport, then the optional
        # destination places are only the current station
        if isinstance(current_site, PublicTransport):
            final_site_options = []
            if current_site.current_station in self.final_site_options:
                final_site_options.append(current_site.current_station)
        else:
            # the destination place can be a public transport only if
            # it is current in the same place as the current place
            final_site_options = []
            for final_loc in self.final_site_options:
                if (not isinstance(final_loc, PublicTransport)) or (
                        final_loc.current_station == current_site):
                    final_site_options.append(final_loc)

        # check wheter there are any optional destination places
        if len(final_site_options) == 0:
            return None

        # choose a destination place
        final_site = random.choice(final_site_options)

        # calculate the time it takes to travel to the destination
        if callable(self.travel_time):
            travel_time = self.travel_time(current_site, final_site)
        else:
            travel_time = self.travel_time

        # calculate arrival time at destination
        final_time = time + timedelta(minutes=travel_time)

        return final_site, final_time
