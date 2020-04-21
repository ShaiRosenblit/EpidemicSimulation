from timing import datetime
from person import Person
from sites import Site


class Meeting:
    """
    Represents a single Meeting between two or more people
    """
    def __init__(self):
        # date and time of the meeting
        self._time: datetime = None
        # list of the people involved in the meeting
        self._people_involved: tuple = None
        # the site in which the meeting happened
        self._location: Site = None

    def __repr__(self):
        string = "Meeting(Location: {0} \n \t person1: {1} \n \t person2: {2} \n \t meeting time: {3} \n \t is meeting infected: {4}".format(
            self._location, str(self._people_involved[0]), str(self._people_involved[1]), self._time, self.is_infected_in_meeting()
        )
        return string

    def __str__(self):
        string = "Meeting(Location: {0} \n person1: {1} \n person2: {2} \n meeting time: {3} \n is meeting infected: {4}".format(
            self._location, str(self._people_involved[0]), str(self._people_involved[1]), self._time,
            self.is_infected_in_meeting()
        )
        return string

    def create_meeting(self, person1: Person, person2: Person, site: Site):
        """
        creates a new meeting object.
        :param person1 - first person in the meeting
        :param person2 - second person in the meeting
        :param site - the location of the meeting
        """
        meeting = Meeting()
        meeting._people_involved = (person1, person2)
        meeting._location = site
        return meeting

    def update_log(self):
        """
        writes down the meeting object in a log.txt file
        work in progress.
        """
        pass

    def is_infected_in_meeting(self):
        """
        checks if one of the people in the meeting is infected.
        :return boolean
        """
        if self._people_involved[1].time_infected is not None or self._people_involved[0].time_infected is not None:
            return True
        return False

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, time):
        """
        updates the _time value of the meeting
        """
        if isinstance(time, datetime):
            self._time = time
        else:
            raise ValueError("expected 'datetime' object recieved {} type".format(type(time)))
