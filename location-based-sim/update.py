from person import Person
from timing import datetime


def update_people(people, policy, time, time_step):
    for person in people:
        move_person(person, policy, time, time_step)


def move_person(person: Person, policy, time: datetime, time_step):
    if person.is_in_dummy_site:
        if time >= person.next_site_time:
            new_site = person.next_site
            person.change_site(new_site)
        return
    else:
        out = None
        for commuting_patten in person.commuting_patterns:
            out = commuting_patten.apply(person.site, time, person.time_in_current_site, time_step)
            if out is not None:
                new_site, next_site_time = out[0], out[1]
                break
        if out is None:
            return
        else:
            if new_site == person.site:
                return
            elif next_site_time > time:
                person.put_in_dummy_site(new_site, next_site_time)
            else:
                person.change_site(new_site)