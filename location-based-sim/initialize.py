import random
from typing import List

from commuting_pattern import CommutingPattern
from sites import Site, FixedSite, PublicTransport, TransportStation, BoundedArea, dummy_site
from person import Sex, PersonOccupation, Household, Person


class AllSites:
    def __init__(self):
        self.cities: List[BoundedArea] = []
        self.districts: List[BoundedArea] = []

        self.homes: List[FixedSite] = []
        self.businesses: List[FixedSite] = []
        self.stores: List[FixedSite] = []
        self.transport_stations: List[FixedSite] = []
        self.other_sites: List[FixedSite] = []

        self.public_transports: List[PublicTransport] = []

        self.dummy_site = dummy_site

    @property
    def sites(self) -> List[Site]:
        return self.homes + self.businesses + self.stores + self.transport_stations + self.other_sites + self.public_transports


def create_sites():
    all_sites = AllSites()

    number_of_homes = 200
    number_of_businesses = 10

    number_of_public_transports = 1
    number_of_transport_stations = 5
    number_of_transport_stations_per_transport = 5

    city = BoundedArea()
    city.sites = []
    district = BoundedArea()
    district.sites = []

    for _ in range(number_of_homes):
        home = FixedSite()
        home.area = random.uniform(40, 60)
        home.nominal_capacity = random.randint(3,6)
        home.dispersion_factor = 1.0

        home.location = (random.uniform(-3, 3), random.uniform(-3, 3))
        home.is_outdoor = False
        home.essentiality = 1.0

        city.sites.append(home)
        district.sites.append(home)

        home.city = city
        home.district = district

        all_sites.homes.append(home)

    for _ in range(number_of_businesses):
        business = FixedSite()
        business.area = random.uniform(100, 300)
        business.nominal_capacity = random.randint(10,20)
        business.dispersion_factor = 1.0

        business.location = (random.normalvariate(0, 2), random.normalvariate(0, 2))
        business.is_outdoor = False
        business.essentiality = random.uniform(0, 1)

        city.sites.append(business)
        district.sites.append(business)

        business.city = city
        business.district = district

        all_sites.businesses.append(business)

    for _ in range(number_of_transport_stations):
        transport_station = TransportStation()
        transport_station.area = random.uniform(5, 20)
        transport_station.nominal_capacity = random.randint(10, 30)
        transport_station.dispersion_factor = 1.0

        transport_station.location = (random.uniform(-3, 3), random.uniform(-3, 3))
        transport_station.is_outdoor = True
        transport_station.essentiality = 0.2

        transport_station.public_transports = []

        city.sites.append(transport_station)
        district.sites.append(transport_station)

        transport_station.city = city
        transport_station.district = district

        all_sites.transport_stations.append(transport_station)

    for _ in range(number_of_public_transports):
        public_transport = PublicTransport()

        public_transport.area = random.uniform(5, 10)
        public_transport.nominal_capacity = random.randint(4, 10)
        public_transport.dispersion_factor = 1.0

        transport_station_shuffled = all_sites.transport_stations.copy()
        random.shuffle(transport_station_shuffled)
        transport_station_shuffled = transport_station_shuffled[:number_of_transport_stations_per_transport]

        public_transport.path = transport_station_shuffled + list(reversed(transport_station_shuffled[:-1]))
        for station in transport_station_shuffled:
            station.public_transports.append(public_transport)

        public_transport.start_times = []
        for day in range(5):
            for minutes in range(420, 30, 1201):
                public_transport.start_times.append((day, minutes))

        public_transport.travel_times = []
        for loc1, loc2 in zip(public_transport.path[:-1], public_transport.path[1:]):
            public_transport.travel_times.append(10.0)

        public_transport.current_station = None

        all_sites.public_transports.append(public_transport)

        return all_sites


def create_people(sites: AllSites):
    people = []

    number_of_houeholds = len(sites.homes)

    for i in range(number_of_houeholds):
        household = Household()
        household.people = []
        household.home = sites.homes[i]

        number_of_people_in_household = random.choices([1, 2, 3, 4, 5, 6], [0.05, 0.1, 0.2, 0.3, 0.25, 0.1])[0]
        for i in range(number_of_people_in_household):
            person = Person()
            household.people.append(person)
            if (i == 0):
                person.age = random.uniform(20, 80)
            elif i == 1:
                person.age = random.uniform(0, 80)
            else:
                person.age = random.uniform(0, 20)
            person.sex = Sex.FEMALE if random.random() < 0.5 else Sex.MALE
            if 18 <= person.age <= 70:
                person.occupation = PersonOccupation.WORKER
            elif 5 <= person.age < 18:
                person.occupation = PersonOccupation.STUDENT
            else:
                person.occupation = PersonOccupation.UNEMPLOYED
            person.household = household
            person.susceptibility_degree = 1.0
            person.sickness_degree = random.choices([0.0, 1.0], [0.9, 0.1])[0]
            person.symptoms_degree = random.uniform(0, 1)
            person.time_infected_minutes = random.uniform(0, 10000) if person.sickness_degree > 0 else None
            person.immunity_degree = 0.0
            person.abides_by_rules_degree = 0.0
            person.site = household.home
            person.time_in_current_site = 300
            person.current_commute = None
            person.current_commute_start_time = None

            person.commuting_patterns = []
            if person.occupation == PersonOccupation.WORKER:
                uses_public_transport = random.choices([True, False], [0.7, 0.3])[0]
                if not uses_public_transport:
                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_site_condition = [person.household.home]
                    commuting_pattern1.minutes_condition = (480.0, 540.0)
                    commuting_pattern1.day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_site_condition = None
                    commuting_pattern1.final_site_options = [random.choice(sites.businesses)]
                    commuting_pattern1.travel_time = random.uniform(20, 50)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_site_condition = commuting_pattern1.final_site_options
                    commuting_pattern2.minutes_condition = None
                    commuting_pattern2.day_condition = None
                    commuting_pattern2.time_in_site_condition = 540
                    commuting_pattern2.final_site_options = [household.home]
                    commuting_pattern2.travel_time = commuting_pattern1.travel_time
                    commuting_pattern2.probability_per_minute = 0.04

                    person.commuting_patterns.append(commuting_pattern1)
                    person.commuting_patterns.append(commuting_pattern2)
                else:
                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_site_condition = [person.household.home]
                    commuting_pattern1.minutes_condition = (480.0, 540.0)
                    commuting_pattern1.day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_site_condition = None
                    commuting_pattern1.final_site_options = [random.choice(sites.transport_stations)]
                    commuting_pattern1.travel_time = random.uniform(0, 10)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_site_condition = commuting_pattern1.final_site_options
                    commuting_pattern2.minutes_condition = None
                    commuting_pattern2.day_condition = None
                    commuting_pattern2.time_in_site_condition = None
                    commuting_pattern2.final_site_options = [
                        random.choice(commuting_pattern1.final_site_options[0].public_transports)]
                    commuting_pattern2.travel_time = 0
                    commuting_pattern2.probability_per_minute = 1

                    commuting_pattern3 = CommutingPattern()
                    commuting_pattern3.initial_site_condition = commuting_pattern2.final_site_options
                    commuting_pattern3.minutes_condition = None
                    commuting_pattern3.day_condition = None
                    commuting_pattern3.time_in_site_condition = None
                    commuting_pattern3.final_site_options = random.choice(
                        [station for station in commuting_pattern3.initial_site_condition[0].path if
                         station is not commuting_pattern2.initial_site_condition[0]])
                    commuting_pattern3.travel_time = 0
                    commuting_pattern3.probability_per_minute = 1

                    commuting_pattern4 = CommutingPattern()
                    commuting_pattern4.initial_site_condition = commuting_pattern3.final_site_options
                    commuting_pattern4.minutes_condition = None
                    commuting_pattern4.day_condition = None
                    commuting_pattern4.time_in_site_condition = None
                    commuting_pattern4.final_site_options = random.choice(sites.businesses)
                    commuting_pattern4.travel_time = random.uniform(0, 10)
                    commuting_pattern4.probability_per_minute = 1

                    commuting_pattern5 = CommutingPattern()
                    commuting_pattern5.initial_site_condition = commuting_pattern4.final_site_options
                    commuting_pattern5.minutes_condition = None
                    commuting_pattern5.day_condition = None
                    commuting_pattern5.time_in_site_condition = 540
                    commuting_pattern5.final_site_options = commuting_pattern4.initial_site_condition
                    commuting_pattern5.travel_time = commuting_pattern4.travel_time
                    commuting_pattern5.probability_per_minute = 0.04

                    commuting_pattern6 = CommutingPattern()
                    commuting_pattern6.initial_site_condition = commuting_pattern5.final_site_options
                    commuting_pattern6.minutes_condition = None
                    commuting_pattern6.day_condition = None
                    commuting_pattern6.time_in_site_condition = None
                    commuting_pattern6.final_site_options = commuting_pattern2.final_site_options
                    commuting_pattern6.travel_time = 0
                    commuting_pattern6.probability_per_minute = 1

                    commuting_pattern7 = CommutingPattern()
                    commuting_pattern7.initial_site_condition = commuting_pattern6.final_site_options
                    commuting_pattern7.minutes_condition = None
                    commuting_pattern7.day_condition = None
                    commuting_pattern7.time_in_site_condition = None
                    commuting_pattern7.final_site_options = commuting_pattern2.initial_site_condition
                    commuting_pattern7.travel_time = 0
                    commuting_pattern7.probability_per_minute = 1

                    commuting_pattern8 = CommutingPattern()
                    commuting_pattern8.initial_site_condition = commuting_pattern7.final_site_options
                    commuting_pattern8.minutes_condition = None
                    commuting_pattern8.day_condition = None
                    commuting_pattern8.time_in_site_condition = None
                    commuting_pattern8.final_site_options = [household.home]
                    commuting_pattern8.travel_time = commuting_pattern1.travel_time
                    commuting_pattern8.probability_per_minute = 1

                    person.commuting_patterns.append(commuting_pattern1)
                    person.commuting_patterns.append(commuting_pattern2)
                    person.commuting_patterns.append(commuting_pattern3)
                    person.commuting_patterns.append(commuting_pattern4)
                    person.commuting_patterns.append(commuting_pattern5)
                    person.commuting_patterns.append(commuting_pattern6)
                    person.commuting_patterns.append(commuting_pattern7)
                    person.commuting_patterns.append(commuting_pattern8)

            people.append(person)

    return people