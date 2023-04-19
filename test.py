import urwid

from hiking_planner.backend import sites, events
from hiking_planner.cui.widgets import ChoiceWidget

COLUMN_SPAN = 20

class Planner:

    def __init__(self, root, itinerary):
        self.root = root

        for content in itinerary.traverse():
            if isinstance(content, events.StartTrailheadEvent):
                text = content.site.text
            elif isinstance(content, events.Stay):
                text = content.site.text
            elif isinstance(content, events.EndTrailheadEvent):
                text = content.site.text
            elif isinstance(content, sites.Route):
                text = content.text
            line_height = len(text.splitlines())
            button = root.add_button(
                text,
                counter,
                0,
                row_span=line_height,
                column_span=100,
                padx=2,
                pady=2,
                command=None,
            )
            counter += line_height

def ui(itinerary):

    choices = []
    for item in itinerary.traverse():
        if isinstance(item, sites.Route):
            lines = item.text.splitlines()
            prefix = '\t\n'
        else:
            lines = item.site.text.splitlines()
            prefix = '\t\t\n'
        choices.append(prefix.join(lines))
    for c in choices:
        print(c)
    input()

    txt = urwid.Text(choices)
    fill = urwid.Filler(txt, 'top')
    loop = urwid.MainLoop(fill)
    loop.run()

if __name__ == '__main__':
    from dateparser import parse

    import hiking_planner.backend.sites as sites
    import hiking_planner.backend.events as events

    # define sites
    starttrailhead = sites.StartTrailhead(0)
    endtrailhead = sites.EndTrailhead(100, 0)
    campsite1 = sites.Site(10, 20, name='Campsite 1')
    campsite2 = sites.Site(20, 200, name='Campsite 2')

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
    ui(itinerary)
