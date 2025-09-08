import time
from ..models import User
from ..utils import JWTUtils
from rest_framework import status
from typing import Optional, Tuple
from ..repositories import UserRepository
from rest_framework.response import Response
from ..constants.response_template import SUCCESS_RESPONSE, ERROR_RESPONSE

class UserService:
    
    @staticmethod
    def register_user(
        firstname: str, 
        lastname: str, 
        email: str, 
        password: str,         
        is_superuser: bool,
        is_staff: bool,
        is_active: bool
        ) :
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
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=is_active
            )

            if not user:
                return ResponseUtils.error(
                    message="User creation failed.",
                    error="User creation failed.",
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)
            if not jwt_token:
                return ResponseUtils.error(
                    message="JWT token generation failed.",
                    error="JWT token generation failed.",
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            
            return user, jwt_token 
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, "An unexpected error occurred during registration."

    @staticmethod
    def login_user(email: str, password: str) -> Tuple[Optional[User], Optional[str]]:
        start = time.time()
        """
        Business logic for user login.
        Returns a tuple of (user_object, error_message).
        """
        print("SERVICE: Step 1 time:", time.time() - start)
        if not email or not password:
            return None, None

        print("SERVICE: Step 2 time:", time.time() - start)
        try:           

            print("SERVICE: Step 3 time:", time.time() - start)
            user = UserRepository.get_login_user_details(email)
            if not user:    
                return None, None

            print("SERVICE: Step 4 time:", time.time() - start)
            if not user.check_password(password):
                return None, None

            print("SERVICE: Step 5 time:", time.time() - start)
            jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)
            if not jwt_token:
                return None, None

            print("SERVICE: Step 6 time:", time.time() - start)
            return user, jwt_token

        except Exception as e:
            return None, None, f"An error occurred during login: {str(e)}"

    @staticmethod
    def get_user (userId: str, email: str) -> Tuple[Optional[User], Optional[str]]:
        """Business logic for retrieving a user by various criteria."""
        
        if (userId):
            user = UserRepository.get_user_by_id(userId)
            if not user:
                return None, "User not found."
        elif(email):
            user = UserRepository.get_user_by_email(email)
            if not user:
                return None, "User not found."
        else:
            user = UserRepository.get_all_users()
            if not user:
                return None, "User not found."
        return user, None

    @staticmethod
    def get_user_profile(user_id: int) -> Optional[User]:
        """Business logic for retrieving a user's profile."""
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def find_user_by_email(email: str) -> Optional[User]:
        """Business logic for finding a user by email."""
        return UserRepository.get_user_by_email(email)
    
    @staticmethod
    def delete_user(user_id=None, email=None) -> bool:
        """
        Deletes a user by ID or Email.
        Returns True if user was deleted, False if not found.
        """
        return UserRepository.delete_user_by_id_or_email(user_id, email)

    @staticmethod
    def logout_user(request, user) -> tuple[Response, str]:
        """
        Handles the logout by returning a response that clears the JWT cookie.
        """
        if not user or not user.is_authenticated:
            return None, "Unauthorized. Valid token required."

        try:
            response = ResponseUtils.success(
                message="User logged out successfully",
                data={},  # Empty data object
                http_status=status.HTTP_200_OK
            )
            response.delete_cookie(
                key='access_token',
                samesite='Lax',
                secure=False,
                httponly=True
            )
            return response, None

        except Exception as e:
            return None, str(e)
