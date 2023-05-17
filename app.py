from flask import Flask, render_template, jsonify, request, redirect
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists
from db import RouteConfig, RoutePlaces, RouteData, create_db
from datetime import datetime, date, timedelta, time

app = Flask(__name__)

if database_exists('sqlite:///routes.db'):
    engine = create_engine('sqlite:///routes.db')
    Session = sessionmaker(bind=engine)
    session = Session()
else:
    create_db()

@app.route('/')
def index():
    route_a_data = session.query(RouteData).filter_by(name='routea').all()
    route_b_data = session.query(RouteData).filter_by(name='routeb').all()
    return render_template('index.html', route_a_data=route_a_data, route_b_data=route_b_data)


@app.route('/data')
def get_route_data():
    today = date.today()
    route_a_data = session.query(RouteData).filter(RouteData.name == 'routea', RouteData.ts >= datetime.combine(today, datetime.min.time())).all()
    route_b_data = session.query(RouteData).filter(RouteData.name == 'routeb', RouteData.ts >= datetime.combine(today, datetime.min.time())).all()
    data = {
        'routea': [
            {'ts': (data.ts + timedelta(hours=2)).strftime('%H:%M'), 'duration_realtime': data.duration_realtime} for data in route_a_data
        ],
        'routeb': [
            {'ts': (data.ts + timedelta(hours=2)).strftime('%H:%M'), 'duration_realtime': data.duration_realtime} for data in route_b_data
        ]
    }
    return jsonify(data)


@app.route('/route_configs')
def route_configs():
    configs = session.query(RouteConfig).all()
    places = session.query(RoutePlaces).all()
    return render_template('route_configs.html', configs=configs, places=places)


@app.route('/add_route_config', methods=['POST'])
def add_route_config():
    name = request.form['name']
    origin_name = request.form['origin_name']
    destination_name = request.form['destination_name']
    departure = time.fromisoformat(request.form['departure'])
    distance = request.form['distance']
    duration = request.form['duration']
    days = request.form['days']
    new_config = RouteConfig(name=name, origin_name=origin_name, destination_name=destination_name,
                             departure=departure, distance=distance, duration=duration, days=days)
    session.add(new_config)
    session.commit()
    return redirect('/route_configs')


@app.route('/delete_route_config')
def delete_route_config():
    name = request.args.get('name')
    config = session.query(RouteConfig).filter_by(name=name).first()
    session.delete(config)
    session.commit()
    return redirect('/route_configs')


@app.route('/edit_route_config')
def edit_route_config():
    name = request.args.get('name')
    edit_config = session.query(RouteConfig).filter_by(name=name).first()
    places = session.query(RoutePlaces).all()
    return render_template('edit_route_config.html', configs=edit_config, places=places)


@app.route('/update_route_config', methods=['POST'])
def update_route_config():
    name = request.form['name']
    origin_name = request.form['origin_name']
    destination_name = request.form['destination_name']
    departure = time.fromisoformat(request.form['departure'])
    distance = request.form['distance']
    duration = request.form['duration']
    days = request.form['days']
    update_config = session.query(RouteConfig).filter_by(name=name).first()
    update_config.name = name
    update_config.origin_name = origin_name
    update_config.destination_name = destination_name
    update_config.departure = departure
    update_config.distance = distance
    update_config.duration = duration
    update_config.days = days
    session.commit()
    return redirect('/route_configs')


@app.route('/route_places')
def route_places():
    places = session.query(RoutePlaces).all()
    return render_template('route_places.html', configs=places)


@app.route('/add_route_place', methods=['POST'])
def add_route_place():
    name = request.form['name']
    lat = request.form['lat']
    lon = request.form['lon']
    new_place = RoutePlaces(name=name, lat=lat, lon=lon)
    session.add(new_place)
    session.commit()
    return redirect('/route_places')


@app.route('/delete_route_place')
def delete_route_place():
    name = request.args.get('name')
    delete_place = session.query(RoutePlaces).filter_by(name=name).first()
    session.delete(delete_place)
    session.commit()
    return redirect('/route_places')


@app.route('/edit_route_place')
def edit_route_place():
    name = request.args.get('name')
    edit_place = session.query(RoutePlaces).filter_by(name=name).first()
    return render_template('edit_route_place.html', configs=edit_place)


@app.route('/update_route_place', methods=['POST'])
def update_route_place():
    name = request.form['name']
    lat = request.form['lat']
    lon = request.form['lon']
    update_place = session.query(RoutePlaces).filter_by(name=name).first()
    update_place.name = name
    update_place.lat = lat
    update_place.lon = lon
    session.commit()
    return redirect('/route_places')


@app.route('/route_data')
def route_data():
    data = session.query(RouteData).all()
    return render_template('route_data.html', configs=data)


if __name__ == '__main__':
    app.run(port=5004, debug=True)
