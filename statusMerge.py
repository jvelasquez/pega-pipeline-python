# coding: utf-8
import sys
import requests
import json
import logging
import os
import time
from requests.exceptions import ConnectionError

# Set the log stream to output via stdout
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#Parse inbound arguments
parser = argparse.ArgumentParser(description="Checks the status of a PEGA merge")
parser.add_argument("baseUrl", help="The base url of the server. This should not include http://, https:// or /prweb. It should be in the form 'example.com'.")
parser.add_argument("mergeID", help="The ID of the merge you want to check the status of")
args = parser.parse_args()

#Construct the URL based on input parameters
url = 'http://%s/api/v1/merges/%s' % (args.baseUrl, mergeId)

#Begin the checking of merge status
for i in range(24):
    
    try:
        r = requests.get(url)
    except ConnectionError as e:
        logging.info("Unable to connect to the specified URL. Please check the supplied parameters")
        sys.exit(1)

    details =  json.loads(r.text)

    if mergeCheckDetails["statusMessage"] == "Processing":
        logging.info('Merge is still processing')
        time.sleep(5)

    elif mergeCheckDetails["statusMessage"] == "Failure":
        logging.debug('Merge has failed')
        logging.debug(mergeCheckDetails["errors"][0]["message"])
        sys.exit(1)

    elif mergeCheckDetails["statusMessage"] == "Success":
        logging.debug('Merge was successful!')
        break
        
else:
    logging.debug('Merge has timed out')
    sys.exit(1)