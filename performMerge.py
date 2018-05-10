# coding: utf-8
import sys
import requests
import json
import logging
import os
import time
import argparse
from requests.exceptions import ConnectionError

# Set the log stream to output via stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# Parse inbound arguments
parser = argparse.ArgumentParser(description="Merge PEGA Branches")
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
parser.add_argument(
    "mergePolicy",
    help="The type of merge policy you want to use (Highest|New)")
args = parser.parse_args()

# Construct the URL based on input parameters
url = 'http://%s/prweb/api/v1/branches/%s/merge?applicationName=%s&applicationVersion=%s&mergePolicy=%s' % (
    args.baseUrl, args.branch, args.applicationName, args.applicationVersion, args.mergePolicy)

# Perform the GET request to check for conflicts.
try:
    r = requests.get(url)
except ConnectionError as e:
    logging.info(
        "Unable to connect to the specified URL. Please check the supplied parameters")
    sys.exit(1)

# Check that the correct status code is returned
if r.status_code == 200:
    logging.info('Merge successfully started.')
else:
    logging.error("Unable to merge. [HTTP response=%s]." % (r.text))

# Parse the JSON & read the ID
details = json.loads(r.text)

# Return the merge ID
mergeId = details["ID"]

# Construct the URL based on input parameters
statusUrl = 'http://%s/prweb/api/v1/merges/%s' % (args.baseUrl, mergeId)

# Begin the checking of merge status
for i in range(24):

    # Perform the REST command.
    try:
        statusResponse = requests.get(statusUrl)
    except ConnectionError as e:
        logging.info(
            "Unable to connect to the specified URL. Please check the supplied parameters")
        sys.exit(1)

    # Parse the JSON data
    statusDetails = json.loads(statusResponse.text)

    # Chech the status message of the merge
    if statusDetails["statusMessage"] == "Processing":
        logging.info('Merge is still processing')
        time.sleep(5)
    elif statusDetails["statusMessage"] == "Failure":
        logging.debug('Merge has failed')
        logging.debug(statusDetails["errors"][0]["message"])
        sys.exit(1)
    elif statusDetails["statusMessage"] == "Success":
        logging.debug('Merge was successful!')
        break

else:
    logging.debug('Merge has timed out')
    sys.exit(1)