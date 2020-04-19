"""
functions for updating the state of the world
"""
from typing import List

from person import Person
from timing import datetime


def move_people(people:List[Person], policy, time:datetime, time_step:float):
    """
    move all people from site to site.
    `people` is the collection of all `Person`s.
    `time` is the current time.
    `time_step' is the size of the time step, in minutes.
    """
    for person in people:
        move_person(person, policy, time, time_step)


def move_person(person: Person, policy, time:datetime, time_step:float):
    """
    move person to next location, taking into account also the policy.
    `time` is the current time.
    `time_step' is the size of the time step, in minutes.
    """

    if person.is_in_dummy_site:
        # if the person is currently in the dummy state, check if it is time to
        # move it out of there, and if so - move it.
        if time >= person.next_site_time:
            new_site = person.next_site
            person.change_site(new_site)
        else:
            person.time_in_current_site += time_step
        return
    else:

        # `out` will have the result of the first commuting pattern to be
        # executed. if no commuting pattern is executed, it will remain `None`.
        out = None
        for commuting_patten in person.commuting_patterns:
            out = commuting_patten.apply(person.site, time,
                                         person.time_in_current_site, time_step)
            if out is not None:
                new_site, next_site_time = out[0], out[1]
                break
        if out is None:
            # no commuting pattern was executed - don't move person.
            person.time_in_current_site += time_step
            return
        else:
            # a commuting pattern was executed.
            if new_site == person.site:
                # if the new site equal the current site, don't do anything.
                person.time_in_current_site += time_step
                return
            elif next_site_time > time:
                # if the destination time in the new site is in the future - go
                # temporarily to the dummy site.
                person.put_in_dummy_site(new_site, next_site_time)
            else:
                # otherwise, go to the destination
                person.change_site(new_site)
