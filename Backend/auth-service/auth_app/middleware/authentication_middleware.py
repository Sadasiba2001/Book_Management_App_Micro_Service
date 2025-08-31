import jwt
from functools import wraps
from typing import Optional
from django.conf import settings
from django.http import HttpResponse
from auth_app.models import User


def jwt_auth_required(view_func):
    """
    Decorator to enforce JWT authentication on a view.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        token = JWTMiddleware.get_token_from_request(request)
        if not token:
            return HttpResponse("No token provided", status=401)
        payload = JWTMiddleware.verify_jwt_token(token)
        if not payload:
            return HttpResponse("Invalid or expired token", status=401)
        user = JWTMiddleware.get_user_from_payload(payload)
        if not user:
            return HttpResponse("Invalid user", status=401)
        request.user = user
        return view_func(request, *args, **kwargs)
    return wrapper

class JWTMiddleware:
    """
    Middleware to handle JWT authentication.
    """
    def __init__(self, get_response):
        self.get_response = get_response
    

    """
    # Helper
    # Function to extract JWT token from the backend cookies.
    # If not in cookies, it checks the Authorization header.
    """
    @staticmethod
    def get_token_from_request(request) -> Optional[str]:
        
        """
        # Extract JWT token from backend cookies.
        """
        token = request.COOKIES.get('access_token')

        """
        # If not in cookies, it checks the Authorization header.
        """
        if not token and request.headers.get('Authorization'):
            auth_header = request.headers.get('Authorization')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        return token

    """
    # Helper
    # Verify and decode a JWT token.
    """
    @staticmethod
    def verify_jwt_token(token: str) -> Optional[dict]:
        
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return None

    """
    # Helper
    # Function to retrieve user from JWT payload.
    """
    @staticmethod
    def get_user_from_payload(payload: dict) -> Optional[User]:
        """
        Retrieve user from JWT payload.
        """
        try:
            user_id = payload.get('user_id')
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    """
    # Main Function
    # Middleware call method.
    """
    def __call__(self, request):
        requested_path = ['/api/auth/login/', '/api/auth/register/']
        if request.path in requested_path:
            return self.get_response(request)
        token = self.get_token_from_request(request)
        if token:
            payload = self.verify_jwt_token(token)
            if payload:
                user = self.get_user_from_payload(payload)
                if user:
                    request.user = user
                else:
                    return HttpResponse("Invalid user", status=401)
            else:
                return HttpResponse("Invalid or expired token", status=401)
        response = self.get_response(request)
        return response