import base64
import os

from cryptography.hazmat.backends import default_backend
from cryptography.x509.oid import NameOID
from cryptography import x509
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from registration_app.services_fabric.services_fabric import FabricClientSingleton


@csrf_exempt
def login_auth(request):
    client_cert_base64 = request.META.get('HTTP_X_SSL_CERT')
    if not client_cert_base64:
        return JsonResponse({"error": "No client certificate provided."}, status=400)

    try:
        # Decode the base64 certificate
        client_cert_pem = base64.b64decode(client_cert_base64).decode('utf-8')
        client_cert = x509.load_pem_x509_certificate(client_cert_pem.encode(), default_backend())

        # Validate the certificate against the CA
        store = x509.CertificateStore()
        store.add_cert(CA_CERT)

        # Create a verification context
        context = x509.CertificateVerificationContext(store)

        # Validate the client certificate
        context.verify_certificate(client_cert)

        # Extract relevant fields
        subject = client_cert.subject
        username = subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value

        print(f"Certificate Subject: {subject}")
        print(f"User identified as: {username}")

        # Init Hyperledge Fabric connection
        FabricClientSingleton(user_cn=username)

    except Exception as e:
        return JsonResponse({"error": f"Certificate validation failed: {str(e)}"}, status=400)

    return JsonResponse({"success": "Certificate validated"})


def load_ca_certificate(ca_cert_path):
    try:
        with open(ca_cert_path, "rb") as f:
            ca_cert = x509.load_pem_x509_certificate(f.read(), default_backend())
        return ca_cert
    except Exception as e:
        raise ValueError(f"Failed to load CA certificate: {str(e)}")


# Path to CA certificate
CA_CERT_PATH = os.path.join(
    os.path.dirname(__file__),
    'auth/ca.university.eu-cert.pem'
)

# Load the CA certificate
CA_CERT = load_ca_certificate(CA_CERT_PATH)
