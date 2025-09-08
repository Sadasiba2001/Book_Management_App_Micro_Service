from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..services import BookCreateService
from ..serializers import BookSerializer
from rest_framework.decorators import api_view

class BookCreateView(APIView):
    
    @staticmethod
    @api_view(['POST'])
    def book_create(self, request):
        try:
            book = BookCreateService.create_book(request.data)
            serializer = BookCreateSerializer(book)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)