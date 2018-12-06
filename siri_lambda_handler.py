#!/usr/bin/env python

# AWS lambda function handler for converting
# real time SIRI XML messages to JSON
# and posting it to elastic

# Use linter with pip3 install pylint and vscode

import json
import xmltodict
import logging
import sys
from elasticsearch import Elasticsearch

logger = logging.getLogger(__name__)

# Set log level to INFO to avoid debug output
logger.setLevel(logging.DEBUG)
log_handler = logging.StreamHandler(sys.stdout)
log_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(log_handler)

# Filter out namespace keys
# Flattens dict one level, to avoid the first 'Siri' level.
def transform_siri_data(event):
    siri_data = xmltodict.parse(event.get('bodyXml'))
    logger.debug("Filter out values starting with '@' from siri data %s", siri_data)

    filtered_siri_data = {}
    # The actual dict is located under the 'Siri' key
    if 'Siri' in siri_data:
        # Dict in dict
        siri_sub_dict = siri_data.get('Siri')
        for key in siri_sub_dict.keys():
            if not key.startswith('@'):
                filtered_siri_data[key] = siri_sub_dict.get(key)
            else:
                logger.debug("Filtering out key from dict: %s", key)
    return filtered_siri_data

# Ignore certain types of siri data if not suitable for indexing
def allow_content(transformed_siri_data):
    print(transformed_siri_data)
    if 'HeartbeatNotification' in transformed_siri_data:
        return False

    # Defaults to true for now
    return True

def post_to_elastic(transformed_siri_data):
    es = Elasticsearch(['https://localhost:9200'])
    res = es.index(index="siri-data", doc_type='siri', id=1, body=transformed_siri_data)
    logger.info("Result from ES: %s", res['result'])

# The lambda function called by AWS
def lambda_handler(event, context):

    logger.debug("Received event. Converting body xml to dict")

    transformed_siri_data = transform_siri_data(event)

    logger.debug(transformed_siri_data)

    if allow_content(transformed_siri_data):
        logger.info("Data is suitable for indexing")
        logger.debug("Converting to json")
        post_to_elastic(transformed_siri_data)


    return {
        'statusCode': '200',
        'body': 'ok'
    }
