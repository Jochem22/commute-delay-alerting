import requests


class CalculateRoute:
    """
    Class to fetch route information from Waze API used to calculate delay for commute.

    Credits to kovacsbalu for the Waze API function: https://github.com/kovacsbalu/WazeRouteCalculator

    Attributes
    ----------
    start : str
        Cooridnates to calculate route from
    end : str
        Cooridnates to calculate route to
    """
    def __init__(self, start, end):
        self.start_coords = start
        self.end_coords = end

    @staticmethod
    def distance(results: list) -> float:
        """Calculate distance that is the sum of length from every segment of route"""
        distance = 0
        for result in results:
            distance += result['length']
        distance = round(distance / 1000.0, 1)
        return distance

    def all_routes(self) -> dict:
        """Get all routes information from Waze API including alternatives"""
        all_routes = {}
        url = "https://www.waze.com/row-RoutingManager/routingRequest"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "referer": "https://www.waze.com/",
        }
        params = {
            "from": self.start_coords,
            "to": self.end_coords,
            "at": 0,
            "returnJSON": "true",
            "returnGeometries": "false",
            "returnInstructions": "false",
            "timeout": 60000,
            "nPaths": 2,
            "subscription": "*",
            "options": 'AVOID_TRAILS:t,AVOID_TOLL_ROADS:t,AVOID_FERRIES:t',
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code == 200:
            if "error" not in response.text:
                response_json = response.json()
                response_dict = response_json['alternatives']
                for route in response_dict:
                    route_description = route['response']['routeName']
                    results = route['response']['results']
                    distance_realtime = self.distance(results)
                    all_routes[route_description] = {
                        "duration_realtime": round(route['response']['totalRouteTime'] / 60, 2),
                        "distance_realtime": distance_realtime
                    }
                return all_routes
            else:
                raise requests.exceptions.HTTPError(response.text)
        else:
            raise requests.exceptions.HTTPError(response.status_code)
