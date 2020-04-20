from typing import List
from math import sqrt

import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

from initialize import AllSites
from person import Person
from timing import datetime


class DisplayManager:
    def __init__(self, people: List[Person], sites: AllSites):

        self.people = people
        self.sites = sites

        self.fig = plt.figure(figsize=(6, 6), facecolor='black',
                              edgecolor='black', frameon=True)
        self.ax = plt.axes(facecolor='black', frameon=False, xticks=[],
                           yticks=[], aspect='equal')

        minx = float('inf')
        maxx = -1 * float('inf')
        miny = float('inf')
        maxy = -1 * float('inf')

        self.home_circles = []
        for home in sites.homes:
            circ = plt.Circle(
                xy=home.location,
                radius=sqrt(home.area / 3.14 )*3,
                linewidth=0,
                facecolor='white',
                edgecolor=(0.5,0.5,0.5,1.0),
                alpha=0.8,
                axes=self.ax,
            )
            self.ax.add_artist(circ)
            self.home_circles.append(circ)

            minx = min(minx, home.location[0])
            maxx = max(maxx, home.location[0])
            miny = min(miny, home.location[1])
            maxy = max(maxy, home.location[1])

        self.business_squares = []
        for business in sites.businesses:
            sqr = plt.Rectangle(
                xy=business.location,
                width=sqrt(business.area)*3,
                height=sqrt(business.area)*3,
                linewidth=0,
                facecolor='white',
                edgecolor=(0.5,0.5,0.5,1.0),
                alpha=0.8,
                axes=self.ax
            )
            self.ax.add_artist(sqr)
            self.business_squares.append(sqr)

            minx = min(minx, business.location[0])
            maxx = max(maxx, business.location[0])
            miny = min(miny, business.location[1])
            maxy = max(maxy, business.location[1])

        dx = (maxx - minx) * 0.05
        dy = (maxy - miny) * 0.05
        self.ax.set_xlim(minx - dx, maxx + dx)
        self.ax.set_ylim(miny - dy, maxy + dy)

        self.time_txt = plt.text(
            x=minx,
            y=maxy,
            s='',
            fontdict={
                'color': 'white',
                'size' : 12
            }
        )

    def update(self, time: datetime):
        self.time_txt.set_text(str(time))

        cmap = LinearSegmentedColormap.from_list('my_cmap',['blue','red'])

        for home, circ in zip(self.sites.homes, self.home_circles):

            if len(home.people) == 0:
                circ.set_facecolor(None)
                circ.set_fill(False)
            else:
                infected = sum(
                    person.illness_degree > 0 for person in home.people)
                infected = infected / len(home.people)
                circ.set_fill(True)
                circ.set_facecolor(cmap(infected))
            circ.set_linewidth((1 + len(home.people)) / 3)

        for business, sqr in zip(self.sites.businesses, self.business_squares):

            if len(business.people) == 0:
                sqr.set_facecolor(None)
                sqr.set_fill(False)
            else:
                infected = sum(
                    person.illness_degree > 0 for person in business.people)
                infected = infected / len(business.people)
                sqr.set_fill(True)
                sqr.set_facecolor(cmap(infected))
            sqr.set_linewidth((1 + len(business.people)) / 20)

        plt.draw()
        plt.pause(0.001)
