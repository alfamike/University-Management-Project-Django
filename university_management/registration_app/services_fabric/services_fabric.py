import os

from hfc.fabric import Client


def get_fabric_client():
    fabric_client = Client(net_profile=os.path.join(os.path.dirname(__file__), 'connection-profile.yaml'))

    return fabric_client
