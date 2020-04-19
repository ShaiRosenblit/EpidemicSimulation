from initialize import create_sites, create_people
from timing import time_iter
from update import update_people

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
