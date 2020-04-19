import random
from typing import List, Tuple, Optional, Union, Callable
from sites import Site, PublicTransport
from timing import datetime, timedelta


class CommutingPattern:
    def __init__(self):
        self.initial_site_condition: Optional[List[Site]] = None
        self.minutes_condition: Optional[Tuple[float, float]] = None
        self.day_condition: Optional[List[int]] = None
        self.time_in_site_condition: Optional[float] = None

        self.final_site_options: List[Site] = None
        self.travel_time: Union[float, Callable[[Site, Site], float]] = None

        self.probability_per_minute: float = None

    def apply(self, current_site: Site, time: datetime, time_in_site: float, time_step: float) -> Optional[
        Tuple[Site, datetime]]:

        # TODO: make sure this applies to public transport

        if (self.initial_site_condition is not None) and (current_site not in self.initial_site_condition):
            return None
        if (self.minutes_condition is not None) and (
                not (self.minutes_condition[0] <= (60 * time.hour + time.minute) <=
                     self.minutes_condition[1])):
            return None
        if (self.day_condition is not None) and (time.day not in self.day_condition):
            return None

        if (self.time_in_site_condition is not None) and (time_in_site < self.time_in_site_condition):
            return None

        if (random.random > min(1, time_step * self.probability_per_minute)):
            return None

        if isinstance(current_site, PublicTransport):
            final_site_options = []
            if current_site.current_station in self.final_site_options:
                final_site_options.append(current_site.current_station)

        else:
            final_site_options = []
            for final_loc in self.final_site_options:
                if (not isinstance(final_loc, PublicTransport)) or (final_loc.current_station == current_site):
                    final_site_options.append(final_loc)

        if len(final_site_options) == 0:
            return None

        final_site = random.choices(final_site_options)
        if callable(self.travel_time):
            travel_time = self.travel_time(current_site, final_site)
        else:
            travel_time = self.travel_time
        final_time = time + timedelta(minutes=travel_time)

        return final_site, final_time
