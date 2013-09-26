#!/usr/bin/env python

import getopt
import sys
import urllib.request
import xml.etree.ElementTree as etree

TOD = {'0':'Night', '1':'Morning', '2':'Day', '3':'Evening'}
CLOUD = {'0':'Fair','1':'Partly cloudy', '2':'Cloudy', '3':'Mainly cloudy'}
PREC = {'4':'Light Rain', '5':'Rain', '6':'Show', '7':'Snow', '8':'Storm', '9':'', '10':''}
DIR = {'0':'N', '1':'N-E', '2':'E', '3':'S-E', '4':'S', '5':'S-W', '6':'W', '7':'N-W'}

day_string = "${color2}%s${goto %s}"
phen_string = "${color1}%s${goto %s}"
pres_string = "${color1}%s${goto %s}"
temp_string = "${color1}%s${goto %s}"
wind_string = "${color1}%s${goto %s}"

def __main__(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        opts, args = getopt.getopt(argv[1:], "l:")
    except getopt.error as msg:
         raise Usage(msg)

    location = ''
    for o, v in opts:
        if o == "-l":
            location = v

    if location == '':
        print('No Location code specified')
        exit(0)

#    url = 'http://informer.gismeteo.ru/xml/27553_1.xml'
    url = 'http://informer.gismeteo.ru/xml/' + location + '_1.xml'
    response = urllib.request.urlopen(url)
    data = response.read()
    text = data.decode('utf-8')

    day = []
    phen = []
    pres = []
    temp = []
    wind = []

    root = etree.fromstring(text)
    for child in root.findall('.//FORECAST'):

        day.append(child.attrib['day'] + " " + child.attrib['month'] + " " + child.attrib['year'] + ', ' + TOD[ child.attrib['tod'] ])

        sub = child.find('./PHENOMENA')
        tmp = CLOUD[ sub.attrib['cloudiness'] ]
        if PREC[ sub.attrib['precipitation'] ] != '':
            tmp = tmp + ', ' + PREC[ sub.attrib['precipitation'] ]
        phen.append(tmp)

        sub = child.find('./PRESSURE')
        pres.append(sub.attrib['min'] + ' .. ' + sub.attrib['max'] + ' mmHg')

        sub = child.find('./TEMPERATURE')
        temp.append(sub.attrib['min'] + ' .. ' + sub.attrib['max'] + ' C')

        sub = child.find('./WIND')
        wind.append(sub.attrib['min'] + ' .. ' + sub.attrib['max'] + ' m/s, ' + DIR[ sub.attrib['direction'] ] )

    i = 185
    for item in day:
        print(day_string % (item, i), end='')
        i = i + 185

    print('')
    i = 185

    for item in phen:
        print(phen_string % (item, i), end='')
        i = i + 185

    print('')
    i = 185

    for item in pres:
        print(pres_string % (item, i), end='')
        i = i + 185

    print('')
    i = 185

    for item in temp:
        print(temp_string % (item, i), end='')
        i = i + 185

    print('')
    i = 185

    for item in wind:
        print(wind_string % (item, i), end='')
        i = i + 185

if __name__ == "__main__":
    sys.exit(__main__())