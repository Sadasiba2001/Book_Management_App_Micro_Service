from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers_model import UserManager  

"""
# Custom user model where email is the unique identifier.
# We are not using Django's default fields like username, first_name, last_name.
"""

class User(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=225)
    lastname = models.CharField(max_length=225)
    email = models.EmailField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    """
    # Tells Django to use the 'email' field for authentication instead of 'username'
    # REQUIRED_FIELDS = [] # Email and password are required by default.
    """    

    USERNAME_FIELD = 'email'
    
    # Assigns the custom manager to this model
    objects = UserManager()

    def __str__(self):
        return self.email