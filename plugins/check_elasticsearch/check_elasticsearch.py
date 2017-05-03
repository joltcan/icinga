#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Fredrik Lundhag"
__email__ = "fredrik.lundhag@verisure.com"
__license__ = "MIT"
__version__ = "1.0"

''' 
    Simple script to query elasticsearch status and return data for an Icinga check.
'''

import argparse
import requests
import sys

STATUS = {0: 'OK',
        1: 'WARNING',
        2: 'CRITICAL',
        3: 'UNKNOWN'}

HEALTH = {'red':    2,
          'yellow': 1,
          'green':  0}

checkname = 'Check elasticsearch'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-H', help='Hostname, default is localhost', dest='hostname', default='localhost')
    parser.add_argument('-P', help='Port, default is 9200', default=9200, type=int, dest='port')
    args = parser.parse_args()

    url = 'http://%s:%d/_cluster/health' % (args.hostname, args.port)
    try:
        r = requests.get(url)
        data = r.json()
    except:
        print "Could not connect to http://%s:%d" % (args.hostname, args.port)
        parser.print_help()
        sys.exit(3)

    returncode = HEALTH[data['status']]
    
    print "%s is %s," % (checkname, STATUS[returncode])
    for key, value in data.iteritems():
        print "%s: %s" % (key.capitalize().replace('_', ' '), value)

    sys.exit(int(returncode))

