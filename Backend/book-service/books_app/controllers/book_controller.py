from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request
from ..services import BookCreateService
from ..serializers import BookCreateSerializer, BookCreateResponseSerializer
from ..utils import ResponseUtils

class BookController(APIView):
    def __init__(self, book_create_service: BookCreateService = None, **kwargs):
        super().__init__(**kwargs)
        self.book_create_service = book_create_service or BookCreateService()  

    def post(self, request: Request) -> Response:
        try:
            
            serializer = BookCreateSerializer(data=request.data)
            
            if not serializer.is_valid():                
                return ResponseUtils.error(
                    message="Invalid data",
                    error=serializer.errors,
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            # Extract validated data            
            validated_data = serializer.validated_data

            # Call the service to create the book       
            book = self.book_create_service.create_book(**validated_data)
            
            if not book:
                return ResponseUtils.error(
                    message="Invalid data",
                    error="Book could not be created",
                    http_status=status.HTTP_400_BAD_REQUEST
                )

            # Serialize the response
            response_serializer = BookCreateResponseSerializer(book)
            return ResponseUtils.success(
                message="Book stored successfully",
                data=response_serializer.data,
                http_status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return ResponseUtils.error(
                message="Error while storing the book",
                error=str(e),
                http_status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )