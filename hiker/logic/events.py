class Event:

    def __init__(self):
        pass


class StartTrailheadEvent(Event):

    def __init__(self, datetime, starttrailhead):
        self.datetime = datetime
        self.site = starttrailhead

    def __repr__(self):
        return f'Start trailhead: {self.site.name}'


class EndTrailheadEvent(Event):

    def __init__(self, datetime, endtrailhead):
        self.datetime = datetime
        self.site = endtrailhead

    def __repr__(self):
        return f'End trailhead: {self.site.name}'


class SiteArriveEvent(Event):

    def __init__(self, datetime, site):
        self.datetime = datetime
        self.site = site


class SiteDepartEvent(Event):

    def __init__(self, datetime, site):
        self.datetime = datetime
        self.site = site

class Stay:

    def __init__(self, site, arrive_datetime, depart_datetime):
        self.event1 = SiteArriveEvent(arrive_datetime, site)
        self.event2 = SiteDepartEvent(depart_datetime, site)
        self.site = site

    def __repr__(self):
        return f'Stay: {self.site.name}'
