from typing import List

from person import Person
from sites import Site
from timing import datetime
from initialize import AllSites


class MetricManager:
    def __init__(self, people: List[Person], sites: AllSites):
        self.people = people
        self.sites = sites

    def get_sir_proportions(self):
        s = 0
        i = 0
        r = 0
        for person in self.people:
            if person.illness_degree > 0:
                i += 1
            elif person.immunity_degree > 0:
                r += 1
            else:
                s += 1

        tot = s + i + r
        return s / tot, i / tot, r / tot

    def show(self, time:datetime):
        s,i,r = self.get_sir_proportions()
        print(time)
        print('S: {:6.2f}%   I: {:6.2f}%   R: {:6.2f}%'.format(s*100,i*100,r*100))
        print('')