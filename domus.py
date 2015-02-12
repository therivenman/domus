#!/usr/bin/env python
import os
import signal
import sys
import datetime
import pytz
from astral import Astral

try:
    import settings
except:
    sys.exit("Unable to find settings.py file.")

__verbose__ = True
__version__ = "0.0.1"

class TimeUtils(object):
    def __init__(self):
        # Setup Astral
        self.astralInstance = Astral()
        self.astralInstance.solar_depression = "civil"
        self.astralCity = self.astralInstance[settings.cityName]

        self.days = {"Monday" : 0, "Tuesday" : 1, "Wednesday" : 2, "Thursday" : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6,
                     "Mon" : 0, "Tues" : 1, "Wed" : 2, "Thurs" : 3, "Fri" : 4, "Sat" : 5, "Sun" : 6 }

        # Update time once to fill __currentTime variable
        self.updateTime()

    def now(self):
        return self.currentTime

    def sunTimes(self):
        return self.sunTime

    def isToday(self, day):
        if type(day) is str:
            try:
                return (self.days[day.capitalize()] == self.currentTime.weekday())
            except KeyError:
                return False;
        else:
            return (day == self.currentTime.weekday())

    def todayAt(self, hr, min = 0, sec = 0):
        return self.currentTime.replace(hour=hr, minute=min, second=sec)

    def minutesUntil(self, hr, min = 0, sec = 0):
        timeDifference = self.todayAt(hr, min, sec) - self.currentTime
        return int(timeDifference.total_seconds() / 60)

    def updateTime(self):
        self.currentTime = datetime.datetime.now(pytz.timezone(settings.timeZone))
        if __verbose__:
            print "Current Time: %s" % self.currentTime

        # Then get todays sunset/sunrise times
        self.sunTime = self.astralCity.sun(self.currentTime)

def signalHandler(signal, frame):
    print "Exiting..."
    sys.exit(0)

def main():
    print "Running"

if __name__ == "__main__":
    main()

