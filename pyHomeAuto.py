#!/usr/bin/env python
import os
import signal
import sys
import datetime
import pytz
from astral import Astral

__verbose__ = True
__version__ = "0.0.1"
cityName = 'Los Angeles'
timeZone = 'US/Pacific'

class LocalTime(object):
    def __init__(self):
        # Setup Astral
        self.astralInstance = Astral()
        self.astralInstance.solar_depression = "civil"
        self.astralCity = self.astralInstance[cityName]

        self.days = {"Monday" : 0, "Tuesday" : 1, "Wednesday" : 2, "Thursday" : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6}

    def getCurrentTime(self):
        self.currentTime = datetime.datetime.now(pytz.timezone(timeZone))
        if __verbose__:
            print "Current Time: %s" % self.currentTime

        # Then get todays sunset/sunrise times
        self.sunTime = self.astralCity.sun(self.currentTime)

    def todayIs(self, day):
        return (self.days[day] == self.currentTime.weekday())

    def todayAt(self, hr, min = 0, sec = 0):
        return self.currentTime.replace(hour=hr, minute=min, second=sec)


def signalHandler(signal, frame):
    print "Exiting..."
    sys.exit(0)

def main():
    print "Running"

if __name__ == "__main__":
    main()

