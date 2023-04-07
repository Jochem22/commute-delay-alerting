from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime
import datetime


def save_to_db(data):
    engine = create_engine('sqlite:///routes.db', echo=True, isolation_level="AUTOCOMMIT")
    meta = MetaData()
    routes = Table(
        'routes', meta,
        Column('id', Integer, primary_key=True),
        Column('ts', DateTime, default=datetime.datetime.utcnow()),
        Column('origin', String),
        Column('destination', String),
        Column('route_description', String),
        Column('duration_realtime', Float),
        Column('duration_delay', Float),
        Column('distance_static', Integer),
        Column('distance_realtime', Float),
        Column('max_delay', Integer)
    )
    # meta.create_all(engine)
    conn = engine.connect()
    conn.execute(routes.insert(), data)

