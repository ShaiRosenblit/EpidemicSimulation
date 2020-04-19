from typing import List, Tuple, Union


class BoundedArea:
    def __init__(self):
        self.sites: List['Site'] = None


class SiteBase:
    def __init__(self):
        self.people: List['Person'] = []


class DummySite(SiteBase):
    def __init__(self):
        SiteBase.__init__(self)

dummy_site = DummySite()


class Site(SiteBase):
    def __init__(self):
        SiteBase.__init__(self)
        self.area: float = None
        self.dispersion_factor: float = None


class FixedSite(Site):
    def __init__(self):
        Site.__init__(self)

        self.location: Tuple[float, float] = None
        self.city: BoundedArea = None
        self.district: BoundedArea = None
        self.is_outdoor: bool = None
        self.essentiality: float = None


class TransportStation(FixedSite):
    def __init__(self):
        FixedSite.__init__(self)
        self.public_transports: List[PublicTransport] = None


class PublicTransport(Site):
    def __init__(self):
        Site.__init__(self)

        self.path: Tuple[TransportStation] = None
        self.start_times: List[Tuple[int, float]] = None
        self.travel_times: Tuple[float] = None

        self.current_station: Union[TransportStation, DummySite] = None


class AllSites:
    def __init__(self):
        self.cities: List[BoundedArea] = None
        self.districts: List[BoundedArea] = None

        self.homes: List[FixedSite] = None
