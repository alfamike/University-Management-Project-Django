import jwt
from django.conf import settings
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        """
        Process the incoming request for JWT authentication.
        """
        # Allow unauthenticated access to specific paths
        allowed_paths = ['/login', '/get_nonce', '/verify_signature']
        if any(request.path.startswith(path) for path in allowed_paths):
            return None

        token = request.COOKIES.get('auth_token')

        if not token:
            return JsonResponse({'error': 'Authorization token missing'}, status=401)
        else:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                request.user_address = payload['address']  # Attach address to the request
            except jwt.ExpiredSignatureError:
                return JsonResponse({'error': 'Access token expired', 'refresh': True}, status=401)
            except jwt.InvalidTokenError:
                return JsonResponse({'error': 'Invalid token'}, status=401)

        return None  # Continue processing if authentication is successful
