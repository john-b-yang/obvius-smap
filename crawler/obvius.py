import logging
import time
import calendar
import urlparse
import re

import smap.driver
from smap.util import periodicSequentialCall

import sensordb

def to_pathname(s):
    s = re.sub('[\W/]+', '_', s)
    s = re.sub('_*$', '', s)
    return s.lower()

class Driver(smap.driver.FetchDriver):
    def setup(self, opts):
        self.mappings = [x for x in sensordb.DB if x['obviusname'] == opts['ObviusType']][0]
        self.set_metadata('/', {
                'Extra/Driver' : 'smap.drivers.obvius',
                'Instrument/Model' : opts['ObviusType']
                })

        # create all the channels
        for (field, regexp, phase, channel,fmt) in self.mappings['sensors'] + self.mappings['meters']:
            self.add_timeseries('/' + phase + '/' + channel,
                                fmt, data_type='double')
            self.set_metadata('/' + phase, {
                'Extra/Phase' : phase })

        # create the url with auth included
        url_p = urlparse.urlparse(opts['Url'])
        netloc = '%s:%s@%s' % (opts['Username'], opts['Password'], url_p.netloc)
        url = urlparse.urlunparse((url_p.scheme, netloc, url_p.path,
                                   url_p.params, url_p.query, url_p.fragment))

        smap.driver.FetchDriver.setup(self, {
                'Uri' : url,
                'Rate' : opts.get('Period', 30),
                })

    def is_sensor(self, channel, OBVIUS_SENSORS):
        for (x,y,z,p,q) in OBVIUS_SENSORS:
            if p == channel:
                return True
        return False

    def process(self, html):
        # the obvius timestamp is in UTC
        reading_time = re.findall('<time.*?>(.*?)</time>', html)[0]
        # pydoc says this is the right way to convert this timestamp
        reading_time = time.strptime(reading_time + " UTC",
                                     "%Y-%m-%d %H:%M:%S %Z")
        reading_time = calendar.timegm(reading_time)
        logging.debug("reading timestamp is " + str(reading_time))

        # this pulls out a list of all the channel-reading pairs
        data = re.findall('<point.*?name="(.*?)".*?value="(.*?)".*?/>', html.lower())
        data_map = {}
        data_map.update(data)

        for (field, regexp, phase, channel,fmt) in \
                self.mappings['sensors'] + self.mappings['meters']:
            reading = data_map.get(field.lower())
            if not reading:
                logging.warn(field + " not found in doc")
                continue
            match = re.search(regexp, reading)
            if not match:
                logging.warn("reading conversion failed: " + reading + " : " + field)
                continue
            self.add('/' + phase + '/' + channel, reading_time, float(match.groups(0)[0]))
