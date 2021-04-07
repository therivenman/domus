#!/usr/bin/env python
import domus
import time
import signal
import sys

def signalHandler(signal, frame):
    print "Exiting..."
    sys.exit(1)

def main():
    timeUtils = domus.TimeUtils()
    sleepTime = timeUtils.timeUntil(timeUtils.dusk())

    if (sleepTime < 0):
        print "Sunset has already passed for today."
        sys.exit(1)

    signal.signal(signal.SIGINT, signalHandler)

    print "Dusk at %s. Sleeping %d seconds." % (timeUtils.dusk(), sleepTime)
    time.sleep(sleepTime)

if __name__ == "__main__":
    main()
