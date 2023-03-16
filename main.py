#! /usr/bin/env python3
from utils import Logger, match_closest_distance
from calculateroute import CalculateRoute
from alerting import Alerting
import datetime
import time
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)
LOGGER = Logger()


def main():
    """
    Check commute for delays
    """
    delay_notified = False
    clear_notified = False
    while True:
        for routes in CONFIG["routes"]:
            commute = CONFIG["routes"][routes]
            max_delay = CONFIG["settings"]["max_delay"]
            send_updates = CONFIG["settings"]["send_updates"]
            date = datetime.datetime.now().strftime('%d-%m-%Y')
            departure_time = commute['departure']
            departure_time = f"{date} {departure_time}"
            departure_time = datetime.datetime.strptime(departure_time, '%d-%m-%Y %H:%M') + datetime.timedelta(hours=2)
            weekday = datetime.datetime.today().weekday()
            if weekday in commute["days"]:
                if datetime.datetime.now() < departure_time:
                    if departure_time - datetime.datetime.now() < datetime.timedelta(hours=4):
                        origin = commute["origin"]
                        destination = commute["destination"]
                        distance_static = commute['distance']
                        duration_static = commute['duration']
                        lat = CONFIG["places"][origin]['lat']
                        lon = CONFIG["places"][origin]['lon']
                        start = f"x:{lon} y:{lat}"
                        lat = CONFIG["places"][destination]['lat']
                        lon = CONFIG["places"][destination]['lon']
                        end = f"x:{lon} y:{lat}"
                        LOGGER.info(f"Started monitoring route {origin} ({start}) to {destination} ({end})")
                        get_routes = CalculateRoute(start, end)
                        all_routes = get_routes.all_routes()
                        LOGGER.debug(all_routes)
                        distance_to_match = match_closest_distance(all_routes, distance_static)
                        for route_description in all_routes:
                            distance_realtime = all_routes[route_description]["distance_realtime"]
                            if distance_realtime == distance_to_match:
                                LOGGER.info(f"Route found for {origin} to {destination} via {route_description}")
                                duration_realtime = all_routes[route_description]["duration_realtime"]
                                duration_delay = duration_realtime - duration_static
                                alerting = Alerting(
                                    max_delay,
                                    origin,
                                    destination,
                                    duration_realtime,
                                    duration_delay,
                                    distance_static,
                                    distance_realtime,
                                    route_description
                                )
                                delay = Alerting.check_delay(alerting)
                                msg = None
                                if delay is True and delay_notified is False:
                                    delay_notified = True
                                    clear_notified = True
                                    msg = Alerting.set_delay(alerting)
                                elif clear_notified is True and delay is False:
                                    delay_notified = False
                                    clear_notified = False
                                    msg = Alerting.set_clearing(alerting)
                                elif delay_notified is True and send_updates is True:
                                    msg = Alerting.set_update(alerting)
                                if msg:
                                    try:
                                        Alerting.send_alert(msg)
                                    except Exception as e:
                                        LOGGER.error(e)
                                else:
                                    LOGGER.info(f"No delays")
                    else:
                        LOGGER.info(f"Nothing to monitor. "
                                    f"Start monitoring at {departure_time - datetime.timedelta(hours=4)}")
        time.sleep(300)


if __name__ == "__main__":
    main()
