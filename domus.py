#!/usr/bin/env python
import os
import signal
import sys
import datetime
import pytz
import ephem
import time
import json
import urllib2
import pickle


API_KEY="AIzaSyCXg9aF0MwlaByTRPMygka4QGmASiifmP4"

__verbose__ = True
__version__ = "0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.0.1"


try:
    import settings
except:
    sys.exit("Unable to find settings.py file.")


store_location = os.path.join(os.path.expanduser('~'), ".config/domus/data_store")
try:
    os.mkdir(os.path.dirname(store_location))
except OSError:
    # Path already exists
    pass

# Let's try loading our store that contains our lat/log we looked up from the
# address in our settings.py
location={}
try:
    location = pickle.load(open(store_location, "rb"))
except:
    url="https://maps.googleapis.com/maps/api/geocode/json?address="+settings.address.replace(" ","+")+"&key="+API_KEY
    data = json.load(urllib2.urlopen(url))

    for s in data['results']:
        if s['geometry']['location']:
            location['lat']=s['geometry']['location']['lat']
            location['lon']=s['geometry']['location']['lng']

    if __verbose__:
        print "Writing location to data store: %s" % location

    pickle.dump(location, open(store_location, "w"))


class TimeUtils(object):
    def __init__(self):
        # Setup ephem
        self.e = ephem.Observer()
        self.e.lat = str(location['lat'])
        self.e.lon = str(location['lon'])
        self.s = ephem.Sun(self.e)

        self.days = {"Monday" : 0, "Tuesday" : 1, "Wednesday" : 2, "Thursday" : 3, "Friday" : 4, "Saturday" : 5, "Sunday" : 6,
                     "Mon" : 0, "Tues" : 1, "Wed" : 2, "Thurs" : 3, "Fri" : 4, "Sat" : 5, "Sun" : 6 }

        # Update time once to fill __currentTime variable
        self.updateTime()

    def now(self):
        return self.currentTime

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

    def timeUntil(self, time):
        timeDifference = time - self.currentTime
        return int(timeDifference.total_seconds())

    def updateTime(self):
        self.currentTime = datetime.datetime.now(pytz.timezone(settings.timeZone))
        if __verbose__:
            print "Current Time: %s" % self.currentTime

        # Then get todays sunset/sunrise times
        self.s.compute()
        self.sunriseTime = self.sunrise()
        self.sunsetTime = self.sunset()

    def sunrise(self):
        return pytz.utc.localize(self.e.next_rising(self.s).datetime())

    def sunset(self):
        return pytz.utc.localize(self.e.next_setting(self.s).datetime())

def signalHandler(signal, frame):
    print "Exiting..."
    sys.exit(0)

def main():
    print "Running"

if __name__ == "__main__":
    main()

