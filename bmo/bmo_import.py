import os
import re
import sys
import time
import datetime

from twisted.internet import reactor, defer
from twisted.python import log

from smap import loader
from smap.drivers.obvius import bmo # import bmo
from smap.contrib import dtutil

# day to start import at
startdt = dtutil.strptime_tz("04 01 2019", "%m %d %Y")
enddt = startdt + datetime.timedelta(days=1)
days = 3

def next_day():
    global startdt
    global enddt
    global inst
    global days

    print "\n\nSTARTING DAY (%i remaining)\n" % days
    tasks = []
    for d in inst.drivers.itervalues():
        if isinstance(d, bmo.BMOLoader):
            tasks.append(d.update(startdt, enddt))

    startdt = startdt + datetime.timedelta(days=1)
    enddt = startdt + datetime.timedelta(days=1)
    d = defer.DeferredList(tasks)
    d.addCallback(lambda _: inst._flush())
    return d

def do_next_day(*args):
    global days
    if days > 0:
        days -= 1
        d = next_day()
        d.addCallback(do_next_day)
        return d
    else:
        reactor.stop()

def import_URLs(config, start_day, num_days):
    global startdt
    global enddt
    global inst
    global days

    inst = loader.load(config)
    startdt = dtutil.strptime_tz(re.sub("-", " ", start_day), "%m %d %Y")
    enddt = startdt + datetime.timedelta(days=1)
    days = int(num_days)
    do_next_day()
    reactor.run()

if __name__ == '__main__':
    if len(sys.argv) != 4: # File Data
        print "\n\tIncorrect Arguments"
        print "\t%s <conf> <startdt> <days>" % sys.argv[0]
        print "\tExample: %s config.ini 04-01-2019 3\n" % sys.argv[0]
    else:
        # log.startLogging(sys.stdout)
        import_URLs(sys.argv[1], sys.argv[2], sys.argv[3])
