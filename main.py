#! /usr/bin/env python3
from utils import Logger, match_closest_distance
from calculateroute import CalculateRoute
from alerting import Alerting
from datetime import datetime, timedelta
from db import save_route_data
import time
import yaml

with open('config.yaml') as f:
    CONFIG = yaml.load(f, Loader=yaml.FullLoader)
LOGGER = Logger()


def check_if_alert(departure_time, commute_days) -> bool:
    if datetime.today().weekday() in commute_days:
        if datetime.now() < departure_time:
            if departure_time - datetime.now() < timedelta(hours=4):
                return True
    else:
        return False


def main() -> None:
    """
    Check commute for delays
    """
    delay_notified: bool = False
    clear_notified: bool = False
    previous_duration_delay = 0
    while True:
        now = datetime.now()
        if now.minute % 5 == 0:
            routes = CONFIG["routes"]
            settings = CONFIG["settings"]
            places = CONFIG["places"]
            max_delay = settings["max_delay"]
            send_updates = settings["send_updates"]
            for name, commute in routes.items():
                departure_time = datetime.now().strftime('%d-%m-%Y ') + commute['departure']
                departure_time = datetime.strptime(departure_time, '%d-%m-%Y %H:%M') + timedelta(hours=2)
                commute_days = commute["days"]
                origin, destination = commute["origin"], commute["destination"]
                distance_static, duration_static = commute['distance'], commute['duration']
                start = f"x:{places[origin]['lon']} y:{places[origin]['lat']}"
                end = f"x:{places[destination]['lon']} y:{places[destination]['lat']}"
                LOGGER.info(f"Get all routes info for {origin} ({start}) to {destination} ({end})")
                get_routes = CalculateRoute(start, end)
                all_routes = get_routes.all_routes()
                LOGGER.debug(all_routes)
                distance_to_match = match_closest_distance(all_routes, distance_static)
                for description in all_routes:
                    distance_realtime = all_routes[description]["distance_realtime"]
                    if distance_realtime == distance_to_match:
                        LOGGER.info(f"Route found for {origin} to {destination} via {description}")
                        duration_realtime = all_routes[description]["duration_realtime"]
                        duration_delay = round(duration_realtime - duration_static, 2)
                        alerting = Alerting(
                            name,
                            max_delay,
                            origin,
                            destination,
                            duration_realtime,
                            duration_delay,
                            distance_static,
                            distance_realtime,
                            description
                        )
                        save_route_data([alerting.__dict__])
                        if check_if_alert(departure_time, commute_days):
                            delay = Alerting.check_delay(alerting)
                            msg = None
                            if delay and not delay_notified:
                                delay_notified = clear_notified = True
                                msg = Alerting.set_delay(alerting)
                            elif clear_notified and not delay:
                                delay_notified = clear_notified = False
                                msg = Alerting.set_clearing(alerting)
                            elif delay_notified and send_updates:
                                if duration_delay < previous_duration_delay:
                                    msg = Alerting.set_update(alerting)
                            if msg:
                                try:
                                    Alerting.send_alert(msg)
                                except Exception as e:
                                    LOGGER.error(e)
                            else:
                                LOGGER.info("No delays for route.")
                            previous_duration_delay = duration_delay
            time.sleep(60)


if __name__ == "__main__":
    main()
