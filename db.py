from sqlalchemy import create_engine, Column, Integer, String, Float, Time, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Session, relationship, declarative_base
import datetime

ENGINE = create_engine('sqlite:///routes.db', echo=True, isolation_level="AUTOCOMMIT")
BASE = declarative_base()


class RoutePlaces(BASE):
    __tablename__ = "route_places"
    name = Column(String, primary_key=True)
    lat = Column(Float)
    lon = Column(Float)


class RouteConfig(BASE):
    __tablename__ = "route_config"
    name = Column(String, primary_key=True)
    origin_name = Column(String, ForeignKey("route_places.name"))
    destination_name = Column(String, ForeignKey("route_places.name"))
    departure = Column(Time)
    distance = Column(Float)
    duration = Column(Integer)
    days = Column(String)

    data = relationship("RouteData", back_populates="route")
    origin = relationship("RoutePlaces", foreign_keys=[origin_name])
    destination = relationship("RoutePlaces", foreign_keys=[destination_name])


class RouteData(BASE):
    __tablename__ = 'route_data'
    data_id = Column(Integer, primary_key=True)
    name = Column(String, ForeignKey('route_config.name'))
    ts = Column(DateTime, default=datetime.datetime.utcnow)
    origin = Column(String)
    destination = Column(String)
    description = Column(String)
    duration_realtime = Column(Float)
    duration_delay = Column(Float)
    distance_static = Column(Integer)
    distance_realtime = Column(Float)
    max_delay = Column(Integer)

    route = relationship("RouteConfig", back_populates="data")


class Settings(BASE):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True)
    max_delay = Column(Integer)
    send_updates = Column(Boolean)


def save_places():
    # Add sample data
    data = [
        {'name': 'utrecht', 'lat': 52.11805947320983, 'lon': 5.02638342275991},
        {'name': 'amsterdam', 'lat': 52.3676122873359, 'lon': 4.901130197765845},
    ]
    session = Session(bind=ENGINE)
    for places in data:
        new_place = RoutePlaces(**places)
        session.add(new_place)
    session.commit()
    session.close()


def save_settings():
    session = Session(bind=ENGINE)
    settings = Settings(max_delay=5, send_updates=False)
    session.add(settings)
    session.commit()
    session.close()


def save_route_config():
    # Add sample data
    data = [
        {'name': 'routea', 'origin_name': 'utrecht', 'destination_name': 'amsterdam', 'departure': datetime.time(hour=17, minute=30, second=0),
         'distance': 38, 'duration': 30, 'days': '012345'},
        {'name': 'routeb', 'origin_name': 'amsterdam', 'destination_name': 'utrecht', 'departure': datetime.time(hour=8, minute=30, second=0),
         'distance': 36, 'duration': 29, 'days': '012345'},
    ]
    session = Session(bind=ENGINE)
    for route_config in data:
        new_config = RouteConfig(**route_config)
        session.add(new_config)
    session.commit()
    session.close()


def save_route_data(data):
    session = Session(bind=ENGINE)
    for route_data in data:
        new_route = RouteData(**route_data)
        session.add(new_route)
    session.commit()
    session.close()


# create database and set example data
# BASE.metadata.create_all(ENGINE)
# save_settings()
# save_places()
# save_route_config()
