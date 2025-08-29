from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from typing import Tuple
from ..api import UserRegistrationSerializer, UserProfileSerializer
from ..services import UserService

class UserController:
    """
    Handles HTTP requests for user-related operations.
    """

    @staticmethod
    @api_view(['POST'])
    def register_user(request: Request) -> Response:
        """
        API endpoint for user registration.
        POST /api/auth/register/
        """
        # Validate incoming data
        serializer = UserRegistrationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract validated data
        validated_data = serializer.validated_data
        firstname = validated_data.get('firstname')
        lastname = validated_data.get('lastname')
        email = validated_data['email']
        password = validated_data['password']

        # Call the service to handle business logic
        user, token, error = UserService.register_user(
            firstname=firstname,
            lastname=lastname,
            email=email,
            password=password,            
        )

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serialize the created user for the response
        response_serializer = UserProfileSerializer(user)       

        # Create response
        response = Response(
            {
                "message": "User registered successfully",
                "user": response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
        
        # Set JWT token as HTTP-only cookie
        response.set_cookie(
            key='access_token',
            value=token,
            httponly=True,     
            secure=False,      
            samesite='Lax',    
            max_age=24 * 60 * 60 
        )
        
        return response
