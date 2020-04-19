from initialize import create_locations, create_people
from timing import time_iter
from update import move_people

locations = create_locations()
people = create_people(locations)

metrics = MetricsObject(people, locations)
display = DisplayObject(people, locations)
policy = PolicyObject(people, locations)

time_step = 5

for step, time in enumerate(time_iter(time_step)):
    metrics.update(people, locations, step)
    display.update(people, locations, step)
    policy.update(people, locations, metrics)
    move_public_transports(locations, policy, time)
    move_people(people, policy, time)
    update_people_status(locations, time)
