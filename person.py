from enum import Enum
from typing import List, Optional

from commuting_pattern import CommutingPattern
from sites import Site, FixedSite, dummy_site
from timing import datetime


class Sex(Enum):
    FEMALE = 0
    MALE = 1


class PersonOccupation(Enum):
    UNEMPLOYED = 0
    WORKER = 1
    STUDENT = 2
    OTEHR = 3


class Household:
    def __init__(self):
        self.people: List[Person] = None
        self.home: Site = None


class Person:
    def __init__(self):
        self.age: float = None
        self.sex: Sex = None
        self.occupation: PersonOccupation = None
        self.commuting_patterns: List[CommutingPattern] = None
        self.household: Household = None

        self.susceptibility_degree: float = None
        self.sickness_degree: float = None
        self.symptoms_degree: float = None
        self.time_sick_minutes: Optional[float] = None
        self.immunity_degree: float = None

        self.wears_mask_probability: float = None
        self.keeps_distance_probability: float = None
        self.washes_hands_probability: float = None
        self.obeys_quarantine_probability: float = None
        self.abides_by_rules_probability: float = None
        self.trackable_probability: float = None

        self.site: Site = None
        self.time_in_current_site: float = None
        self.current_commute: Optional[CommutingPattern] = None
        self.current_commute_start_time: Optional[float] = None

        self.next_site: Optional[Site] = None
        self.next_site_time: Optional[datetime] = None
        self.is_in_dummy_site: bool = None

    @property
    def location(self):
        if isinstance(self.site, FixedSite):
            return self.site.location
        else:
            return None

    def change_site(self, new_site: Site):
        if self.site is not new_site:

            if self.is_in_dummy_site:
                self.is_in_dummy_site = False
                self.next_site = None
                self.next_site_time = None

            self.site.people.remove(self)
            self.site = new_site
            new_site.people.append(self)
            self.time_in_current_site = 0

    def put_in_dummy_site(self, next_site:Site, next_site_time:datetime):

        self.change_site(dummy_site)

        self.is_in_dummy_site = True
        self.next_site = next_site
        self.next_site_time = next_site_time