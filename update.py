from person import Person
from timing import datetime


def move_people(people, policy, time):
    for person in people:
        update_person(person, policy, time)


def update_person(person: Person, policy, time: datetime, time_step):
    if person.is_in_dummy_site:
        if time >= person.next_site_time:
            new_site = person.next_site
            person.is_in_dummy_site = False

    out = None
    for commuting_patten in person.commuting_patterns:
        out = commuting_patten.apply(person.site, time, person.time_in_current_site, time_step)
        if out is not None:
            final_site, final_time = out[0], out[1]
            break
    if out is not None:
        pass
