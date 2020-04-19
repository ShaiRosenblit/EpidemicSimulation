"""
functions usefull for dealing with time
"""
from copy import copy
from datetime import datetime, timedelta
from typing import Optional

from pytz import timezone

# this just emphasizes that we want these classes to be imported from the
# current package
datetime = datetime
timedelta = timedelta

def time_iter(time_step_minutes: float, initial_time: Optional[datetime] = None):
    """
    a generator for iterating from an initial time to infinity, with a fixed
    time step.
    """
    time_step = timedelta(minutes=time_step_minutes)
    if initial_time is None:
        # if we don't have an initial time, use this default.
        current_time = datetime(2020, 3, 1, 0, 0, tzinfo=timezone('Israel'))
    else:
        current_time = copy(initial_time)
    while True:
        yield current_time
        current_time = current_time + time_step
