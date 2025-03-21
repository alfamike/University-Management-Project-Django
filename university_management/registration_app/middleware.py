import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JWTAuthenticationMiddleware(MiddlewareMixin):
    """
    Middleware for handling JWT authentication in incoming requests.
    """

    def process_request(self, request):
        """
        Process the incoming request for JWT authentication.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            JsonResponse or None: Returns a JsonResponse with an error message if authentication fails,
                                  otherwise returns None to continue processing the request.
        """
        # Allow unauthenticated access to specific paths
        allowed_paths = ['/', '/get_nonce', '/verify_signature']
        if any(request.path.startswith(path) for path in allowed_paths):
            return None

        # Retrieve the token from cookies
        token = request.COOKIES.get('auth_token')

        if not token:
            # Return an error response if the token is missing
            return JsonResponse({'error': 'Authorization token missing'}, status=401)
        else:
            try:
                # Decode the JWT token
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                # Attach the user address to the request
                request.user_address = payload['address']
            except jwt.ExpiredSignatureError:
                # Return an error response if the token has expired
                return JsonResponse({'error': 'Access token expired', 'refresh': True}, status=401)
            except jwt.InvalidTokenError:
                # Return an error response if the token is invalid
                return JsonResponse({'error': 'Invalid token'}, status=401)

        return None
