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

            print("*********** SERVICE: User created:", user)

            jwt_token = JWTUtils.generate_jwt_token(user.id, user.email)
            print("*********** SERVICE: JWT token generated:", jwt_token)

            return user, jwt_token, None
        except ValueError as e:
            return None, str(e)
        except Exception as e:
            return None, "An unexpected error occurred during registration."

    @staticmethod
    def get_user_profile(user_id: int) -> Optional[User]:
        """Business logic for retrieving a user's profile."""
        return UserRepository.get_user_by_id(user_id)

    @staticmethod
    def find_user_by_email(email: str) -> Optional[User]:
        """Business logic for finding a user by email."""
        return UserRepository.get_user_by_email(email)