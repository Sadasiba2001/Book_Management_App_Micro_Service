from rest_framework import serializers
from .models import Book

class BookCreateSerializer(serializers.ModelSerializer):
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
            'created_at', 
            'updated_at'
        ]