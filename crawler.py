import os, re, sys
from bs4 import BeautifulSoup as bs
import argparse, configparser

import pandas as pd
import json, string
import requests, urllib
from auth import *
import sensordb

try:
    import ordereddict
except ImportError:
    import collections as ordereddict

def to_pathname(value):
    s = re.sub(r'[\W/]+', '_', value)
    s = re.sub(r'_*$', '', s)
    return s.lower()

def remove_nbsp(s):
    if not s:
        return s
    s = re.sub("&nbsp;", '', s);
    return s

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error encountered when creating directory")
        os._exit(1)

def crawler(start, end):
    # Define Time parameters appropriately
    startArgs = start.split("-")
    endArgs = end.split("-")

    # find all the AcquiSuite boxes
    devices = {}
    response = requests.get(BMOROOT + STATUSPAGE, auth=AUTH)
    soup = bs(response.content, features="html.parser")

    for tr in soup.findAll('tr'):
        tds = tr('td')
        if len(tds) != 6: continue

        name = tds[0].a.string
        devices[name] = {
            'ip' : remove_nbsp(tds[3].string),
            'href' : tds[0].a['href'],
            }

    # look at all the meters hanging off each of them
    for location in devices.keys():
        print("Location: ", location, " URL: ", BMOROOT + devices[location]['href'])
        response = requests.get(BMOROOT + devices[location]['href'], auth=AUTH)
        soup = bs(response.content, features="html.parser")
        subdevices = []
        for tr in soup.findAll('tr'):
            tds = tr('td')
            if len(tds) != 5 or tds[3].a != None: continue
            subdevices.append({
                    'address' : re.sub("<.*?>", "", str(tds[0])),
                    'status': remove_nbsp(tds[1].string),
                    'name' : remove_nbsp(tds[2].string),
                    'type' : remove_nbsp(tds[3].string),
                    'firmware': remove_nbsp(tds[4].string)
                    })
        devices[location]['subdevices'] = subdevices

    f = open("devices.json", "w")
    with open("devices.json", "w") as out:
        out.write(json.dumps(devices))
    f.close()
    print("Exported Device Data to JSON")

    conf = {}
    for location, devs in devices.items():
        params = urllib.parse.parse_qs(urllib.parse.urlsplit(devs['href']).query)
        if not "AS" in params or not  "DB" in params: continue
        if location in AUTH: continue
        thisconf = {}
        for d in devs['subdevices']:
            if sensordb.get_map(d['type'], location) != None:
                dlurl = BMOROOT + 'mbdev_export.php/' + params['AS'][0] + '_' +  \
                    d['address'] + '.csv' + "?DB=" + params['DB'][0] + '&AS=' + \
                    params['AS'][0] + '&MB=' + d['address'] + '&DOWNLOAD=YES' + \
                    "&COLNAMES=ON&EXPORTTIMEZONE=UTC&DELIMITER=COMMA" + \
                    '&DATE_RANGE_STARTTIME={}&DATE_RANGE_ENDTIME={}'
                dlurl = str.replace(dlurl, " ", "")
                thisconf[d['name']] = (
                    d['type'],
                    dlurl)

        if len(thisconf) > 0:
            conf[location] = thisconf

    # generate config file
    cf = configparser.RawConfigParser('', ordereddict.OrderedDict)
    cf.optionxform = str

    cf.add_section('server')
    cf.set('server', 'SuggestThreadPool', '20')
    cf.set('server', 'Port', '9051')
    cf.add_section('/')
    cf.set('/', 'Metadata/Location/Campus', 'UCB')
    cf.set('/', 'Metadata/SourceName', 'buildingmanageronline archive')
    cf.set('/', 'uuid', '91dde108-d02b-11e0-8542-0026bb56ec92')

    for building in conf.keys():
        building_path = '/' + to_pathname(building)
        cf.add_section(building_path)
        cf.set(building_path, 'type', 'Collection')
        for metername in conf[building].keys():
            metertype, url = conf[building][metername]

            building_name = building
            if "New" in building_name:
                building_name = building_name[:building_name.index("New")]
            if "NEW" in building_name:
                building_name = building_name[:building_name.index("NEW")]

            meter_path = building_path + '/' + to_pathname(metername)
            cf.add_section(meter_path)
            cf.set(meter_path, 'Metadata/Extra/MeterName', metername)
            cf.set(meter_path, 'Metadata/Instrument/Model', '"' + metertype + '"')
            cf.set(meter_path, 'Metadata/Location/Building', building_name)
            cf.set(meter_path, 'Url', url)

            # add any extra config options specific to this meter type
            sensor_map = sensordb.get_map(metertype, building_name)
            if 'extra' in sensor_map:
                for k,v in sensor_map['extra'].items():
                    cf.set(meter_path, k, v)

            request_url = url.format(start, end) \
                + "&mnuStartMonth=" + startArgs[1] \
                + "&mnuStartDay=" + startArgs[2] \
                + "&mnuStartYear=" + startArgs[0] \
                + "&mnuStartTime=0%3A0" \
                + "&mnuEndMonth=" + endArgs[1] \
                + "&mnuEndDay=" + endArgs[2] \
                + "&mnuEndYear=" + endArgs[0] \
                + "&mnuEndTime=23%3A59"

    config_file = open("config.ini", "w")
    cf.write(config_file)
    config_file.close()

if __name__ == '__main__':
    # Defining Arguments
    parser = argparse.ArgumentParser(description="Specify Start and End Dates of Building Data Query")
    parser.add_argument("-s", "--start", help="[Required] Start Date of Query (MM-DD-YYYY)", required=True, type=str, metavar="YYYY-MM-DD")
    parser.add_argument("-e", "--end", help='[Required] End Date of Query (MM-DD-YYYY)', required=True, type=str, metavar="YYYY-MM-DD")
    args = parser.parse_args()

    crawler(args.start, args.end)
