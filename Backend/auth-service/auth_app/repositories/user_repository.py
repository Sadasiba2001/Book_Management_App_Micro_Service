import time
from django.db import transaction
from typing import Optional
from ..models import User

class UserRepository:
    """
    Repository class for handling all database operations for the User model.
    This abstracts the data layer from the rest of the application.
    """

    @staticmethod
    def get_login_user_details(email: str) -> Optional[User]:
        start = time.time()
        """
        Retrieve a user by their unique email address.
        """
        print("REPOSITORY: Step 1 time:", time.time() - start)
        try:
            print("REPOSITORY: Step 2 time:", time.time() - start)
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
    
    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def get_user_by_name(firstname: str, lastname: str) -> Optional[list[User]]:
        """
        Retrieve a user by their name.
        """
        try:
            return list(User.objects.filter(firstname__icontains=firstname, lastname__icontains=lastname))
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(userId: int):
        return User.objects.filter(id=userId)

    @staticmethod
    def get_user_by_email(email: str):
        return User.objects.filter(email=email)

    @staticmethod
    @transaction.atomic
    def create_user(
        firstname: str, 
        lastname: str, 
        email: str, 
        password: str, 
        is_superuser: bool, 
        is_staff: bool, 
        is_active: bool
    ):
        """
        Create and save a new user with the given email and password.
        Uses a transaction to ensure data integrity.
        """
        try:
            print("REPOSITORY: Creating user with email:", email)

            # Check if user already exists
            if UserRepository.get_user_by_email(email):
                raise ValueError("A user with this email already exists.")

            # Use the custom manager's method to create the user
            user = User.objects.create_user(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password,
                is_superuser=is_superuser,
                is_staff=is_staff,
                is_active=is_active
            )
            print("REPOSITORY: User created with ID:", user.id)
            return user

        except Exception as e:
            print("REPOSITORY ERROR: Failed to create user —", str(e))
            raise  # Optionally re-raise the exception if you want upstream handling


    @staticmethod
    @transaction.atomic
    def update_user(user: User, **update_fields) -> User:
        """
        Update an existing user's fields.
        """
        for field, value in update_fields.items():
            setattr(user, field, value)
        user.save()
        return user

    @staticmethod
    @transaction.atomic
    def delete_user(user: User) -> None:
        """
        Permanently delete a user from the database.
        """
        user.delete()
    
    @staticmethod
    def delete_user_by_id_or_email(user_id=None, email=None) -> bool:
        """
        Delete a user by ID or Email. Returns True if deleted, False if not found.
        """
        try:
            user = None
            if user_id:
                user = User.objects.filter(id=user_id).first()
            elif email:
                user = User.objects.filter(email=email).first()

            if user:
                user.delete()
                return True

            return False

        except Exception:
            # Optional: Log the error here
            return False