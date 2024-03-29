from dotenv import dotenv_values
from utils import Logger
import requests

LOGGER = Logger()
SECRET = dotenv_values()


class Alerting:
    """
    Class for setting and sending alerts regarding delay of commute

    Attributes
    ----------
    max_delay : int
        max delay in minutes set in config
    origin : str
        origin name set in config
    destination : str
        destination name set in config
    duration_realtime : float
        duration of route in real time including traffic jams
    duration_delay : float
        total delay of route in minutes in real time used to check for delay
    description : str
        short description of route
    """
    def __init__(self, name, max_delay, origin, destination, duration_realtime, duration_delay, description):
        self.name = name
        self.max_delay = max_delay
        self.origin = origin
        self.destination = destination
        self.duration_realtime = duration_realtime
        self.duration_delay = duration_delay
        self.description = description

    def check_delay(self) -> bool:
        """Returns True if total delay in minutes exceeds max delay in minutes set in config"""
        return bool(self.duration_delay >= self.max_delay)

    def set_delay(self) -> str:
        """Set message when delay is True"""
        msg = (
            f"Delay on route from {self.origin} to {self.destination} ({self.description}):%0A%0A"
            f"Current duration is {self.duration_realtime} minutes with "
            f"{self.duration_delay} minutes delay. "
        )
        return msg

    def set_clearing(self) -> str:
        """Set message when delay alarms are cleared"""
        msg = (
            f"Cleared alarms for {self.origin} to {self.destination} ({self.description}):%0A%0A"
            f"Duration is {self.duration_realtime} minutes. "
        )
        return msg

    def set_update(self) -> str:
        """Set message for update on duration"""
        msg = (
            f"Update on delay:%0A%0A"
            f"Current duration is {self.duration_realtime} minutes."
        )
        return msg

    @staticmethod
    def send_alert(msg: str) -> None:
        """Send message to chat_id via Telegram"""
        token = SECRET["TOKEN"]
        chat_id = SECRET["CHATID"]
        url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={msg}"
        request = requests.get(url, timeout=10)
        if request.status_code == 200:
            LOGGER.debug(request.text)
        else:
            raise requests.exceptions.HTTPError("error sending telegram message")
