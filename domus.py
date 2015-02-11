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

class TimeUtils(object):
    def __init__(self):
        # Setup Astral
        self.__astralInstance = Astral()
        self.__astralInstance.solar_depression = "civil"
        self.__astralCity = self.__astralInstance[cityName]

        self.__days = {"Monday" : 0, "Tuesday" : 1, "Wednesday" : 2, "Thursday" : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6,
                     "Mon" : 0, "Tues" : 1, "Wed" : 2, "Thurs" : 3, "Fri" : 4, "Sat" : 5, "Sun" : 6 }

        # Update time once to fill __currentTime variable
        self.updateTime()

    def now(self):
        return self.__currentTime

    def sunTimes(self):
        return self.__sunTime

    def isToday(self, day):
        if type(day) is str:
            try:
                return (self.__days[day.capitalize()] == self.__currentTime.weekday())
            except KeyError:
                return False;
        else:
            return (day == self.__currentTime.weekday())

    def todayAt(self, hr, min = 0, sec = 0):
        return self.__currentTime.replace(hour=hr, minute=min, second=sec)

    def minutesUntil(self, hr, min = 0, sec = 0):
        timeDifference = self.todayAt(hr, min, sec) - self.__currentTime
        return int(timeDifference.total_seconds() / 60)

    def updateTime(self):
        self.__currentTime = datetime.datetime.now(pytz.timezone(timeZone))
        if __verbose__:
            print "Current Time: %s" % self.__currentTime

        # Then get todays sunset/sunrise times
        self.__sunTime = self.__astralCity.sun(self.__currentTime)

def signalHandler(signal, frame):
    print "Exiting..."
    sys.exit(0)

def main():
    print "Running"

if __name__ == "__main__":
    main()

