from copy import copy
from datetime import datetime, timedelta
from typing import Optional

from pytz import timezone

MINUTES_PER_DAY = 24 * 60
DAYS_PER_WEEK = 7


class Time:
    def __init__(self, day_of_week: int, minute_of_day: float):
        self.day_of_week = day_of_week
        self.minute_of_day = minute_of_day

    def advance(self, time_step_minutes: float, return_copy=False):
        if return_copy:
            time = copy(Time)
        else:
            time = self
        time.minute_of_day += time_step_minutes
        if time.minute_of_day > MINUTES_PER_DAY:
            time.minute_of_day = time.minute_of_day % MINUTES_PER_DAY
            time.day_of_week = (time.day_of_week + 1) % DAYS_PER_WEEK
        return time


def time_iter(time_step_minutes: float, initial_time: Optional[datetime] = None):
    time_step = timedelta(minutes=time_step_minutes)
    if initial_time is None:
        current_time = datetime(2020, 3, 1, 0, 0, tzinfo=timezone('Israel'))
    else:
        current_time = copy(initial_time)
    while True:
        yield current_time
        current_time = current_time + time_step
