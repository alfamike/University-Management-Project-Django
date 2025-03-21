import asyncio
import os
import traceback

from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate
from hfc.fabric.user import create_user
from hfc.fabric_ca.caservice import Enrollment
from hfc.fabric_network import wallet
from hfc.fabric_network.gateway import Gateway
from hfc.util.consts import CC_TYPE_JAVA
from hfc.util.crypto.crypto import Ecies
from hfc.util.keyvaluestore import FileKeyValueStore


class HyperledgeFabric:
    @classmethod
    def init_connection(cls):
        try:
            # Wallet and state_store
            new_wallet = wallet.FileSystenWallet('crypto_store/wallet')
            state_store = FileKeyValueStore('crypto_store/hfc-kvs')

            # Identity creation
            with open('crypto_store/hfc-cvs/Org1/Admin/cert.pem', 'rb') as cert_file:
                cert_data = cert_file.read()
            cert_admin = load_pem_x509_certificate(cert_data).public_bytes(encoding=serialization.Encoding.PEM)

            with open('crypto_store/hfc-cvs/Org1/Admin/key.pem', 'rb') as key_file:
                private_key_data = key_file.read()
            admin_private_key = serialization.load_pem_private_key(private_key_data, password=None)
            admin_private_key_pem = admin_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            with open('crypto_store/hfc-cvs/Org1/Django/cert.pem', 'rb') as cert_file:
                cert_data_django = cert_file.read()
            cert_django = load_pem_x509_certificate(cert_data_django).public_bytes(encoding=serialization.Encoding.PEM)

            with open('crypto_store/hfc-cvs/Org1/Django/key.pem', 'rb') as key_file:
                private_key_data = key_file.read()
            django_private_key = serialization.load_pem_private_key(private_key_data, password=None)
            django_private_key_pem = django_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            # admin_identity_path = os.path.join('crypto_store/wallet', 'admin_org1')

            # if not new_wallet.exists('admin_org1'):
            #     print("Admin identity not found in the wallet. Adding identity...")
            #     user_identity = wallet.Identity("admin_org1", Enrollment(admin_private_key, cert_data))
            #     user_identity.CreateIdentity(new_wallet)
            #
            #     # os.makedirs(admin_identity_path, exist_ok=True)
            #     # with open(os.path.join(admin_identity_path, 'enrollmentCert.pem'), 'wb') as cert_file:
            #     #     cert_file.write(cert_data)
            #     # with open(os.path.join(admin_identity_path, 'private_sk'), 'wb') as key_file:
            #     #     key_file.write(private_key_data)
            #
            #     # enrollment = Enrollment(private_key, cert_data)
            #     print("Admin identity added to the wallet.")
            # else:
            #     print("Admin identity already exists in the wallet.")

            if not new_wallet.exists('django'):
                print("Django identity not found in the wallet. Adding identity...")
                django_identity = wallet.Identity("django", Enrollment(django_private_key, cert_data_django))
                django_identity.CreateIdentity(new_wallet)

                # os.makedirs(admin_identity_path, exist_ok=True)
                # with open(os.path.join(admin_identity_path, 'enrollmentCert.pem'), 'wb') as cert_file:
                #     cert_file.write(cert_data)
                # with open(os.path.join(admin_identity_path, 'private_sk'), 'wb') as key_file:
                #     key_file.write(private_key_data)

                # enrollment = Enrollment(private_key, cert_data)
                print("Django identity added to the wallet.")
            else:
                print("Django identity already exists in the wallet.")

            # Set the connection profile path
            connection_profile_path = os.path.join(
                os.path.dirname(__file__),
                'connection-profile.json'
            )

            # Validate the connection profile path
            if not os.path.exists(connection_profile_path):
                raise FileNotFoundError(f"Connection profile not found at {connection_profile_path}")

            # # Ensure the event loop is set for the current thread
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
            except RuntimeError:  # No event loop in the current thread or loop is closed
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            # Initialize the Fabric client
            # client = Client(net_profile=connection_profile_path)
            crypto_suite = Ecies()
            # client.cryptoSuite = crypto_suite
            # client.state_store = state_store
            # client.kv_store_path = 'crypto_store/hfc-kvs'

            # admin_user = create_user(name='Admin', org='org1.university.eu', msp_id='Org1MSP',
            #                          state_store=state_store,
            #                          cert_pem=cert_admin, key_pem=admin_private_key_pem, crypto_suite=crypto_suite)

            django_user = create_user(name='Django', org='org1.university.eu', msp_id='Org1MSP',
                                      state_store=state_store,
                                      cert_pem=cert_django, key_pem=django_private_key_pem, crypto_suite=crypto_suite)

            new_gateway = Gateway()
            options = {'wallet': 'crypto_store/wallet'}
            loop.run_until_complete(new_gateway.connect(connection_profile_path, options))

            # # Check if the client is successfully created
            # if client is None:
            #     raise RuntimeError("Fabric client is None after initialization.")
            #
            # if not client.get_user('org1.university.eu', 'Admin'):
            #     admin_user = create_user(name='Admin', org='org1.university.eu', msp_id='Org1MSP',
            #                              state_store=state_store,
            #                              cert_pem=cert_admin, key_pem=admin_private_key_pem, crypto_suite=crypto_suite)
            # else:
            #     admin_user = client.get_user('org1.university.eu', 'Admin')

            new_network = loop.run_until_complete(
                new_gateway.get_network('registration-channel', requestor=django_user))
            print(new_network)
            new_contract = new_network.get_contract('title_cc')

            client = new_gateway.get_client()

            # with open('crypto_store/wallet/admin_org1/enrollmentCert.pem', 'rb') as cert_file:
            #     cert_data = cert_file.read()
            # cert_wallet = load_pem_x509_certificate(cert_data)
            #
            # with open('crypto_store/wallet/admin_org1/private_sk', 'rb') as key_file:
            #     private_key_data = key_file.read()
            # key_wallet = serialization.load_pem_private_key(private_key_data, password=None)
            #
            # key_wallet_bytes = key_wallet.private_bytes(
            #     encoding=serialization.Encoding.PEM,
            #     format=serialization.PrivateFormat.PKCS8,
            #     encryption_algorithm=serialization.NoEncryption()
            # )
            #
            # enrollment = Enrollment(key_wallet, cert_data)

            print("Fabric client initialized successfully with the wallet and state store.")
            return client, django_user

        except FileNotFoundError as e:
            error_message = f"FileNotFoundError: {e}"
            raise RuntimeError(error_message)

        except asyncio.CancelledError:
            raise RuntimeError("Event loop was cancelled unexpectedly.")

        except Exception as e:
            error_message = f"Failed to initialize Fabric client: {e} | Traceback: {traceback.format_exc()}"
            print(error_message)

    @classmethod
    def query_chaincode(cls, chaincode_name, function, args):
        client, user = cls.init_connection()
        try:
            loop = asyncio.get_event_loop()
            if loop.is_closed():
                raise RuntimeError("Existing event loop is closed. Creating a new event loop.")
        except RuntimeError:  # No event loop in the current thread or loop is closed
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(client.chaincode_query(
            requestor=user,
            channel_name='registration-channel',
            peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
            args=args,
            cc_name=chaincode_name,
            cc_type=CC_TYPE_JAVA,
            fcn=function
        ))

    @classmethod
    def invoke_chaincode(cls, chaincode_name, function, args):
        client, user = cls.init_connection()
        return client.chaincode_invoke(
            requestor=user,
            channel_name='registration-channel',
            peers=['peer0.org1.university.eu', 'peer1.org1.university.eu'],
            args=args,
            cc_name=chaincode_name,
            cc_type=CC_TYPE_JAVA,
            fcn=function
        )
