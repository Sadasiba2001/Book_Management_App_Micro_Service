import jwt
import time
from copy import deepcopy
from http import HTTPStatus
from django.conf import settings
from rest_framework import status
from ..services import UserService
from ..utils import CustomPagination
from rest_framework.request import Request
from ..utils import JWTUtils, ResponseUtils
from rest_framework.response import Response
from auth_app.utils.jwt_utils import JWTUtils
from rest_framework.decorators import api_view
from auth_app.middleware import jwt_auth_required
from django.views.decorators.csrf import csrf_exempt
from ..constants.response_template import SUCCESS_RESPONSE, ERROR_RESPONSE
from ..api import UserRegistrationSerializer, UserProfileSerializer, UserLoginSerializer



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
        try:
            # Validate incoming data
            serializer = UserRegistrationSerializer(data=request.data)
            if not serializer.is_valid():
                return ResponseUtils.error(
                    message="Invalid data",
                    error=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            # Extract validated data
            validated_data = serializer.validated_data
            firstname = validated_data.get('firstname')
            lastname = validated_data.get('lastname')
            email = validated_data['email']
            password = validated_data['password']
            
            # Call the service to handle business logic
            user, token = UserService.register_user(
                firstname=firstname,
                lastname=lastname,
                email=email,
                password=password,
                is_superuser=request.data.get('is_superuser', False),
                is_staff=request.data.get('is_staff', False),
                is_active=request.data.get('is_active', True)
            )

            print("*********** User and token received from service:", user, token)

            if not user or not token:
                return ResponseUtils.error(
                    message="Registration failed",
                    error="User creation or token generation failed.",
                    http_status=status.HTTP_400_BAD_REQUEST
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
            
            return ResponseUtils.success(
                message="User registered successfully",
                data=response_serializer.data,
                http_status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Catch any unexpected errors and return as JSON
            return ResponseUtils.error(
                message="Something went wrong",
                error=str(e),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @staticmethod
    @api_view(['GET'])
    def user_validate(request: Request) -> Response:
        """
        API endpoint to validate if the user is authenticated.
        GET /api/auth/validate/
        Requires a valid JWT token in cookies.
        """
        try:
            # Try to get the token from cookies
            token = request.COOKIES.get('access_token')

            if not token:
                return ResponseUtils.error(
                    message="Access token not found in cookies.",
                    error="No token provided",
                    http_status=status.HTTP_401_UNAUTHORIZED
                )

            # Decode and validate the token
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY, 
                settings.JWT_ALGORITHM      
            )
            if not payload:
                return ResponseUtils.error(
                    message="Invalid or expired token.",
                    error="Token validation failed",
                    http_status=status.HTTP_401_UNAUTHORIZED
                )

            return ResponseUtils.success(
                message="User is authenticated.",
                data={
                    "user_id": payload.get("user_id"),
                    "email": payload.get("email")
                },
                http_status=status.HTTP_200_OK
            )

        except Exception as e:
            return ResponseUtils.error(
                message="Something went wrong",
                error=str(e),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    @api_view(['POST'])
    def login_user(request: Request) -> Response:
        """
        API endpoint for user login.
        POST /api/auth/login/
        """
        start = time.time()
        try:
            print("CONTROLLER: Step 1 time:", time.time() - start)

            # Validate incoming data
            serializer = UserLoginSerializer(data=request.data)
            if not serializer.is_valid():
                return ResponseUtils.error(
                    message="Data validation failed",
                    error=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            print("CONTROLLER: Step 2 time:", time.time() - start)
            # Extract validated data
            validated_data = serializer.validated_data
            email = validated_data['email']
            password = validated_data['password']

            print("CONTROLLER: Step 3 time:", time.time() - start)  
            # Call the service to handle business logic
            user, token = UserService.login_user(
                email=email,
                password=password
            )
            if not user or not token:
                return ResponseUtils.error(
                    message="Login failed",
                    error="Invalid email or password.",
                    http_status=status.HTTP_401_UNAUTHORIZED
                )

            print("CONTROLLER: Step 4 time:", time.time() - start)
            # Serialize the user for the response
            response_serializer = UserProfileSerializer(user)
            if not response_serializer:
                return ResponseUtils.error(
                    message="Serialization failed",
                    error="Could not serialize user data.",
                    http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            print("CONTROLLER: Step 5 time:", time.time() - start)
            # Create response
            response = Response(
                {
                    "message": "User logged in successfully",
                    "user": response_serializer.data
                },
                status=status.HTTP_200_OK
            )

            print("CONTROLLER: Step 6 time:", time.time() - start)
            # Set JWT token as HTTP-only cookie
            response.set_cookie(
                key='access_token',
                value=token,
                httponly=True,
                secure=False,
                samesite='Lax',
                max_age=24 * 60 * 60
            )

            print("CONTROLLER: Total time:", time.time() - start)
            return ResponseUtils.success(
                message="User logged in successfully",
                data=response_serializer.data,
                http_status=status.HTTP_200_OK
            )
        
        except Exception as e:
            # Catch any unexpected errors and return as JSON
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @api_view(['POST'])
    def logout_user(request: Request) -> Response:
        """
        API endpoint to log out a user by clearing the JWT cookie.
        POST /api/auth/logout/
        """
        try:
            response = UserService.logout_user()

            return ResponseUtils.success(
                message="User logged out successfully",
                error="User logged out successfully",
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            return ResponseUtils.error(
                message="Logout failed",
                error=str(e),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


    @staticmethod
    @api_view(['GET'])
    @jwt_auth_required
    def get_user(request: Request) -> Response:
        """
        API endpoint for retrieving a user by various criteria.
        GET /api/auth/user/?userId=<id>&name=<name>&email=<email>
        Requires a valid JWT token in cookies or Authorization header.
        """
        try:
            # Get query parameters
            user_id = request.query_params.get("userId")
            firstname = request.query_params.get("firstname")
            lastname = request.query_params.get("lastname")
            email = request.query_params.get("email")
            page = int(request.query_params.get("page", 1))
            limit = int(request.query_params.get("limit", 5))
            

            # Call UserService to fetch user
            user, error = UserService.get_user(
                userId=user_id, 
                firstname=firstname, 
                lastname=lastname, 
                email=email, 
                page=page, 
                limit=limit
                )

            if error:
                return Response(
                    {"error": error},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serialize the user for the response
            response_serializer = UserProfileSerializer(user, many=True)
            return Response(
                {
                    "message": "User retrieved successfully",
                    "user": response_serializer.data
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            # Catch any unexpected errors and return as JSON
            return Response(
                {"error": "Something went wrong", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @staticmethod
    @api_view(['DELETE'])
    @csrf_exempt
    @jwt_auth_required
    def delete_user(request: Request) -> Response:
        """
        Delete a user by ID or Email.
        Accepts: DELETE /api/auth/delete/?id=1 or /?email=abc@example.com
        """
        try:
            user_id = request.query_params.get('id')
            email = request.query_params.get('email')

            if not user_id and not email:
                return Response(
                    {"error": "User ID or Email must be provided."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            deleted = UserService.delete_user(user_id=user_id, email=email)

            if deleted:
                return Response(
                    {"message": "User deleted successfully."},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "User not found."},
                    status=status.HTTP_404_NOT_FOUND
                )

        except Exception as e:
            return Response(
                {"error": "An error occurred.", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )