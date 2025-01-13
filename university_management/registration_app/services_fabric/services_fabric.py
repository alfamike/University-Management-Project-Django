import asyncio
import json
import os
import traceback
from threading import Lock
from hfc.fabric import Client
from hfc.fabric_ca.caservice import Enrollment
from hfc.fabric_network import wallet
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from hfc.util.keyvaluestore import FileKeyValueStore
from hfc.fabric.user import User


class FabricClientSingleton:
    _instance = None
    _lock = Lock()
    _user = None
    _initialized = False
    _fabric_client = None

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if not cls._instance:
                cls._instance = super(FabricClientSingleton, cls).__new__(cls)
                cls._instance.init_client()
                cls._instance._initialized = True
        return cls._instance

    def init_client(self):
        try:
            new_wallet = wallet.FileSystenWallet('crypto_store/wallet')

            # Identity creation
            with open('certs/admin_cert.pem', 'rb') as cert_file:
                cert_data = cert_file.read()

            with open('certs/admin_key', 'rb') as key_file:
                private_key_data = key_file.read()
            private_key = serialization.load_pem_private_key(private_key_data, password=None)

            user_identity = wallet.Identity("admin", Enrollment(private_key, cert_data))
            user_identity.CreateIdentity(new_wallet)

            # State store creation
            with open('crypto_store/wallet/admin/enrollmentCert.pem', 'rb') as cert_file:
                cert_data = cert_file.read()
            cert_wallet = load_pem_x509_certificate(cert_data)

            with open('crypto_store/wallet/admin/private_sk', 'rb') as key_file:
                private_key_data = key_file.read()
            key_wallet = serialization.load_pem_private_key(private_key_data, password=None)

            key_wallet_bytes = key_wallet.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            state_store = FileKeyValueStore('crypto_store/hfc-kvs')

            enrollment = json.dumps({
                'private_key': key_wallet_bytes.decode('utf-8'),
                'certificate': cert_data.decode('utf-8')
            })

            # state_store.set_value('Admin@Org1', enrollment)

            # User creation
            if not state_store.get_value('user.Admin.Org1'):
                admin = User('Admin', 'Org1', state_store)
            else:
                admin = state_store.get_value('user.Admin.Org1')

            self._user = admin

            # Client setup
            # Ensure the event loop is set for the current thread
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:  # No event loop in the current thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            connection_profile_path = os.path.join(
                os.path.dirname(__file__),
                'connection-profile.json'
            )

            if not os.path.exists(connection_profile_path):
                raise FileNotFoundError(f"Connection profile not found at {connection_profile_path}")

            self._fabric_client = Client(net_profile=connection_profile_path)

            if not self._fabric_client:
                raise RuntimeError("Fabric client is None after initialization."+ traceback.format_exc() )

        except Exception as e:
            raise RuntimeError(f"Failed to initialize Fabric client: {e}")

    def get_client(self):
        if not self._initialized or not self._fabric_client:
            raise ValueError("Fabric client is not initialized." + "get_client" + traceback.format_exc())
        return self._fabric_client

    def get_user(self):
        if not self._initialized or not self._fabric_client:
            raise ValueError("Fabric client is not initialized." + "get_user" + traceback.format_exc())
        return self._user


def query_chaincode(client, user, chaincode_name, function, args):
    return client.chaincode_query(
        requestor=user,
        channel_name='registration-channel',
        peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )


def invoke_chaincode(client, user, chaincode_name, function, args):
    return client.chaincode_invoke(
        requestor=user,
        channel_name='registration-channel',
        peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
        args=args,
        cc_name=chaincode_name,
        fcn=function
    )
