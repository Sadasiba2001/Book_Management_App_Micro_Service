from typing import Optional, Tuple
from django.contrib.auth import authenticate
from ..models import User
from ..repositories import UserRepository
from ..utils import JWTUtils

class UserService:
    
    @staticmethod
    def register_user(
        firstname: str, 
        lastname: str, 
        email: str, 
        password: str,         
        **extra_fields
        ) -> Tuple[Optional[User], Optional[str]]:
        """
        Business logic for user registration.
        Returns a tuple of (user_object, error_message).
        """
        try:
            user = UserRepository.create_user(
                email=email,
                password=password,
                firstname=firstname,
                lastname=lastname,  
                **extra_fields
            )

            jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)

            return user, jwt_token, None
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, "An unexpected error occurred during registration."

    @staticmethod
    def login_user(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        """
        Business logic for user login.
        Returns a tuple of (user_object, error_message).
        """
        user = UserRepository.get_user_by_email(email)
        if not user:
            return None, "User not found."

        if not user.verify_password(password):
            return None, "Invalid password."

        jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)

        return user, jwt_token, None

    @staticmethod
    def get_user_profile(user_id: int) -> Optional[User]:
        """Business logic for retrieving a user's profile."""
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def find_user_by_email(email: str) -> Optional[User]:
        """Business logic for finding a user by email."""
        return UserRepository.get_user_by_email(email)