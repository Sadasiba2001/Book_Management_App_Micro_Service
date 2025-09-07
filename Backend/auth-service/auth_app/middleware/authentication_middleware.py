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
            return HttpResponse("Invalid or expired token 1", status=401)
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
    def verify_jwt_token(token: str):
        
        try:            
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
            if not payload:
                raise ValueError("Invalid token payload.")
            return payload

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError) as e:
            raise ValueError("Invalid or expired token.")  # ✅ raise, not return

        except Exception as e:
            raise ValueError("Error verifying token.")  # ✅ raise, not return


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
        if not token:
            return HttpResponse("No token provided", status=401)

        try:
            payload = self.verify_jwt_token(token)
            if not payload:
                return HttpResponse("Payload not setup.\nToken can't authenticated.", status=401)

            user = self.get_user_from_payload(payload)
            if not user:
                return HttpResponse("Invalid user", status=401)

            request.user = user
            response = self.get_response(request)
            if not response:
                return HttpResponse("No response from view", status=500)

            return response
        except Exception as e:
            return HttpResponse(f"Authentication error: {str(e)}", status=401)