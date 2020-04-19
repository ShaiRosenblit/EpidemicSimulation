from enum import Enum
from typing import List, Optional

from commuting_pattern import CommutingPattern
from location import Location, FixedLocation
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
        self.home: Location = None


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

        self.location: Location = None
        self.time_in_current_location: float = None
        self.current_commute: Optional[CommutingPattern] = None
        self.current_commute_start_time: Optional[float] = None

        self.next_location: Optional[Location] = None
        self.next_location_time: Optional[datetime] = None
        self.is_in_dummy_location: bool = None

    @property
    def coordinates(self):
        if isinstance(self.location, FixedLocation):
            return self.location.coordinates
        else:
            return None
