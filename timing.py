from copy import copy
from datetime import datetime, timedelta
from typing import Optional

from pytz import timezone


def time_iter(time_step_minutes: float, initial_time: Optional[datetime] = None):
    time_step = timedelta(minutes=time_step_minutes)
    if initial_time is None:
        current_time = datetime(2020, 3, 1, 0, 0, tzinfo=timezone('Israel'))
    else:
        current_time = copy(initial_time)
    while True:
        yield current_time
        current_time = current_time + time_step
