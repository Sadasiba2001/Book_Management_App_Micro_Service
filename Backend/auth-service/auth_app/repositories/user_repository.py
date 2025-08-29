from django.db import transaction
from typing import Optional
from ..models import User

class UserRepository:
    """
    Repository class for handling all database operations for the User model.
    This abstracts the data layer from the rest of the application.
    """

    
    @staticmethod
    def get_all_users() -> Optional[list[User]]:
        """
        Retrieve all users.
        """
        try:
            return list(User.objects.all())
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_name(name: str) -> Optional[User]:
        """
        Retrieve a user by their name.
        """
        try:
            return User.objects.filter(name__icontains=name).first()
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
        """
        Retrieve a user by their primary key (id).
        """
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None

    @staticmethod
    def get_user_by_email(email: str) -> Optional[User]:
        """
        Retrieve a user by their unique email address.
        """
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    @staticmethod
    @transaction.atomic
    def create_user(firstname: str, lastname: str, email: str, password: str, **extra_fields) -> User:
        """
        Create and save a new user with the given email and password.
        Uses a transaction to ensure data integrity.
        """
        # Check if user already exists
        if UserRepository.get_user_by_email(email):
            raise ValueError("A user with this email already exists.")

        # Use the custom manager's method to create the user
        user = User.objects.create_user(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,
            **extra_fields
        )

        print("*********** User created:", user)
        return user

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