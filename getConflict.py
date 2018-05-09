# coding: utf-8
import sys
import requests
import json
import logging
import os
from requests.exceptions import ConnectionError

# Set the log stream to output via stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#Construct the URL based on input parameters
try:
    url = 'http://%s/api/v1/branches/%s/conflicts?applicationName=%s&applicationVersion=%s' % (sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    logging.info('REST URL has been generated: %s' % url)
except IndexError:
    logging.debug('Not enough parameters have been passed')

# Perform the GET request to check for conflicts. 
try:
    r = requests.get(url)
except ConnectionError as e:
    logging.info("Unable to connect to the specified URL. Please check the supplied parameters")
    sys.exit(1)

# Check that the correct status code is returned
if r.status_code == 500:
    logging.info('Conflict details successfully obtained.')
else:
    logging.error("Unable to check for conflicts. [HTTP response=%s]." % (r.text))

# Parse the JSON
details =  json.loads(r.text)

# Retrieve the conflict count from the JSON
conflictCount = int(details["conflictsCount"])

# Check if there are any conflicts. If there are, fail the build
if conflictCount == 1:
    logging.error("Conflict Detected.")
    sys.exit(1)
else:
    logging.info('No conflicts were detected')

