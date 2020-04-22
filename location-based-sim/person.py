from enum import Enum
from typing import List, Optional, Union

from commuting_pattern import CommutingPattern
from sites import Site, FixedSite, dummy_site, DummySite
from timing import datetime


class Sex(Enum):
    FEMALE = 0
    MALE = 1


class PersonOccupation(Enum):
    UNEMPLOYED = 0
    WORKER = 1
    STUDENT = 2
    OTHER = 3


class Household:
    """
    A household represents a collection of `Person`s living in the same
    place (this is usually a family)
    """
    def __init__(self):

        # the collection of `Person`s the belong to the `Household`
        self.people: List[Person] = None

        # the `Site` that is the home
        self.home: FixedSite = None


class Person:
    """
    Represents a single person
    """
    def __init__(self):
        # age, in years
        self.age: float = None
        self.sex: Sex = None
        self.occupation: PersonOccupation = None

        # a collection of `CommutingPattern`s. A `CommutingPattern` can define
        # things such as: going to work, returning home, going to a store...
        self.commuting_patterns: List[CommutingPattern] = None

        # the `Household` (e.g. family) of the `Person`
        self.household: Household = None

        # magnitudes of various variables that characterize the illness
        # (the `Person` is ill if their `illness_degree` is strictly positive)
        self.susceptibility_degree: float = None
        self.illness_degree: float = None
        self.symptoms_degree: float = None
        self.immunity_degree: float = None

        # if currently infected, this will contain the total time being
        # infected, in days. Otherwise, this will be `None`
        self.time_infected_minutes: Optional[float] = None

        # the degree to which the `Person` will abide by rules enforced by a
        # policy, such as: masks, hand washing, social distancing, quarantine.
        self.abides_by_rules_degree: float = None

        # The `Person` is currently in this place.
        self.site: Union[Site, DummySite] = None

        # times, in minutes, of being in the current place
        self.time_in_current_site: float = None

        #
        self.current_commute: Optional[CommutingPattern] = None
        self.current_commute_start_time: Optional[float] = None

        # these variables will hold values only for when the `Person` is in a
        # dummy site. the dummy site is used for temporarily holding the person
        # until it gets to its destination, given by the following variables.
        # if the `Person` is not in the dummy site, these should have the `None`
        # value.
        self.next_site: Optional[Site] = None
        self.next_site_time: Optional[datetime] = None


    @property
    def location(self):
        """
        get (x,y) coordinates (meters)
        """
        if isinstance(self.site, FixedSite):
            return self.site.location
        else:
            return None

    @property
    def is_in_dummy_site(self):
        return self.site == dummy_site

    def change_site(self, new_site: Site):
        """
        invoke this function when moving from site to site
        """
        # if this condition is false, no change should be made
        if self.site is not new_site:

            if self.is_in_dummy_site:
                # this means we are leaving the dummy site.
                self.next_site = None
                self.next_site_time = None

            # remove `Person` from its current site.
            self.site.people.remove(self)

            # change site of `Person`
            self.site = new_site

            # add `Person` to new site
            new_site.people.append(self)

            # reset counter of time in site.
            self.time_in_current_site = 0

    def put_in_dummy_site(self, next_site:Site, next_site_time:datetime):
        """
        put the `Person` in the dummy site. The dummy site is a place for
        temporarily hiding the `Person` until it gets to its next destination,
        at the time and place given by the arguments to this function.
        """

        self.change_site(dummy_site)

        self.next_site = next_site
        self.next_site_time = next_site_time

    def is_infected(self):
        """
        checks if the person is infected, if so return True.
        :return Boolean
        """
        return self.time_infected_minutes != None