import uuid
from . import features


def uuid4():
    u = uuid.uuid4().int
    return int(str(u)[:7])


class Site:

    def __init__(self, location, elevation, features=[], name=''):
        self.location = location
        self.elevation = elevation
        self.features = features
        self._name = name
        self.id = uuid4()

    @property
    def deletable(self):
        return False

    @property
    def has_water(self):
        return True in [
            isinstance(feature, features.WaterFeature)
            for feature in self.features
        ]

    def add_feature(self, feature):
        self.features.append(feature)

    def remove_feature(self, feature):
        for feat in self.features:
            if feat is feature:
                self.features.remove(feature)

    def remove_water(self):
        for feature in self.features:
            if isinstance(feature, features.WaterFeature):
                self.remove_feature(feature)

    def add_water(self):
        self.features.append(features.WaterFeature())

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def info(self):
        return (
            f'Location along route: {self.location}'
            f'\nElevation: {self.elevation}'
        )

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

    def align_text(self, n):
        lines = self.text.splitlines()
        for i in range(len(lines)):
            lines[i] = '\t'*n+lines[i]
        return '\n'.join(lines)


class Route:

    def __init__(self, site1, site2, features, note='', name=None):
        self.site1 = site1
        self.site2 = site2
        self.features = features
        self.padx = 1
        self.id = uuid4()
        self.note = ''
        if name is None:
            self.name = f'Trail from {self.site1.name} to {self.site2.name}'
        else:
            self.name = name

    def entrylines(self):
        result = []
        result.append(f'--> {self.name}')
        result.append(f'\tStart: {self.site1} (elevation: {self.site1.elevation})')
        result.append(f'\tEnd: {self.site2} (elevation: {self.site2.elevation})')
        result.append(f'\tDistance: {self.length}')
        result.append(f'\tElevation change: {self.elevation_change}')
        result.append(f'\tWater on route: {"yes" if self.has_water else "no"}')
        result.append(f'\tNotes: {self.note}')
        return result

    @property
    def length(self):
        return abs(self.site2.location - self.site1.location)

    @property
    def has_water(self):
        return True in [
            isinstance(feature, features.WaterFeature)
            for feature in self.features
        ]

    def add_feature(self, feature):
        self.features.append(feature)

    def remove_feature(self, feature):
        try:
            self.features.remove(feature)
        except ValueError:
            pass

    def remove_water(self):
        for feature in self.features:
            if isinstance(feature, features.WaterFeature):
                self.remove_feature(feature)

    def add_water(self):
        self.features.append(features.WaterFeature())

    @property
    def elevation_change(self):
        return self.site2.elevation - self.site1.elevation

    def is_between(self, site1, site2):
        return self.site1 is site1 and self.site2 is site2

    def __repr__(self):
        return f'--> Site 1: {self.site1.name} / Site 2: {self.site2.name}'

    @property
    def deletable(self):
        return False

    @property
    def info(self):
        return (
            f'Length: {self.length}'
            f'\nElevation change: {self.elevation_change}'
        )


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
        note='',
        name='',
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
        self.id = uuid4()
        self.note = note
        self.name = name
        if self.name == '':
            self.name = 'Itinerary'

    def index(self, item):
        for i, im in enumerate(self.traverse()):
            if im.id == item.id:
                return i

    def remove_route(self, route):
        for r in self._routes:
            if route.id == r.id:
                self._routes.remove(route)

    def remove_stay(self, stay):
        items = list(self.traverse())
        for i, item in enumerate(items):
            if stay.id == item.id:
                route1 = items[i-1]
                route2 = items[i+1]
                self._stays.remove(stay)
                self.remove_route(route1)
                self.remove_route(route2)
        self.autofill_routes()

    def _add_stay(self, stay):
        self._stays.append(stay)

    def add_stay(self, stay):
        self._add_stay(stay)
        self.autofill_routes()

    def add_route(self, route):
        self._routes.append(route)

    def autofill_routes(self):
        site1 = self.starttrailhead_event.site
        for stay in self.stays:
            site2 = stay.site
            if True not in [
                route.is_between(site1, site2) for route in self.routes
            ]:
                self.add_route(Route(site1, site2, features=[]))
            site1 = site2
        site2 = self.endtrailhead_event.site
        if True not in [
            route.is_between(site1, site2) for route in self.routes
        ]:
            self.add_route(Route(site1, site2, features=[]))

    @property
    def deletable(self):
        return False

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

    def get_item(self, id):
        for item in self.traverse():
            if item.id == id:
                return item
        raise ValueError('No such id')
