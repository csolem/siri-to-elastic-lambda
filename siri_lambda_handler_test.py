#!/usr/bin/env python

# Simple test script that calls siri lambda handler

import unittest

from siri_lambda_handler import allow_content, transform_siri_data



class TestLambdaHandler(unittest.TestCase):

    # Test that a heartbeat XML can be converted into a suitable flattened dict
    def test_heartbeat(self):

        heart_beat_xml = '''<?xml version="1.0" encoding="UTF-8"?>
            <Siri xmlns="http://www.siri.org.uk/siri" xmlns:ns2="http://www.ifopt.org.uk/acsb" xmlns:ns3="http://www.ifopt.org.uk/ifopt" xmlns:ns4="http://datex2.eu/schema/2_0RC1/2_0" version="2.0">
            <HeartbeatNotification>
                <RequestTimestamp>2018-12-06T13:35:39.249+01:00</RequestTimestamp>
                <ProducerRef>2d1a7f9a-f938-11e8-9f70-186590dd94c5</ProducerRef>
                <Status>true</Status>
                <ServiceStartedTime>2018-11-28T06:59:43.989+01:00</ServiceStartedTime>
            </HeartbeatNotification>
            </Siri>
        '''

        # Create event object
        event = {
		    "bodyXml" : heart_beat_xml
        }

        result = transform_siri_data(event)

        print(result)

        self.assertTrue('HeartbeatNotification' in result)
        self.assertTrue('@xmlns' not in result)


    # Allthough heartbeat can be parsed and transformed it should not be indexed
    def test_do_not_allow_heartbeat(self):
        transformed_siri_data = {}
        transformed_siri_data["HeartbeatNotification"] = {}
        result = allow_content(transformed_siri_data)
        self.assertFalse(result)

    # TODO: More tests

if __name__ == '__main__':
    unittest.main()