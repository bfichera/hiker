class Site:

    def __init__(self, location, elevation, features=[], name=''):
        self.location = location
        self.elevation = elevation
        self.features = features
        self.name = name

    @property
    def text(self):
        return f'{self.name}\n(LOC: {self.location} | ELE: {self.elevation})'

    def __lt__(self, other):
        return self.location < other.location

    def __gt__(self, other):
        return self.location > other.location

    def __le__(self, other):
        return self.location <= other.location

    def __ge__(self, other):
        return self.location >= other.location

    def __repr__(self):
        return 'Name: '+self.name


class Route:

    def __init__(self, site1, site2, sites=[]):
        self.site1 = site1
        self.site2 = site2
        self.sites = sites

    @property
    def length(self):
        return abs(self.site2.location - self.site1.location)

    @property
    def elevation_change(self):
        return self.site2.elevation - self.site1.elevation

    def is_between(self, site1, site2):
        return self.site1 is site1 and self.site2 is site2

    def __repr__(self):
        return f'--> Site 1: {self.site1.name} / Site 2: {self.site2.name}'

    @property
    def text(self):
        return f'{self.site1.name} --> {self.site2.name}\n(dLOC: {self.length} | dELE: {self.elevation_change})'


class StartTrailhead(Site):

    def __init__(self, elevation, features=[], name='Start'):
        super().__init__(0, elevation, features, name)


class EndTrailhead(Site):

    def __init__(self, location, elevation, features=[], name='End'):
        super().__init__(location, elevation, features, name)


class Itinerary:

    def __init__(
        self,
        starttrailhead_event,
        endtrailhead_event,
        stays=[],
        routes=[],
    ):
        self.starttrailhead_event = starttrailhead_event
        self.endtrailhead_event = endtrailhead_event
        self._stays = []
        self._routes = []
        for event in stays:
            self.add_stay(event)
        for route in routes:
            self.add_route(route)
        self.autofill_routes()

    def add_stay(self, stay):
        self._stays.append(stay)

    def add_route(self, route):
        self._routes.append(route)

    def autofill_routes(self):
        site1 = self.starttrailhead_event.site
        for stay in self.stays:
            site2 = stay.site
            if True not in [
                route.is_between(site1, site2) for route in self.routes
            ]:
                self.add_route(Route(site1, site2, sites=[]))
            site1 = site2
        site2 = self.endtrailhead_event.site
        if True not in [
            route.is_between(site1, site2) for route in self.routes
        ]:
            self.add_route(Route(site1, site2, sites=[]))

    @property
    def stays(self):
        return list(sorted(self._stays, key=lambda x: x.event1.datetime))

    @property
    def routes(self):
        return list(sorted(self._routes, key=lambda x: x.site1))

    def traverse(self):
        result = []
        result.append(self.starttrailhead_event)
        for stay, route in zip(self.stays, self.routes):
            result.append(route)
            result.append(stay)
        result.append(self.routes[-1])
        result.append(self.endtrailhead_event)
        yield from result
