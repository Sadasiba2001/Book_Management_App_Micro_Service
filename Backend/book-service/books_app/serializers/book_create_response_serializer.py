from rest_framework import serializers
from ..models import Book

class BookCreateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id', 
            'title', 
            'author', 
            'isbn', 
            'publication_date', 
            'genre', 
            'description', 
            'images',
            'created_at', 
            'updated_at'
        ]
        read_only_fields = fields