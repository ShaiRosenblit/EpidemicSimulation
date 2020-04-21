from typing import List, Tuple, Optional
from timing import datetime
from meetings import Meeting
import random

class BoundedArea:
    """
    A bounded area can represent, e.g., a city or district. It is implemented
    simply as a collection of `Site` objects (for example, it will contain all
    `Site`s that belong to the city).
    """
    def __init__(self):

        # list of `Site` objects that belong to this bounded area.
        self.sites: List['Site'] = None


class SiteBase:
    """
    base class for all `Site` classes. The only thing in common with all `Site`s
    is that they include a collection  of `Person`s who are located at the
    `Site`.
    """
    def __init__(self):

        # list of people current in the site
        self.people: List['Person'] = []


class DummySite(SiteBase):
    """
    The `DummySite` is a special site, used for the purpose of temporarily
    "hiding" `Person`s. For example, if a `Person` drives from one `Site` to
    another in a private car, during this time the `Person` should not be
    considered in any `Site`. Therefore, we temporarily put it in a `DummySite`.
    The special thing about the `DummySite` is that nobody can get infected
    in it. This class should be a singleton (i.e only one instance)
    """
    def __init__(self):
        SiteBase.__init__(self)

# this is the only instance of the `DummySite`
dummy_site = DummySite()


class Site(SiteBase):
    """
    A base class for more specific `Site`s.
    """
    def __init__(self):
        SiteBase.__init__(self)

        # the "effective" area, in meters squared, of the site.
        self.area: float = None

        # the typical maximal number of people that the site can contain
        self.nominal_capacity: int = None

        # this value determines the tendency of people in the site to move around
        # (lower values mean that people are relatively static)
        self.dispersion_factor: float = None

        # the probability of creating a meeting, depending on the area, number of people in the site
        # and the dispersion factor of the site
        self.meeting_probability: float = None

    def update_meeting_probability(self):
        """
        calculates the meeting probabilty in a 'Site' in a certain moment.
        multiplying the number of people in square meters with the dispersion factor.
        the meeting probability is in scale of 0 to 100.
        """
        if len(self.people) < 2:
            self.meeting_probability = 0
        else:
            m_p = (len(self.people)*10/self.area)*self.dispersion_factor*100
            self.meeting_probability = m_p if m_p < 100 else 100

    def check_meeting(self):
        """
        checks for meetings randomly using the meeting probability.
        if the randomized number is in the range of the meeting probability a 'Meeting' object is created.
        :return list of meetings that occured in the 'Site'.
                if no meetings were created returns an empty list.
        """
        meetings = []
        if self.meeting_probability > 0:
            for i in range(len(self.people)):
                if random.uniform(0, 100) <= self.meeting_probability:
                    person1 = self.people[i]
                    person2 = random.choice([person for person in self.people if person != person1])
                    meeting = Meeting().create_meeting(person1=person1, person2=person2, site=self)
                    meeting.time = datetime
                    meetings.append(meeting)
        return meetings


class FixedSite(Site):
    """
    A `Site` that has a fixed location
    """
    def __init__(self):
        Site.__init__(self)

        # location, as coordinates (x,y), in meters.
        self.location: Tuple[float, float] = None

        # The city containing the `FixedSite` belongs to
        self.city: BoundedArea = None

        # The district containing the `FixedSite` belongs to
        self.district: BoundedArea = None

        # whether the `FixedSite` is outdoors
        self.is_outdoor: bool = None

        # the degree of how essential this place is. Higher values means that
        # the place is more essential for the economy / society
        self.essentiality: float = None


class TransportStation(FixedSite):
    """
    A specific `FixedSite` representing a public transportation station (such
    as a bus stop)
    """
    def __init__(self):
        FixedSite.__init__(self)

        # a collection of all public transport lines passing through
        self.public_transports: List[PublicTransport] = None


class PublicTransport(Site):
    """
    A specific `Site` which represents a public transport vehicle, such as a
    bus. A `PublicTransport` does not have a fixed locations. Rather, it has
    a sequence of `TransportStation` through  which it moves according to a
    schedule.
    """
    def __init__(self):
        Site.__init__(self)

        # A sequence of `TransportStation`s where the `PublicTransport` stops
        self.path: Tuple[TransportStation] = None

        # a list of tuples (day of week, time in day in minutes). These represent
        # the times of the week when the `PublicTransport` starts its rounds.
        self.start_times: List[Tuple[int, float]] = None

        # This sequence should have length smaller by 1 than the length of
        # `self.path`. It represents the times (in minutes) that it takes to
        # travel between every two consecutive `TransportStation`s.
        self.travel_times: Tuple[float] = None

        # The current `TransportStation` of the `PublicTransport`. If currently
        # in between stations, it will be `None`
        self.current_station: Optional[TransportStation] = None

        # index of next station in `path`
        self.next_station_index: Optional[int] = None

        # time of stop in next station in `path`
        self.next_station_time: Optional[datetime] = None