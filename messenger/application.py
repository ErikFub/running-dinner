import pywhatkit
from datetime import datetime


class Messenger:
    def __init__(self):
        self.current_hour = datetime.now().hour
        self.current_minute = datetime.now().minute + 1

    def send_message(self):
        pywhatkit.sendwhatmsg("+XXX",
                              "Test",
                              self.current_hour, self.current_minute)

    def send_group_message(self):
        pywhatkit.sendwhatmsg_to_group("XXX",
                                       "Test",
                                       self.current_hour, self.current_minute)
