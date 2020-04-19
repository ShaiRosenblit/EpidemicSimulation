from typing import List, Tuple, Union


class BoundedArea:
    def __init__(self):
        self.locations: List['Location'] = None


class LocationBase:
    def __init__(self):
        self.people: List['Person'] = []


DummyLocation = LocationBase


class Location(LocationBase):
    def __init__(self):
        LocationBase.__init__(self)
        self.area: float = None
        self.dispersion_factor: float = None


class FixedLocation(Location):
    def __init__(self):
        Location.__init__(self)

        self.coordinates: Tuple[float, float] = None
        self.city: BoundedArea = None
        self.district: BoundedArea = None
        self.is_outdoor: bool = None
        self.essentiality: float = None


class TransportStation(FixedLocation):
    def __init__(self):
        FixedLocation.__init__(self)
        self.public_transports: List[PublicTransport] = None


class PublicTransport(Location):
    def __init__(self):
        Location.__init__(self)

        self.path: Tuple[TransportStation] = None
        self.start_times: List[Tuple[int, float]] = None
        self.travel_times: Tuple[float] = None

        self.current_station: Union[TransportStation, DummyLocation] = None


class AllLocations:
    def __init__(self):
        self.cities: List[BoundedArea] = None
        self.districts: List[BoundedArea] = None

        self.homes: List[FixedLocation] = None
