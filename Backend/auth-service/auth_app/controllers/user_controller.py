from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from typing import Tuple
from ..api import UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer
from ..services import UserService

"""
Handles HTTP requests for user-related operations.
"""
class UserController:

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
            is_superuser=request.data.get('is_superuser', False),
            is_staff=request.data.get('is_staff', False),
            is_active=request.data.get('is_active', True)
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
    
    @staticmethod
    @api_view(['POST'])
    def login_user(request: Request) -> Response:
        """
        API endpoint for user login.
        POST /api/auth/login/
        """
        # Validate incoming data
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "Invalid data", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract validated data
        validated_data = serializer.validated_data
        email = validated_data['email']
        password = validated_data['password']

        # Call the service to handle business logic
        user, token, error = UserService.login_user(
            email=email,
            password=password
        )

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Serialize the user for the response
        response_serializer = UserProfileSerializer(user)

        # Create response
        response = Response(
            {
                "message": "User logged in successfully",
                "user": response_serializer.data
            },
            status=status.HTTP_200_OK
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

    @staticmethod
    @api_view(['GET'])
    def get_user(request: Request) -> Response:
        """
        API endpoint for retrieving a user by various criteria.
        GET /api/auth/user/
        """
        userId = request.query_params.get("userId")
        name = request.query_params.get("name")
        email = request.query_params.get("email")

        user, error = UserService.get_user(userId=userId, name=name, email=email)

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the user for the response
        serializer = UserLoginSerializer(data=request.data)
        user, error = UserService.get_user(userId=userId, name=name, email=email)

        if error:
            return Response(
                {"error": error},
                status=status.HTTP_404_NOT_FOUND
            )

        # Serialize the user for the response
        response_serializer = UserProfileSerializer(user)

        return Response(
            {
                "message": "User retrieved successfully",
                "user": response_serializer.data
            },
            status=status.HTTP_200_OK
        )