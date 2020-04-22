
class Meeting:
    """
    Represents a single Meeting between two or more people
    """
    def __init__(self, person1, person2, site, time):
        # date and time of the meeting
        self._time = time
        # list of the people involved in the meeting
        self._people_involved = [person1, person2]
        # the site in which the meeting happened
        self._location = site

    def __repr__(self):
        string = "Meeting(Location: {0} \n \t person1: {1} \n \t person2: {2} \n \t meeting time: {3} \n \t is meeting infected: {4}".format(
            self._location, str(self._people_involved[0]), str(self._people_involved[1]), self._time, self.is_meeting_infected()
        )
        return string

    def __str__(self):
        string = "Meeting(Location: {0} \n person1: {1} \n person2: {2} \n meeting time: {3} \n is meeting infected: {4}".format(
            self._location, str(self._people_involved[0]), str(self._people_involved[1]), self._time,
            self.is_meeting_infected()
        )
        return string

    def update_log(self):
        """
        writes down the meeting object in a log.txt file
        work in progress.
        """
        pass

    def is_meeting_infected(self):
        """
        checks if one of the people in the meeting is infected.
        :return boolean
        """
        return self._people_involved[1].is_infected or self._people_involved[0].is_infected


