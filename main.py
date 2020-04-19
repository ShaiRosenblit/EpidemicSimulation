"""
Simulation of epidemic.
The two most important classes are: `Site` and `Person`.
A `Site` object can represent any type of "place" - a house, a shopping mall,
an office building, a bus. A `Site` contains, at each instant in time, a list of
`Person`s who are currently present in the `Site`. Given this list, and given
the site's characteristics (such as the effective area of the site),
the simulation calculates the new state of each `Person`. The state of a
`Person` measures the magnitude of the infection in the
`Person`. A `Person` has multiple characteristics that affect its chances of
infecting and getting infected. Another important property of a  `Person` is
its `CommutingPattern`s. Each `CommutingPattern` instance describes some
tendency of the `Person` to commute. For example, a `CommutingPattern` can
define that the `Person` goes from its home `Site` to its work `Site` everyday
at a specific time.

The master loop of the simulation is roughly the following:
for each time step:
    move each `Person` from `Site` to `Site` according to its commuting patterns.
    for each `Site`:
        update the infection status for all `Person`s in the `Site`
"""
from initialize import create_people, create_sites

sites = create_sites()
people = create_people(sites)
#
# metrics = MetricsObject(people, sites)
# display = DisplayObject(people, sites)
# policy = PolicyObject(people, sites)
#
# time_step = 5
#
# for step, time in enumerate(time_iter(time_step)):
#     metrics.update(people, sites, step)
#     display.update(people, sites, step)
#     policy.update(people, sites, metrics)
#     move_public_transports(sites.public_transports, policy, time, time_step)
#     move_people(people, policy, time)
#     update_people_status(sites, time)
