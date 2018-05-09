# coding: utf-8
import sys
import requests
import json
import logging
import os
from requests.exceptions import ConnectionError

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

url = 'http://%s/api/v1/branches/%s/conflicts?applicationName=%s&applicationVersion=%s' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
logging.info('REST URL has been generated: %s' % url)

try:
    r = requests.get(url)
except ConnectionError as e:    # This is the correct syntax
    print "Unable to connect to the specified URL. Please check the supplied parameters"
    sys.exit(1)

if r.status_code == 500:
    logging.info('User details successfully obtained.')
else:
    logging.error("Unable to get user details. [HTTP response=%s]." % (r.text))

details =  json.loads(r.text)

conflictCount = details["conflictsCount"]

if conflictCount == 1:
    logging.error("Conflict Detected.")
    sys.exit(1)
else:
    logging.info('No conflicts were detected')

