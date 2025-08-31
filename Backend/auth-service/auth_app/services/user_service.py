from typing import Optional, Tuple
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
        is_superuser: bool,
        is_staff: bool,
        is_active: bool
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
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=is_active
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
        user = UserRepository.get_login_user_details(email)
        if not user:
            return None, "User not found."

        if not user.check_password(password):
            return None, "Invalid password."

        jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)

        return user, jwt_token, None

    @staticmethod
    def get_user (userId: str, firstname: str, lastname: str, email: str, page: int, limit: int) -> Tuple[Optional[User], Optional[str]]:
        """Business logic for retrieving a user by various criteria."""
        
        if (userId):
            user = UserRepository.get_user_by_id(userId, page, limit)
            if not user:
                return None, "User not found."
            return user, None
        elif(firstname or lastname):
            user = UserRepository.get_user_by_name(firstname, lastname, page, limit)
            if not user:
                return None, "User not found."
        elif(email):
            user = UserRepository.get_user_by_email(email, page, limit)
            if not user:
                return None, "User not found."
        else:
            user = UserRepository.get_all_users(page, limit)
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