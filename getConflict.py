# coding: utf-8
import sys
import requests
import json
import logging
import os
import argparse
from requests.exceptions import ConnectionError

# Set the log stream to output via stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Parse inbound arguments
parser = argparse.ArgumentParser(
    description="Check for branch merge conflicts on PEGA.")
parser.add_argument(
    "baseUrl",
    help="The base url of the server. This should not include http://, https:// or /prweb. It should be in the form 'example.com'.")
parser.add_argument(
    "branch",
    help="The name of the branch you want to conflict check.")
parser.add_argument(
    "applicationName",
    help="The name of the application the branch exists in.")
parser.add_argument(
    "applicationVersion",
    help="The version of the application the branch exists in.")
args = parser.parse_args()

# Construct the URL based on input parameters
apiUrl = 'http://%s/prweb/api/v1/branches/%s/conflicts?applicationName=%s&applicationVersion=%s' % (
    args.baseUrl, args.branch, args.applicationName, args.applicationVersion)

# Perform the GET request to check for conflicts.
try:
    r = requests.get(apiUrl)
except ConnectionError as e:
    logging.info(
        "A connection error has occured when trying to run the REST command.")
    sys.exit(1)

# Check that the correct status code is returned
if r.status_code == 500:
    logging.info('Conflict details successfully obtained.')
else:
    logging.error("Unable to check for conflicts.")
    logging.error("STATUS CODE: %s" % (r.status_code))
    logging.error("RESPONSE: %s" % (r.text))
    sys.exit(1)

# Parse the JSON
details = json.loads(r.text)

# Retrieve the conflict count from the JSON
conflictCount = int(details["conflictsCount"])

# Check if there are any conflicts. If there are, fail the build
if conflictCount == 1:
    logging.error("Conflict Detected.")
    sys.exit(1)
else:
    logging.info('No conflicts were detected')
