"""
functions for updating the state of the world
"""
import random
from typing import List

from person import Person
from sites import Site
from timing import datetime
from functools import reduce


def move_people(people: List[Person], policy, time: datetime, time_step: float):
    """
    move all people from site to site.
    `people` is the collection of all `Person`s.
    `time` is the current time.
    `time_step' is the size of the time step, in minutes.
    """
    for person in people:
        move_person(person, policy, time, time_step)


def move_person(person: Person, policy, time: datetime, time_step: float):
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


def update_people_status(sites: List[Site], policy, time_step: float, time: datetime):
    """
    update the status of all people, by looping over all sites and updating
    for the people in each site.
    `time_step' is the size of the time step, in minutes.
    :param time - current time
    """
    for site in sites:
        ###
        site.update_meeting_probability(time_step)
        meetings = site.check_meeting(time)
        ###
        # update_people_status_for_site(site, policy, time_step, meetings)
        update_people_status_based_on_meetings(site, policy, time_step, meetings)

def update_people_status_for_site(site: Site, policy, time_step: float, meetings: list):
    """
    update the status of all people in given site.
    `time_step' is the size of the time step, in minutes.
    """
    people = site.people
    number_of_people = len(people)
    if number_of_people == 0:
        return

    # the following code should be changed to be a realistic model of the chance
    # if infection given the site and people properties.

    # calculate several variables
    number_of_ill_people = sum(
        [person.illness_degree > 0 for person in people])
    ratio_of_ill_people = number_of_ill_people / number_of_people
    density = number_of_people / site.area
    ratio_of_capacity = number_of_people / site.nominal_capacity

    # from these variables, get a "score" for the site, where a high score
    # means higher chance if infection
    site_infecting_score = time_step * ratio_of_ill_people * density * \
                           ratio_of_capacity \
                           * site.dispersion_factor / 50.0

    # for each person, calculate whether it got infected, or maybe even healed
    for person in people:

        # a probability for this specific person of getting infected
        person_infecting_score = site_infecting_score * (
                    1 - person.immunity_degree) * person.susceptibility_degree

        # perform infection
        if random.random() < person_infecting_score:
            person.illness_degree = 1.0
            if person.time_infected_minutes is None:
                person.time_infected_minutes = 0.0

        # if did not get infected
        else:

            # if already infected from before
            if person.illness_degree > 0.0:

                # chance of healing
                if random.random() < 0.00001*time_step:

                    # apply healing
                    person.illness_degree = 0.0
                    person.immunity_degree = 1.0
                    person.time_infected_minutes = None

                # if did not heal
                else:
                    person.time_infected_minutes += time_step

def update_people_status_based_on_meetings(site: Site, policy, time_step: float, meetings: list):
    """
    update the status of all people in given site.
    `time_step' is the size of the time step, in minutes.
    """

    # reduces only for meetings that contained an infected person
    meetings = [meeting for meeting in meetings if meeting.is_meeting_infected()]

    if len(meetings) > 0:
        site_infecting_score = calculate_site_infection_score(site, time_step)
        all_people_envolved = reduce(lambda a, b: a + b, [meeting._people_involved for meeting in meetings])
        for person in all_people_envolved:
            if person.is_infected:
                try_to_heal(person, time_step)
            else:
                try_to_infect(person, site_infecting_score)

def calculate_site_infection_score(site: Site, time_step):
    """
    calculates an infection score for a specific site,
    based on several variables derived from the people and the site.
    :param site - the current site
    :param time_step - the intervals
    :return site_infecting_score.
    """
    number_of_people = len(site.people)
    if number_of_people == 0:
        return

    # calculate several variables
    number_of_ill_people = len([person for person in site.people if person.is_infected])
    ratio_of_ill_people = number_of_ill_people / number_of_people
    density = number_of_people / site.area
    ratio_of_capacity = number_of_people / site.nominal_capacity

    # from these variables, get a "score" for the site, where a high score
    # means higher chance if infection
    site_infecting_score = time_step * ratio_of_ill_people * density * \
                           ratio_of_capacity \
                           * site.dispersion_factor / 50.0
    return site_infecting_score

def try_to_heal(person, time_step):
    """
    attempts to heal an infected person.
    if succeeded zeros the infection parameter and the person is no more infectious.
    otherwise increments the infection count.
    :param person - the person to be healed
    :param time_step - the time intervals
    """
    # chance of healing
    if random.random() < 0.00001 * time_step:

        # apply healing
        person.illness_degree = 0.0
        person.immunity_degree = 1.0
        person.time_infected_minutes = None
        person.is_infected = False
    #if not healed
    else:
        person.time_infected_minutes += time_step

def try_to_infect(person, site_infecting_score):
    """
    in a contagious meeting try to infect a non infected person.
    if succeeded start the time infected count/
    :param person - the person to be infected
    :param site_infecting_score - the infecting score calculated for the specific site.
    """
    # a probability for this specific person of getting infected
    person_infecting_score = site_infecting_score * (
            1 - person.immunity_degree) * person.susceptibility_degree

    # perform infection
    if random.random() < person_infecting_score:
        person.illness_degree = 1.0
        person.time_infected_minutes = 0.0
        person.is_infected = True
