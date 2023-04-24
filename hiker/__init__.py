import pickle
from pathlib import Path
from datetime import datetime

import yaml
from appdirs import user_data_dir, user_config_dir
from dateparser import parse
from flask import (
    Flask,
    render_template,
    url_for,
    redirect,
    request,
)

from .logic import sites, events
from .info import app_name

app = Flask(__name__)


def make_default_cfg(file):
    data_dir = Path(user_data_dir()) / app_name
    if not data_dir.exists():
        data_dir.mkdir()
    cfg = {
        'data_dir': str(data_dir.absolute()),
    }
    with open(file, 'w') as fh:
        yaml.dump(cfg, fh)
    return Path(file).exists()


def get_cfg():
    cfgdir = Path(user_config_dir()) / app_name
    cfgfile = Path(user_config_dir()) / app_name / 'config.yaml'
    if not cfgdir.exists():
        cfgdir.mkdir(parents=True, exist_ok=True)
    if not cfgfile.exists():
        if not make_default_cfg(cfgfile):
            raise IOError('Could not create config file')
    with open(cfgfile, 'r') as fh:
        return yaml.safe_load(fh)


def get_data_dir():
    cfg = get_cfg()
    return Path(cfg['data_dir'])


def load_itinerary(itinerary_id):
    data_dir = get_data_dir()
    with open(data_dir / Path(str(itinerary_id)+'.pkl'), 'rb') as fh:
        itinerary = pickle.load(fh)
    return itinerary


def dump_itinerary(itinerary):
    data_dir = get_data_dir()
    with open(data_dir / Path(str(itinerary.id)+'.pkl'), 'wb') as fh:
        return pickle.dump(itinerary, fh)


@app.route('/overview/<int:itinerary_id>', methods=['POST', 'GET'])
def overview(itinerary_id):
    itinerary = load_itinerary(itinerary_id)
    return render_template(
        'overview.html',
        itinerary=load_itinerary(itinerary_id),
        routes=[
            i.id
            for i in itinerary.traverse()
            if isinstance(i, sites.Route)
        ],
        stays=[
            i.id
            for i in itinerary.traverse()
            if isinstance(i, events.Stay)
        ],
        trailheads=[
            i.id for i in itinerary.traverse()
            if (
                isinstance(i, events.StartTrailheadEvent)
                or isinstance(i, events.EndTrailheadEvent)
            )
        ],
    )


@app.route('/load', methods=['POST', 'GET'])
def load():
    itineraries = []
    for path in get_data_dir().glob('*.pkl'):
        itinerary_id = int(path.stem)
        itineraries.append(load_itinerary(itinerary_id))
    return render_template('load.html', itineraries=itineraries)


@app.route('/add/<int:itinerary_id>/<int:id>', methods=['POST'])
def add(itinerary_id, id):
    return redirect(
        url_for(
            'add_stay',
            itinerary_id=itinerary_id,
            id=id,
        ),
    )


@app.route('/add/stay/<int:itinerary_id>/<int:id>', methods=['POST', 'GET'])
def add_stay(itinerary_id, id):
    itinerary = load_itinerary(itinerary_id)
    route = itinerary.get_item(id)
    new_stay = events.Stay(
        sites.Site(
            route.site1.location,
            route.site1.elevation,
        ),
        datetime.now(),
        datetime.now(),
    )
    itinerary.add_stay(new_stay)
    dump_itinerary(itinerary)
    return redirect(
        url_for(
            'edit_stay',
            itinerary_id=itinerary.id,
            id=new_stay.id,
        ),
    )


@app.route('/delete/itinerary/<int:itinerary_id>', methods=['POST'])
def delete_itinerary(itinerary_id):
    path = Path(get_data_dir()).absolute() / f'{itinerary_id}.pkl'
    path.unlink()
    return redirect(url_for('load'))


@app.route('/delete/<int:itinerary_id>/<int:id>', methods=['POST'])
def delete(itinerary_id, id):
    return redirect(url_for('delete_stay', itinerary_id=itinerary_id, id=id))


@app.route('/delete/stay/<int:itinerary_id>/<int:id>', methods=['POST', 'GET'])
def delete_stay(itinerary_id, id):
    itinerary = load_itinerary(itinerary_id)
    item = itinerary.get_item(id)
    itinerary.remove_stay(item)
    dump_itinerary(itinerary)
    return redirect(url_for('overview', itinerary_id=itinerary_id))


@app.route('/edit/<int:itinerary_id>/<int:id>', methods=['POST'])
def edit(itinerary_id, id):
    item = load_itinerary(itinerary_id).get_item(id)
    if isinstance(item, sites.Route):
        return redirect(
            url_for(
                'edit_route',
                itinerary_id=itinerary_id,
                id=id,
            ),
        )
    if isinstance(item, events.Stay):
        return redirect(url_for('edit_stay', itinerary_id=itinerary_id, id=id))
    if (
        isinstance(item, events.StartTrailheadEvent)
        or isinstance(item, events.EndTrailheadEvent)
    ):
        return redirect(
            url_for(
                'edit_trailhead',
                itinerary_id=itinerary_id,
                id=id,
            ),
        )
    return redirect(url_for('overview', itinerary_id=itinerary_id))


@app.route('/edit/route/<int:itinerary_id>/<int:id>', methods=['POST', 'GET'])
def edit_route(itinerary_id, id):
    itinerary = load_itinerary(itinerary_id)
    route = itinerary.get_item(id)
    if request.method == 'POST':
        if 'has_water' in request.form:
            if not route.has_water:
                route.add_water()
        else:
            route.remove_water()
        route.name = request.form['name']
        route.note = request.form['note']
        dump_itinerary(itinerary)
        return redirect(url_for('overview', itinerary_id=itinerary.id))
    return render_template(
        'edit_route.html',
        route=route,
        itinerary=itinerary,
    )


@app.route(
    '/edit/stay/<int:itinerary_id>/<int:id>',
    methods=['POST', 'GET'],
)
def edit_stay(itinerary_id, id):
    itinerary = load_itinerary(itinerary_id)
    stay = itinerary.get_item(id)
    if request.method == 'POST':
        if 'has_water' in request.form:
            if not stay.site.has_water:
                stay.site.add_water()
        else:
            stay.site.remove_water()
        if 'needs_permit' in request.form:
            stay.needs_permit = True
        else:
            stay.needs_permit = False
        stay.site.name = request.form['name']
        if parse(request.form['arrive_time']) is not None:
            stay.event1.datetime = parse(request.form['arrive_time'])
        if parse(request.form['depart_time']) is not None:
            stay.event2.datetime = parse(request.form['depart_time'])
        stay.site.location = int(float(request.form['location']))
        stay.site.elevation = int(float(request.form['elevation']))
        stay.note = request.form['note']
        dump_itinerary(itinerary)
        return redirect(url_for('overview', itinerary_id=itinerary.id))
    return render_template(
        'edit_stay.html',
        stay=stay,
        itinerary=itinerary,
    )


@app.route(
    '/edit/trailhead/<int:itinerary_id>/<int:id>',
    methods=['POST', 'GET'],
)
def edit_trailhead(itinerary_id, id):
    itinerary = load_itinerary(itinerary_id)
    trailhead = itinerary.get_item(id)
    if request.method == 'POST':
        if 'has_water' in request.form:
            if not trailhead.site.has_water:
                trailhead.site.add_water()
        else:
            trailhead.site.remove_water()
        if parse(request.form['arrive_time']) is not None:
            trailhead.datetime = parse(request.form['arrive_time'])
        trailhead.site.name = request.form['name']
        trailhead.site.location = int(float(request.form['location']))
        trailhead.site.elevation = int(float(request.form['elevation']))
        trailhead.note = request.form['note']
        dump_itinerary(itinerary)
        return redirect(url_for('overview', itinerary_id=itinerary.id))
    return render_template(
        'edit_trailhead.html',
        trailhead=trailhead,
        itinerary=itinerary,
    )


@app.route(
    '/edit/title/<int:itinerary_id>',
    methods=['POST', 'GET'],
)
def edit_title(itinerary_id):
    itinerary = load_itinerary(itinerary_id)
    if request.method == 'POST':
        if not request.form.keys():
            pass
        else:
            itinerary.name = request.form['name']
            dump_itinerary(itinerary)
            return redirect(url_for('overview', itinerary_id=itinerary.id))
    return render_template(
        'edit_title.html',
        itinerary=itinerary,
    )


@app.route('/new', methods=['POST', 'GET'])
def new():
    starttrailhead = sites.StartTrailhead(0)
    endtrailhead = sites.EndTrailhead(0, 0)

    # define events
    starttrailhead_event = events.StartTrailheadEvent(
        datetime.now(),
        starttrailhead,
    )
    endtrailhead_event = events.EndTrailheadEvent(
        datetime.now(),
        endtrailhead,
    )
    itinerary = sites.Itinerary(
        starttrailhead_event,
        endtrailhead_event,
    )
    dump_itinerary(itinerary)
    return redirect(url_for('overview', itinerary_id=itinerary.id))


@app.route('/export/<int:itinerary_id>', methods=['POST', 'GET'])
def export(itinerary_id):
    itinerary = load_itinerary(itinerary_id)
    result = ''
    for item in itinerary.traverse():
        for line in item.entrylines():
            result += line+'\n'
        result += '\n'
    return render_template('export.html', result=result)
