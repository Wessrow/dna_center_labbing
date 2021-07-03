#!/usr/bin/python3

"""
DNA Center Lab for DEVCOR
Gustav Larsson
"""

import json
import requests
from requests.auth import HTTPBasicAuth

def load_credentials(host):
    """ Functions written to help with testing """

    with open("credentials.json", "r") as handle:

        credentials = json.load(handle)[host]

    return credentials

class DNACHandler:
    """ SDK to help with DNAC management """

    def __init__(self, host, user, password, verify=False):
        """ Constructor for the class, assigns variables """

        self.host = host
        self.user = user
        self.password = password
        self.verify = verify

        if verify is False:
            requests.urllib3.disable_warnings()

    def _get_token(self):
        """ Internal helper fucntion to handle authentication """

        token_url = f"https://{self.host}//dna/system/api/v1/auth/token"

        response = requests.post(token_url,
                                auth=HTTPBasicAuth(self.user, self.password),
                                verify=self.verify)

        return response

    def _req(self):
        """ Internal helper function to construct requests """

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": self._get_token()
        }

if __name__ == "__main__":


    dnac_credentials = load_credentials("devnet_always_on")

    dnac_host = dnac_credentials["host"]
    dnac_user = dnac_credentials["username"]
    dnac_password = dnac_credentials["password"]

    dnac_instance = DNACHandler(dnac_host, dnac_user, dnac_password)

    print(dnac_instance._get_token())
