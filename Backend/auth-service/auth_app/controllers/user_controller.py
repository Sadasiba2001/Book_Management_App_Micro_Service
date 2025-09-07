from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view
from typing import Tuple
from ..api import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from ..services import UserService
from ..utils import JWTUtils

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

@api_view(['POST'])
def logout_user(request: Request) -> Response:
    """
    API endpoint for user logout.
    POST /api/auth/logout/
    """
    try:
        # Get token from cookies
        token = JWTUtils.get_token_from_request(request)
        
        if not token:
            return Response(
                {"error": "No authentication token found"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Verify the token is valid
        payload = JWTUtils.verify_jwt_token(token)
        if not payload:
            return Response(
                {"error": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Call service to handle logout logic
        success, error = UserService.logout_user(token)
        
        if error:
            return Response(
                {"error": error},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create response
        response = Response(
            {"message": "User logged out successfully"},
            status=status.HTTP_200_OK
        )
        
        # Clear the JWT cookie
        response.delete_cookie(
            key='access_token',
            samesite='Lax'
        )
        
        return response
        
    except Exception as e:
        print("*********** LOGOUT ERROR:", str(e))
        return Response(
            {"error": "An unexpected error occurred during logout"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
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

    # Extract serializer validated data
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