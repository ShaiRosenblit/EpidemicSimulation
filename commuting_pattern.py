import random
from typing import List, Tuple, Optional, Union, Callable

from location import Location, PublicTransport
from timing import datetime, timedelta


class CommutingPattern:
    def __init__(self):
        self.initial_location_condition: Optional[List[Location]] = None
        self.minutes_condition: Optional[Tuple[float, float]] = None
        self.day_condition: Optional[List[int]] = None
        self.time_in_location_condition: Optional[float] = None

        self.final_location_options: List[Location] = None
        self.travel_time: Union[float, Callable[[Location, Location], float]] = None

        self.probability_per_minute: float = None

    def apply(self, current_location: Location, time: datetime, time_in_location: float, time_step: float) -> Optional[
        Tuple[Location, datetime]]:

        # TODO: make sure this applies to public transport

        if (self.initial_location_condition is not None) and (current_location not in self.initial_location_condition):
            return None
        if (self.minutes_condition is not None) and (
                not (self.minutes_condition[0] <= (60 * time.hour + time.minute) <=
                     self.minutes_condition[1])):
            return None
        if (self.day_condition is not None) and (time.day not in self.day_condition):
            return None

        if (self.time_in_location_condition is not None) and (time_in_location < self.time_in_location_condition):
            return None

        if isinstance(current_location, PublicTransport):
            final_location_options = []
            if current_location.current_station in self.final_location_options:
                final_location_options.append(current_location.current_station)

        else:
            final_location_options = []
            for final_loc in self.final_location_options:
                if (not isinstance(final_loc, PublicTransport)) or (final_loc.current_station == current_location):
                    final_location_options.append(final_loc)

        if len(final_location_options) == 0:
            return None

        if (random.random > min(1, time_step * self.probability_per_minute)):
            return None

        final_location = random.choices(final_location_options)
        if callable(self.travel_time):
            travel_time = self.travel_time(current_location, final_location)
        else:
            travel_time = self.travel_time
        final_time = time + timedelta(minutes=travel_time)

        return final_location, final_time
