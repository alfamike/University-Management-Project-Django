import asyncio
import json
import os
import traceback

from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from hfc.fabric import Client
from hfc.fabric.user import User
from hfc.fabric_ca.caservice import Enrollment
from hfc.fabric_network import wallet
from hfc.util.keyvaluestore import FileKeyValueStore


def init_connection():
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

        # Client setup
        # Ensure the event loop is set for the current thread
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        # Set the connection profile path
        connection_profile_path = os.path.join(
            os.path.dirname(__file__),
            'connection-profile.json'
        )

        # Validate the connection profile path
        if not os.path.exists(connection_profile_path):
            raise FileNotFoundError(f"Connection profile not found at {connection_profile_path}")

        # Initialize the Fabric client
        client = Client(net_profile=connection_profile_path)

        # Check if the client is successfully created
        if not client:
            raise RuntimeError("Fabric client is None after initialization.")

        print("Fabric client successfully initialized.")

    except FileNotFoundError as e:
        error_message = f"FileNotFoundError: {e}"
        print(error_message)
        raise RuntimeError(error_message)

    except asyncio.CancelledError:
        # Handle specific asyncio error if applicable
        raise RuntimeError("Event loop was cancelled unexpectedly.")

    except Exception as e:
        error_message = f"Failed to initialize Fabric client: {e} | Traceback: {traceback.format_exc()}"
        print(error_message)
        raise RuntimeError(error_message)


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
