import os
from threading import Lock

from hfc.fabric import Client


class FabricClientSingleton:
    _instance = None
    _lock = Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(FabricClientSingleton, cls).__new__(cls, *args, **kwargs)
                cls._instance._initialized = False
            return cls._instance

    def __init__(self, user_cn=None):
        if not self._initialized:
            self._fabric_client = None
            self._user = None
            self._initialized = True

        if user_cn:
            self.init_client(user_cn)

    def init_client(self, user_cn):
        if not self._fabric_client:
            connection_profile_path = os.path.join(
                os.path.dirname(__file__),
                'connection-profile.json'
            )
            self._fabric_client = Client(net_profile=connection_profile_path)
            self._user = self._fabric_client.get_user(org_name='org1.university.eu', name=user_cn)

    def get_client(self):
        if not self._fabric_client:
            raise ValueError("Fabric client is not initialized. Call init_client() first.")
        return self._fabric_client

    def get_user(self):
        if not self._user:
            raise ValueError("Fabric client user is not initialized. Call init_client() first.")
        return self._user


def query_chaincode(client, user, chaincode_name, function, args):
    return client.chaincode_query(
        requestor=user,
        channel_name='registration_app',
        peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )


def invoke_chaincode(client, user, chaincode_name, function, args):
    return client.chaincode_invoke(
        requestor=user,
        channel_name='registration_app',
        peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )
