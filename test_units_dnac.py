#!/usr/bin/python3

"""
Unit tests for DNAC Handler Functoins
Written by Gustav Larsson
"""

import json
from dna_funcitons import DNACHandler

def load_credentials(host):
    """ Loads credentials of test instance """

    with open("credentials.json", "r") as handle:

        credentials = json.load(handle)[host]

    return credentials

def construct_handler():
    """ Function to build test instance of class """

    dnac_credentials = load_credentials("devnet_always_on")

    dnac_host = dnac_credentials["host"]
    dnac_user = dnac_credentials["username"]
    dnac_password = dnac_credentials["password"]

    dnac_instance = DNACHandler(dnac_host, dnac_user, dnac_password)

    return dnac_instance

# Global instance of the DNAC Handler to only create the object once for testing
DNAC_TEST_INSTANCE = construct_handler()

def test_token_authentication():
    """ Tests authentication with given credentials """

    assert DNAC_TEST_INSTANCE._get_token().status_code != 401

def test_valid_token():
    """ Tests the validity of the returned token """

    assert DNAC_TEST_INSTANCE.get_client_health().status_code == 200
