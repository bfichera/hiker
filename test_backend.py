from dateparser import parse

import hiking_planner.backend.sites as sites
import hiking_planner.backend.events as events

# define sites
starttrailhead = sites.StartTrailhead(0)
endtrailhead = sites.EndTrailhead(100, 0)
campsite1 = sites.Site(10, 20)
campsite2 = sites.Site(20, 200)

# define events
starttrailhead_event = events.StartTrailheadEvent(
    parse('in 10 days'),
    starttrailhead,
)
endtrailhead_event = events.EndTrailheadEvent(
    parse('in 17 days'),
    endtrailhead,
)
stay1 = events.Stay(
    campsite1,
    parse('in 11 days'),
    parse('in 12 days'),
)
stay2 = events.Stay(
    campsite2,
    parse('in 13 days'),
    parse('in 14 days'),
)

itinerary = sites.Itinerary(
    starttrailhead_event,
    endtrailhead_event,
    [stay1, stay2],
)
