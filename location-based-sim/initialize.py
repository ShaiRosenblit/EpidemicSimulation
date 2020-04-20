"""
functions to populate world we sites and people
"""
import random
from typing import List

from commuting_pattern import CommutingPattern
from person import Household, Person, PersonOccupation, Sex
from sites import BoundedArea, FixedSite, PublicTransport, Site, \
    TransportStation, dummy_site


class AllSites:
    """
    this class will used to keep track of all site types.
    """

    def __init__(self):
        self.cities: List[BoundedArea] = []
        self.districts: List[BoundedArea] = []

        # people live in these places
        self.homes: List[FixedSite] = []

        # people work at these places
        self.businesses: List[FixedSite] = []

        # stations for public transportation
        self.transport_stations: List[FixedSite] = []

        # other types of sites
        self.other_sites: List[FixedSite] = []

        # public transportation vehicles
        self.public_transports: List[PublicTransport] = []

        # the singleton dummy site
        self.dummy_site = dummy_site

        self.households : List[Household] = []

    @property
    def sites(self) -> List[Site]:
        """
        get collection of all sites (excluding the dummy site)
        """
        return self.homes + self.businesses + self.transport_stations + \
               self.other_sites + self.public_transports


def create_sites():
    """
    create all sites. this function can be changed to obtain a more realistic
    distribution of sites, for example by using shape files of GIS data.
    """
    all_sites = AllSites()

    # number of places were people live
    number_of_homes = 300

    # numebr of places where people work
    number_of_businesses = 20

    number_of_public_transports = 0
    number_of_transport_stations = 0
    number_of_transport_stations_per_transport = 5

    # we will have one city, and one district (and they will be identical...)
    city = BoundedArea()
    city.sites = []
    district = BoundedArea()
    district.sites = []

    # create all homes
    for _ in range(number_of_homes):
        home = FixedSite()

        # effective area of home
        home.area = random.uniform(40, 60)

        # number of people the home can contain in nominal conditions
        home.nominal_capacity = random.randint(3, 6)

        home.dispersion_factor = 1.0
        home.is_outdoor = False
        home.essentiality = 1.0

        # choose location ((x,y) coordinates) uniformly in the plane
        home.location = (random.uniform(-300, 300), random.uniform(-300, 300))

        # add to the city and district
        city.sites.append(home)
        district.sites.append(home)

        # set the city and district of this site
        home.city = city
        home.district = district

        # update collection og all homes
        all_sites.homes.append(home)

    # create all businesses
    for _ in range(number_of_businesses):
        business = FixedSite()

        # effective area of business
        business.area = random.uniform(100, 300)

        # number of people the business can contain in nominal conditions
        business.nominal_capacity = random.randint(10, 20)

        business.dispersion_factor = 1.0
        business.is_outdoor = False
        business.essentiality = random.uniform(0, 1)

        # choose location ((x,y) coordinates) with higher density in the center
        business.location = (
            random.normalvariate(0, 100), random.normalvariate(0, 100))

        # add to the city and district
        city.sites.append(business)
        district.sites.append(business)

        # set the city and district of this site
        business.city = city
        business.district = district

        all_sites.businesses.append(business)

    # add public transport stations
    for _ in range(number_of_transport_stations):
        transport_station = TransportStation()
        transport_station.area = random.uniform(5, 20)
        transport_station.nominal_capacity = random.randint(10, 30)
        transport_station.dispersion_factor = 1.0

        transport_station.location = (
            random.uniform(-3, 3), random.uniform(-3, 3))
        transport_station.is_outdoor = True
        transport_station.essentiality = 0.2

        transport_station.public_transports = []

        city.sites.append(transport_station)
        district.sites.append(transport_station)

        transport_station.city = city
        transport_station.district = district

        all_sites.transport_stations.append(transport_station)

    # add public transport lines
    for _ in range(number_of_public_transports):
        public_transport = PublicTransport()

        # effective area of vehicle
        public_transport.area = random.uniform(5, 10)

        # number of people the vehicle can contain in nominal conditions
        public_transport.nominal_capacity = random.randint(4, 10)

        public_transport.dispersion_factor = 1.0

        # find the path of the line, by sorting all public transport stations
        transport_station_shuffled = all_sites.transport_stations.copy()
        random.shuffle(transport_station_shuffled)
        transport_station_shuffled = transport_station_shuffled[
                                     :number_of_transport_stations_per_transport]

        # we will make the line do a round-trip (back and forth)
        public_transport.path = transport_station_shuffled + list(
            reversed(transport_station_shuffled[:-1]))

        # update the stations to include a pointer to this line
        for station in transport_station_shuffled:
            station.public_transports.append(public_transport)

        # which times of the week the line starts its route
        public_transport.start_times = []
        for day in range(5):
            for minutes in range(420, 30, 1201):
                public_transport.start_times.append((day, minutes))

        # time it takes to travel between each two stations
        public_transport.travel_times = []
        for loc1, loc2 in zip(public_transport.path[:-1],
                              public_transport.path[1:]):
            public_transport.travel_times.append(10.0)

        public_transport.current_station = None

        all_sites.public_transports.append(public_transport)

    return all_sites


def create_people(sites: AllSites):
    """
    create all people. this function can be changed to obtain a more
    realistic distribution of people, by using demographic data.
    """

    # this will be the collection of all people
    people = []

    number_of_houeholds = len(sites.homes)

    # we will loop over all homes, and for each home we will choose a random
    # number of inhabitants
    for i in range(number_of_houeholds):

        # create household for the current home
        household = Household()
        sites.households.append(household)
        household.people = []
        household.home = sites.homes[i]

        # choose how many people live in this home
        number_of_people_in_household = \
            random.choices([1, 2, 3, 4, 5, 6],
                           [0.05, 0.1, 0.2, 0.3, 0.25, 0.1])[0]

        # create each of the people who live in the house
        for i in range(number_of_people_in_household):
            person = Person()
            household.people.append(person)

            if (i == 0):
                # if this is the first person - it is an adult
                person.age = random.uniform(20, 80)

            elif i == 1:
                # if this is the second person - it is either an adult or
                # a child
                person.age = random.uniform(0, 80)
            else:
                # choose child
                person.age = random.uniform(0, 20)

            person.sex = Sex.FEMALE if random.random() < 0.5 else Sex.MALE

            # choose occupation of person
            if 18 <= person.age <= 70:
                person.occupation = PersonOccupation.WORKER
            elif 5 <= person.age < 18:
                person.occupation = PersonOccupation.STUDENT
            else:
                person.occupation = PersonOccupation.UNEMPLOYED

            # set household of person
            person.household = household
            person.susceptibility_degree = 1.0

            # choose whether ill or healthy
            person.illness_degree = random.choices([0.0, 1.0], [0.98, 0.02])[0]

            # choose whether has symptoms
            person.symptoms_degree = 0.0 if (person.illness_degree == 0.0) else random.uniform(0, 1)

            # choose how long infected
            person.time_infected_minutes = random.uniform(0,10000) if \
                person.illness_degree > 0 else None

            # set other parameters
            person.immunity_degree = 0.0
            person.abides_by_rules_degree = 0.0
            person.site = household.home
            person.site.people.append(person)
            person.time_in_current_site = 300
            person.current_commute = None
            person.current_commute_start_time = None

            # we now choose commting patterns for the person.
            # we will add commuting patterns only to people who are workers.
            # we will have two cases: use public transport or not.
            # if not - use two patterns, one for the trip to work and one
            # for return.
            # otherwise, use eight patters, for for each direction. the patterns
            # will be: go to station, get on transport, get off at station, go
            # to destination

            person.commuting_patterns = []
            if person.occupation == PersonOccupation.WORKER:

                # check if uses public transport
                uses_public_transport = False
                # uses_public_transport = \
                #     random.choices([True, False], [0.0, 1.0])[0]

                if not uses_public_transport:
                    # doesn't use public transport.

                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_site_condition = [
                        person.household.home]
                    commuting_pattern1.minutes_condition = (480.0, 540.0)
                    commuting_pattern1.day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_site_condition = None
                    commuting_pattern1.final_site_options = [
                        random.choice(sites.businesses)]
                    commuting_pattern1.travel_time = random.uniform(20, 50)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_site_condition = \
                        commuting_pattern1.final_site_options
                    commuting_pattern2.minutes_condition = None
                    commuting_pattern2.day_condition = None
                    commuting_pattern2.time_in_site_condition = 540
                    commuting_pattern2.final_site_options = [household.home]
                    commuting_pattern2.travel_time = \
                        commuting_pattern1.travel_time
                    commuting_pattern2.probability_per_minute = 0.04

                    person.commuting_patterns.append(commuting_pattern1)
                    person.commuting_patterns.append(commuting_pattern2)
                else:
                    # uses public transport.

                    commuting_pattern1 = CommutingPattern()
                    commuting_pattern1.initial_site_condition = [
                        person.household.home]
                    commuting_pattern1.minutes_condition = (480.0, 540.0)
                    commuting_pattern1.day_condition = [0, 1, 2, 3, 4, 5]
                    commuting_pattern1.time_in_site_condition = None
                    commuting_pattern1.final_site_options = [
                        random.choice(sites.transport_stations)]
                    commuting_pattern1.travel_time = random.uniform(0, 10)
                    commuting_pattern1.probability_per_minute = 0.01

                    commuting_pattern2 = CommutingPattern()
                    commuting_pattern2.initial_site_condition = \
                        commuting_pattern1.final_site_options
                    commuting_pattern2.minutes_condition = None
                    commuting_pattern2.day_condition = None
                    commuting_pattern2.time_in_site_condition = None
                    commuting_pattern2.final_site_options = [
                        random.choice(commuting_pattern1.final_site_options[
                                          0].public_transports)]
                    commuting_pattern2.travel_time = 0
                    commuting_pattern2.probability_per_minute = 1

                    commuting_pattern3 = CommutingPattern()
                    commuting_pattern3.initial_site_condition = \
                        commuting_pattern2.final_site_options
                    commuting_pattern3.minutes_condition = None
                    commuting_pattern3.day_condition = None
                    commuting_pattern3.time_in_site_condition = None
                    commuting_pattern3.final_site_options = random.choice(
                        [station for station in
                         commuting_pattern3.initial_site_condition[0].path if
                         station is not
                         commuting_pattern2.initial_site_condition[0]])
                    commuting_pattern3.travel_time = 0
                    commuting_pattern3.probability_per_minute = 1

                    commuting_pattern4 = CommutingPattern()
                    commuting_pattern4.initial_site_condition = \
                        commuting_pattern3.final_site_options
                    commuting_pattern4.minutes_condition = None
                    commuting_pattern4.day_condition = None
                    commuting_pattern4.time_in_site_condition = None
                    commuting_pattern4.final_site_options = random.choice(
                        sites.businesses)
                    commuting_pattern4.travel_time = random.uniform(0, 10)
                    commuting_pattern4.probability_per_minute = 1

                    commuting_pattern5 = CommutingPattern()
                    commuting_pattern5.initial_site_condition = \
                        commuting_pattern4.final_site_options
                    commuting_pattern5.minutes_condition = None
                    commuting_pattern5.day_condition = None
                    commuting_pattern5.time_in_site_condition = 540
                    commuting_pattern5.final_site_options = \
                        commuting_pattern4.initial_site_condition
                    commuting_pattern5.travel_time = \
                        commuting_pattern4.travel_time
                    commuting_pattern5.probability_per_minute = 0.04

                    commuting_pattern6 = CommutingPattern()
                    commuting_pattern6.initial_site_condition = \
                        commuting_pattern5.final_site_options
                    commuting_pattern6.minutes_condition = None
                    commuting_pattern6.day_condition = None
                    commuting_pattern6.time_in_site_condition = None
                    commuting_pattern6.final_site_options = \
                        commuting_pattern2.final_site_options
                    commuting_pattern6.travel_time = 0
                    commuting_pattern6.probability_per_minute = 1

                    commuting_pattern7 = CommutingPattern()
                    commuting_pattern7.initial_site_condition = \
                        commuting_pattern6.final_site_options
                    commuting_pattern7.minutes_condition = None
                    commuting_pattern7.day_condition = None
                    commuting_pattern7.time_in_site_condition = None
                    commuting_pattern7.final_site_options = \
                        commuting_pattern2.initial_site_condition
                    commuting_pattern7.travel_time = 0
                    commuting_pattern7.probability_per_minute = 1

                    commuting_pattern8 = CommutingPattern()
                    commuting_pattern8.initial_site_condition = \
                        commuting_pattern7.final_site_options
                    commuting_pattern8.minutes_condition = None
                    commuting_pattern8.day_condition = None
                    commuting_pattern8.time_in_site_condition = None
                    commuting_pattern8.final_site_options = [household.home]
                    commuting_pattern8.travel_time = \
                        commuting_pattern1.travel_time
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
