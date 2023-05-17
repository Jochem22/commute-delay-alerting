from logging.handlers import RotatingFileHandler
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db import RouteConfig, RoutePlaces, Settings
import logging


class Logger:
    def __init__(self):
        self.filename = "main.log"
        logging.basicConfig(
            format='%(asctime)s | %(levelname)s | %(message)s',
            level=logging.DEBUG,
            handlers=[RotatingFileHandler(self.filename, maxBytes=100000, backupCount=5)]
        )

    @staticmethod
    def debug(debug):
        logging.debug(debug)

    @staticmethod
    def info(info):
        logging.info(info)

    @staticmethod
    def warning(warning):
        logging.warning(warning)

    @staticmethod
    def error(error):
        logging.error(error)


def match_closest_distance(dct, nmbr):
    lst = [list(value.values())[1] for value in dct.values()]
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i] - nmbr))]


def get_config():
    engine = create_engine('sqlite:///routes.db')
    session = sessionmaker(bind=engine)
    session = session()
    routes = session.query(RouteConfig).all()
    places = session.query(RoutePlaces).all()
    settings = session.query(Settings).all()
    places_config = {}
    for place in places:
        name = place.name
        lat = place.lat
        lon = place.lon
        places_config[name] = {'lat': lat, 'lon': lon}
    routes_config = {}
    for route in routes:
        name = route.name
        origin_name = route.origin_name
        destination_name = route.destination_name
        departure = route.departure
        distance = route.distance
        duration = route.duration
        days = route.days
        routes_config[name] = {
            'origin': origin_name,
            'destination': destination_name,
            'departure': departure,
            'distance': distance,
            'duration': duration,
            'days': days
        }
    for setting in settings:
        max_delay = setting.max_delay
        send_updates = setting.send_updates
        settings_config = {"max_delay": max_delay, "send_updates": send_updates}
    session.close()
    return places_config, routes_config, settings_config
