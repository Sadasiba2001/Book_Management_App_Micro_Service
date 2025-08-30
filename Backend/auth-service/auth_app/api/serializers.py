from rest_framework import serializers
from ..models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializes and validates user registration requests.
    """
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = User
        fields = ('firstname', 'lastname', 'email', 'password', 'is_superuser', 'is_staff', 'is_active')
        extra_kwargs = {
            'firstname': {'required': True, 'allow_blank': False},
            'lastname': {'required': True, 'allow_blank': False},
        }

    def validate_email(self, value):
        """
        Custom validation to ensure email is unique.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

class UserLoginSerializer(serializers.Serializer):
    """
    Serializes and validates user login requests.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        fields = ('email', 'password')

class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializes user profile data for responses.
    """
    class Meta:
        model = User
        fields = ('id', 'firstname', 'lastname', 'email', 'created_at')
        read_only_fields = ('id', 'email', 'created_at') 