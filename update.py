from person import Person
from timing import datetime


def move_people(people, policy, time):
    for person in people:
        update_person(person, policy, time)


def update_person(person: Person, policy, time: datetime, time_step):
    if person.is_in_dummy_location:
        if time >= person.next_location_time:
            new_location = person.next_location
            person.is_in_dummy_location = False

    out = None
    for commuting_patten in person.commuting_patterns:
        out = commuting_patten.apply(person.location, time, person.time_in_current_location, time_step)
        if out is not None:
            final_location, final_time = out[0], out[1]
            break
    if out is not None:
        pass
