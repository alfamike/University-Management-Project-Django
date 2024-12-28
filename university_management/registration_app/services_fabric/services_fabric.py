import os

from hfc.fabric import Client


def get_fabric_client():
    fabric_client = Client(net_profile=os.path.join(os.path.dirname(__file__), 'connection-profile.yaml'))
    return fabric_client


def query_chaincode(client, chaincode_name, function, args):
    return client.chaincode_query(
        requestor='Admin',
        channel_name='mychannel',
        peers=['peer0.org1.example.com'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )


def invoke_chaincode(client, chaincode_name, function, args):
    return client.chaincode_invoke(
        requestor='Admin',
        channel_name='mychannel',
        peers=['peer0.org1.example.com'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )
