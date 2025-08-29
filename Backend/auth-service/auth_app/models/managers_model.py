from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    """
    # Custom manager for the User model without a username field.
    """

    def create_user(self, firstname, lastname, email, password=None, **extra_fields):
        """
        # Creates and saves a User with the given name, email and password.
        """
        if not firstname:
            raise ValueError('The Firstname field must be set')
        if not lastname:
            raise ValueError('The Lastname field must be set')
        if not email:
            raise ValueError('The Email field must be set')

        email = self.normalize_email(email)

        user = self.model(email=email, firstname=firstname, lastname=lastname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, firstname, lastname, email, password=None, **extra_fields):
        """
        # Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)