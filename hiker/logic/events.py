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

    def entrylines(self):
        result = []
        result.append(f'Start at: {self.site.name}')
        result.append(f'\tElevation: {self.site.elevation}')
        result.append(f'\tDepart: {self.datetime.strftime("%A, %B %e %Y at %I:%M %p")}')
        result.append(f'\tHas water: {"yes" if self.site.has_water else "no"}')
        result.append(f'\tNotes: {self.note}')
        return result


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

    def entrylines(self):
        result = []
        result.append(f'End at: {self.site.name}')
        result.append(f'\tElevation: {self.site.elevation}')
        result.append(f'\tArrive: {self.datetime.strftime("%A, %B %e %Y at %I:%M %p")}')
        result.append(f'\tHas water: {"yes" if self.site.has_water else "no"}')
        result.append(f'\tNotes: {self.note}')
        return result


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

    def __init__(self, site, arrive_datetime, depart_datetime, note='', needs_permit=False):
        self.event1 = SiteArriveEvent(arrive_datetime, site)
        self.event2 = SiteDepartEvent(depart_datetime, site)
        self.site = site
        self.padx = 2
        self.id = uuid4()
        self.note = note
        self.needs_permit = needs_permit

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

    def entrylines(self):
        result = []
        result.append(f'Stay at: {self.site.name}')
        result.append(f'\tElevation: {self.site.elevation}')
        result.append(f'\tHas water: {"yes" if self.site.has_water else "no"}')
        result.append(f'\tNeeds permit: {"yes" if self.needs_permit else "no"}')
        result.append(f'\tArrive: {self.arrive_datetime.strftime("%A, %B %e %Y at %I:%M %p")}')
        result.append(f'\tDepart: {self.depart_datetime.strftime("%A, %B %e %Y at %I:%M %p")}')
        result.append(f'\tNotes: {self.note}')
        return result

