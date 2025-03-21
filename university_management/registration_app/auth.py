import binascii
import json
import os
from datetime import datetime, timedelta

import jwt
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from eth_account.messages import encode_defunct
from web3 import Web3

# Temporary storage for nonces
NONCE_STORAGE = {}


def generate_nonce():
    """
    Generate a random nonce for the user.

    Returns:
        str: A random nonce as a hexadecimal string.
    """
    return binascii.hexlify(os.urandom(16)).decode()


@csrf_exempt
def get_nonce(request):
    """
    Generate a random nonce for the user.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response containing the generated nonce or an error message.
    """
    data = json.loads(request.body)
    address = data.get('address', '')

    if not address:
        return JsonResponse({'error': 'Address is required'}, status=400)

    nonce = generate_nonce()
    NONCE_STORAGE[address] = nonce  # Store nonce temporarily
    return JsonResponse({'nonce': nonce})


@csrf_exempt
def verify_signature(request):
    """
    Verify the signature provided by the user.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        JsonResponse: A JSON response indicating the result of the verification process.
    """
    data = json.loads(request.body)
    address = data.get('address', '')
    signature = data.get('signature', '')

    if not address or not signature:
        return JsonResponse({'error': 'Address and signature are required'}, status=400)

    nonce = NONCE_STORAGE.get(address)
    if not nonce:
        return JsonResponse({'error': 'Nonce not found or expired'}, status=400)

    # Verify the signature using web3
    w3 = Web3()
    message = encode_defunct(text=nonce)

    try:
        # Recover the address from the signature
        recovered_address = w3.eth.account.recover_message(message, signature=signature)
    except ValueError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if recovered_address.lower() == address.lower():
        # Authentication successful, generate JWT tokens
        access_token = generate_tokens(address)
        response = JsonResponse({
            'success': True,
            'message': 'Authentication successful',
            'access_token': access_token,
        })

        # Set the cookie
        response.set_cookie(
            'auth_token',
            access_token,
            httponly=True,  # Prevent JavaScript access
            secure=False,  # Only over HTTPS
            max_age=int(timedelta(days=1).total_seconds()),  # Cookie lifespan
        )

        return response
    else:
        return JsonResponse({'error': 'Authentication failed'}, status=400)


def generate_tokens(address):
    """
    Generate JWT tokens for the authenticated user.

    Args:
        address (str): The user's address.

    Returns:
        str: The generated JWT access token.
    """
    payload = {
        'address': address,
        'exp': datetime.utcnow() + timedelta(hours=24)  # Short-lived access token
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    return access_token
