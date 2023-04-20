import uuid

def uuid4():
    u = uuid.uuid4().int
    return int(str(u)[:7])

class Event:

    def __init__(self):
        self.id = uuid4()

    @property
    def deletable(self):
        return False


class StartTrailheadEvent(Event):

    def __init__(self, datetime, starttrailhead, note=''):
        self.datetime = datetime
        self.site = starttrailhead
        self.padx = 0
        self.note = note
        super().__init__()

    def __repr__(self):
        return f'Start trailhead: {self.site.name}'

    @property
    def name(self):
        return self.site.name

    @name.setter
    def name(self, value):
        self.site.name = value

    @property
    def info(self):
        return self.site.info


class EndTrailheadEvent(Event):

    def __init__(self, datetime, endtrailhead, note=''):
        self.datetime = datetime
        self.site = endtrailhead
        self.padx = 0
        self.note = note
        super().__init__()

    def __repr__(self):
        return f'End trailhead: {self.site.name}'

    @property
    def name(self):
        return self.site.name

    @name.setter
    def name(self, value):
        self.site.name = value

    @property
    def info(self):
        return self.site.info


class SiteArriveEvent(Event):

    def __init__(self, datetime, site):
        self.datetime = datetime
        self.site = site
        super().__init__()

    @property
    def name(self):
        return self.site.name

    @name.setter
    def name(self, value):
        self.site.name = value

    @property
    def info(self):
        return self.site.info


class SiteDepartEvent(Event):

    def __init__(self, datetime, site):
        self.datetime = datetime
        self.site = site
        super().__init__()

    @property
    def name(self):
        return self.site.name

    @name.setter
    def name(self, value):
        self.site.name = value

    @property
    def info(self):
        return self.site.info

class Stay:

    def __init__(self, site, arrive_datetime, depart_datetime, note=''):
        self.event1 = SiteArriveEvent(arrive_datetime, site)
        self.event2 = SiteDepartEvent(depart_datetime, site)
        self.site = site
        self.padx = 2
        self.id = uuid4()
        self.note = note

    @property
    def name(self):
        return self.site.name

    @name.setter
    def name(self, value):
        self.site.name = value

    @property
    def info(self):
        return self.site.info

    @property
    def deletable(self):
        return True

    @property
    def arrive_datetime(self):
        return self.event1.datetime

    @arrive_datetime.setter
    def arrive_datetime(self, value):
        self.event1.datetime = value

    @property
    def depart_datetime(self):
        return self.event2.datetime

    @depart_datetime.setter
    def depart_datetime(self, value):
        self.event2.datetime = value

