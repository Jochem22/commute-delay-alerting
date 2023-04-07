import matplotlib.pyplot as plt
import datetime
from sqlalchemy import create_engine, Table, MetaData, select, Column, Integer, String, Float, DateTime

# create an engine and connect to the SQLite database
engine = create_engine('sqlite:///routes.db', echo=True)
connection = engine.connect()

# create a metadata object
meta = MetaData()

# define the table
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

# select the data for the two routes and order by timestamp
stmt = select(routes.c.ts, routes.c.duration_realtime).\
       where(routes.c.origin == 'ede').where(routes.c.destination == 'druten').\
       order_by(routes.c.ts)
stmt2 = select(routes.c.ts, routes.c.duration_realtime).\
       where(routes.c.origin == 'druten').where(routes.c.destination == 'ede').\
       order_by(routes.c.ts)

# execute the queries and fetch the results
results = connection.execute(stmt).fetchall()
results2 = connection.execute(stmt2).fetchall()

# extract the timestamps and durations for each route
timestamps = [r[0] for r in results]
durations = [r[1] for r in results]
timestamps2 = [r[0] for r in results2]
durations2 = [r[1] for r in results2]

# create a figure and axis object
fig, ax = plt.subplots()

# plot the two routes
ax.plot(timestamps, durations, label='Ede to Druten')
ax.plot(timestamps2, durations2, label='Druten to Ede')

# format the x-axis as dates
import matplotlib.dates as mdates
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))
fig.autofmt_xdate()

# add a legend and axis labels
ax.legend()
ax.set_xlabel('Timestamp')
ax.set_ylabel('Duration Realtime')

# show the plot
plt.show()