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

        token_url = f"https://{self.host}/dna/system/api/v1/auth/token"

        response = requests.post(token_url,
                                auth=HTTPBasicAuth(self.user, self.password),
                                verify=self.verify)

        return response

    def _req(self, resource, method="GET", payload=None):
        """ Internal helper function to construct requests """

        token = self._get_token().json()["Token"]
        base_url = f"https://{self.host}/dna/intent/api/v1/"
        api_call_url = f"{base_url}{resource}"

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Auth-Token": token
        }

        response = requests.request(method=method,
                                    headers=headers,
                                    url=api_call_url,
                                    data=json.dumps(payload),
                                    verify=self.verify)

        return response

    def get_site_health(self):
        """ Fetches health of all sites available """

        site_health = self._req("site-health")

        return site_health

    def get_client_health(self):
        """ Fetches health of all clients available """

        client_health = self._req("client-health")

        return client_health

    def get_network_devices(self):
        """ Gets a list of devices in the network """

        network_devices = self._req("network-device")

        return network_devices

    def parsed_client_health(self):
        """ Parses an easier list of client health """

        clients = self.get_client_health().json()

        result = {}

        for category in clients["response"][0]["scoreDetail"]:
            result.update({category["scoreCategory"]["value"]:{}})

            #print(json.dumps(category, indent=2))
                
            if "scoreList" in category:
                scores = {}

                for score_category in category["scoreList"]:
                    scores.update({score_category["scoreCategory"]["value"]:score_category["clientCount"]})

                result.update({category["scoreCategory"]["value"]:scores})
            else:
                continue

        return result

if __name__ == "__main__":

    dnac_credentials = load_credentials("devnet_always_on")

    dnac_host = dnac_credentials["host"]
    dnac_user = dnac_credentials["username"]
    dnac_password = dnac_credentials["password"]

    dnac_instance = DNACHandler(dnac_host, dnac_user, dnac_password)

    devices = dnac_instance.get_network_devices().json()

    print(json.dumps(devices, indent=2))

    # for device in devices["response"]:
    #     print(device["macAddress"])

    #print(json.dumps(dnac_instance.parsed_client_health(), indent=2))
