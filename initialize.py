import random
from typing import List

from commuting_pattern import CommutingPattern
from location import Location, FixedLocation, PublicTransport, TransportStation, BoundedArea, DummyLocation
from person import Sex, PersonOccupation, Household, Person


class AllLocations:
    def __init__(self):
        self.cities: List[BoundedArea] = []
        self.districts: List[BoundedArea] = []

        self.homes: List[FixedLocation] = []
        self.businesses: List[FixedLocation] = []
        self.stores: List[FixedLocation] = []
        self.transport_stations: List[FixedLocation] = []
        self.other_locations: List[FixedLocation] = []

        self.public_transports: List[PublicTransport] = []

        self.dummy_location = DummyLocation()

    @property
    def locations(self) -> List[Location]:
        return self.homes + self.businesses + self.stores + self.transport_stations + self.other_locations + self.public_transports


def create_locations():
    all_locations = AllLocations()

    number_of_homes = 200
    number_of_businesses = 10

    number_of_public_transports = 1
    number_of_transport_stations = 5
    number_of_transport_stations_per_transport = 5

    city = BoundedArea()
    city.locations = []
    district = BoundedArea()
    district.locations = []

    for _ in range(number_of_homes):
        home = FixedLocation()
        home.area = random.uniform(40, 60)
        home.dispression_factor = 1.0

        home.coordinates = (random.uniform(-3, 3), random.uniform(-3, 3))
        home.is_outdoor = False
        home.essentiality = 1.0

        city.locations.append(home)
        district.locations.append(home)

        home.city = city
        home.district = district

        all_locations.homes.append(home)

    for _ in range(number_of_businesses):
        business = FixedLocation()
        business.area = random.uniform(100, 300)
        business.dispression_factor = 1.0

        business.coordinates = (random.normalvariate(0, 2), random.normalvariate(0, 2))
        business.is_outdoor = False
        business.essentiality = random.uniform(0, 1)

        city.locations.append(business)
        district.locations.append(business)

        business.city = city
        business.district = district

        all_locations.businesses.append(business)

    for _ in range(number_of_transport_stations):
        transport_station = TransportStation()
        transport_station.area = random.uniform(5, 20)
        transport_station.dispression_factor = 1.0

        transport_station.coordinates = (random.uniform(-3, 3), random.uniform(-3, 3))
        transport_station.is_outdoor = True
        transport_station.essentiality = 0.2

        transport_station.public_transports = []

        city.locations.append(transport_station)
        district.locations.append(transport_station)

        transport_station.city = city
        transport_station.district = district

        all_locations.transport_stations.append(transport_station)

    for _ in range(number_of_public_transports):
        public_transport = PublicTransport()

        public_transport.area = random.uniform(5, 10)
        public_transport.dispression_factor = 1.0

        transport_station_shuffled = all_locations.transport_stations.copy()
        random.shuffle(transport_station_shuffled)
        transport_station_shuffled = transport_station_shuffled[:number_of_transport_stations_per_transport]

        public_transport.path = transport_station_shuffled + list(reversed(transport_station_shuffled[:-1]))
        for station in transport_station_shuffled:
            station.public_transports.append(public_transport)

        public_transport.start_times = []
        for day in range(5):
            for minutes in range(420, 30, 1201):
                public_transport.start_times.append(Time(day, minutes))

        public_transport.travel_times = []
        for loc1, loc2 in zip(public_transport.path[:-1], public_transport.path[1:]):
            public_transport.travel_times.append(10.0)

        public_transport.current_station = None

        all_locations.public_transports.append(public_transport)

        return all_locations


def create_people(locations: AllLocations):
    people = []

    number_of_houeholds = len(locations.homes)

    for i in range(number_of_houeholds):
        household = Household()
        household.people = []
        household.home = locations.homes[i]

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
            person.time_sick_minutes = random.uniform(0, 10000) if person.sickness_degree > 0 else None
            person.immunity_degree = 0.0
            person.wears_mask_probability = 0.0
            person.keeps_distance_probability = 0.0
            person.washes_hands_probability = 0.0
            person.obeys_quarantine_probability = 0.0
            person.abides_by_rules_probability = 0.0
            person.trackable_probability = 0.0
            person.location = household.home
            person.time_in_current_location = 300
            person.current_commute = None
            person.current_commute_start_time = None

            person.commuting_patterns = []
            if person.occupation == PersonOccupation.WORKER:
                uses_public_transport = random.choices([True, False], [0.7, 0.3])[0]
                if not uses_public_transport:
                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_location_condition = [person.household.home]
                    commuting_pattern1.initial_minutes_condition = (480.0, 540.0)
                    commuting_pattern1.initial_day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_location_condition = None
                    commuting_pattern1.final_location_options = [random.choice(locations.businesses)]
                    commuting_pattern1.travel_time = random.uniform(20, 50)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_location_condition = commuting_pattern1.final_location_options
                    commuting_pattern2.initial_minutes_condition = None
                    commuting_pattern2.initial_day_condition = None
                    commuting_pattern2.time_in_location_condition = 540
                    commuting_pattern2.final_location_options = [household.home]
                    commuting_pattern2.travel_time = commuting_pattern1.travel_time
                    commuting_pattern2.probability_per_minute = 0.04

                    person.commuting_patterns.append(commuting_pattern1)
                    person.commuting_patterns.append(commuting_pattern2)
                else:
                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_location_condition = [person.household.home]
                    commuting_pattern1.initial_minutes_condition = (480.0, 540.0)
                    commuting_pattern1.initial_day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_location_condition = None
                    commuting_pattern1.final_location_options = [random.choice(locations.transport_stations)]
                    commuting_pattern1.travel_time = random.uniform(0, 10)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_location_condition = commuting_pattern1.final_location_options
                    commuting_pattern2.initial_minutes_condition = None
                    commuting_pattern2.initial_day_condition = None
                    commuting_pattern2.time_in_location_condition = None
                    commuting_pattern2.final_location_options = [
                        random.choice(commuting_pattern1.final_location_options[0].public_transports)]
                    commuting_pattern2.travel_time = 0
                    commuting_pattern2.probability_per_minute = 1

                    commuting_pattern3 = CommutingPattern()
                    commuting_pattern3.initial_location_condition = commuting_pattern2.final_location_options
                    commuting_pattern3.initial_minutes_condition = None
                    commuting_pattern3.initial_day_condition = None
                    commuting_pattern3.time_in_location_condition = None
                    commuting_pattern3.final_location_options = random.choice(
                        [station for station in commuting_pattern3.initial_location_condition[0].path if
                         station is not commuting_pattern2.initial_location_condition[0]])
                    commuting_pattern3.travel_time = 0
                    commuting_pattern3.probability_per_minute = 1

                    commuting_pattern4 = CommutingPattern()
                    commuting_pattern4.initial_location_condition = commuting_pattern3.final_location_options
                    commuting_pattern4.initial_minutes_condition = None
                    commuting_pattern4.initial_day_condition = None
                    commuting_pattern4.time_in_location_condition = None
                    commuting_pattern4.final_location_options = random.choice(locations.businesses)
                    commuting_pattern4.travel_time = random.uniform(0, 10)
                    commuting_pattern4.probability_per_minute = 1

                    commuting_pattern5 = CommutingPattern()
                    commuting_pattern5.initial_location_condition = commuting_pattern4.final_location_options
                    commuting_pattern5.initial_minutes_condition = None
                    commuting_pattern5.initial_day_condition = None
                    commuting_pattern5.time_in_location_condition = 540
                    commuting_pattern5.final_location_options = commuting_pattern4.initial_location_condition
                    commuting_pattern5.travel_time = commuting_pattern4.travel_time
                    commuting_pattern5.probability_per_minute = 0.04

                    commuting_pattern6 = CommutingPattern()
                    commuting_pattern6.initial_location_condition = commuting_pattern5.final_location_options
                    commuting_pattern6.initial_minutes_condition = None
                    commuting_pattern6.initial_day_condition = None
                    commuting_pattern6.time_in_location_condition = None
                    commuting_pattern6.final_location_options = commuting_pattern2.final_location_options
                    commuting_pattern6.travel_time = 0
                    commuting_pattern6.probability_per_minute = 1

                    commuting_pattern7 = CommutingPattern()
                    commuting_pattern7.initial_location_condition = commuting_pattern6.final_location_options
                    commuting_pattern7.initial_minutes_condition = None
                    commuting_pattern7.initial_day_condition = None
                    commuting_pattern7.time_in_location_condition = None
                    commuting_pattern7.final_location_options = commuting_pattern2.initial_location_condition
                    commuting_pattern7.travel_time = 0
                    commuting_pattern7.probability_per_minute = 1

                    commuting_pattern8 = CommutingPattern()
                    commuting_pattern8.initial_location_condition = commuting_pattern7.final_location_options
                    commuting_pattern8.initial_minutes_condition = None
                    commuting_pattern8.initial_day_condition = None
                    commuting_pattern8.time_in_location_condition = None
                    commuting_pattern8.final_location_options = [household.home]
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
