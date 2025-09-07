import jwt
from django.conf import settings
from datetime import datetime, timedelta
from typing import Dict, Optional

class JWTUtils:
    """
    Utility class for JWT token operations
    """

    @staticmethod
    def generate_jwt_token(user_id: int, email: str) -> str:
        """
        Generate a JWT token for a user
        """

        if (not user_id or not email):
            raise ValueError("User ID and email are required to generate JWT token.")

        if not settings.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY is not set or is empty")

        if not settings.JWT_ALGORITHM:
            raise ValueError("JWT_ALGORITHM is not set or is empty")

        if not settings.JWT_ACCESS_TOKEN_LIFETIME_HOURS:
            raise ValueError("JWT_ACCESS_TOKEN_LIFETIME_HOURS is not set or is empty")


        try:
            print(f"ENCODE: The secret key is: {settings.JWT_SECRET_KEY}\nThe algorithm is: {settings.JWT_ALGORITHM}")
            payload = {
                'user_id': user_id,
                'email': email,
                'exp': datetime.utcnow() + timedelta(hours=int(settings.JWT_ACCESS_TOKEN_LIFETIME_HOURS)),
                'iat': datetime.utcnow()
            }

            token = jwt.encode(
                payload, 
                settings.JWT_SECRET_KEY, 
                algorithm=settings.JWT_ALGORITHM
            )
            print("ENCODED: Generated JWT token:", token)

            return token
        except Exception as e:
            print("Error generating JWT token:", e)
            return None

    @staticmethod
    def verify_jwt_token(token: str) -> Optional[Dict]:
        """
        Verify and decode a JWT token
        """
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except jwt.ExpiredSignatureError:
            return None  
        except jwt.InvalidTokenError:
            return None

    @staticmethod
    def get_token_from_request(request):
        """
        Extract JWT token from request cookies
        """
        return request.COOKIES.get('access_token')