from rest_framework import serializers
from ..models import Book
from django.utils.html import strip_tags
from .cloudinary_image_upload_serializer import CloudinaryUploadSerializer
import re

class BookCreateSerializer(serializers.ModelSerializer):
    images = CloudinaryUploadSerializer(many=True, required=False)

    def sanitize_string(self, value):
        """Sanitize string by removing HTML tags, extra spaces, and trimming"""
        if value is None:
            return value
        
        # Remove HTML tags
        sanitized = strip_tags(str(value))
        # Remove extra whitespace
        sanitized = re.sub(r'\s+', ' ', sanitized)
        # Trim leading/trailing spaces
        sanitized = sanitized.strip()
        
        return sanitized
    
    def validate_title(self, value):
        """Sanitize and validate title"""
        sanitized = self.sanitize_string(value)
        if len(sanitized) < 2:
            raise serializers.ValidationError("Title must be at least 2 characters long.")
        return sanitized
    
    def validate_author(self, value):
        """Sanitize and validate author"""
        sanitized = self.sanitize_string(value)
        if len(sanitized) < 2:
            raise serializers.ValidationError("Author name must be at least 2 characters long.")
        # Check if author contains only letters, spaces, and common punctuation
        if not re.match(r'^[a-zA-Z\s\.\-]+$', sanitized):
            raise serializers.ValidationError("Author name contains invalid characters.")
        return sanitized
    
    def validate_isbn(self, value):
        """Validate and sanitize ISBN"""
        if value:
            sanitized = self.sanitize_string(value)
            # Remove any non-alphanumeric characters except hyphens
            sanitized = re.sub(r'[^a-zA-Z0-9\-]', '', sanitized)
            # Basic ISBN format validation (10 or 13 digits)
            if not re.match(r'^(?:\d{10}|\d{13})$', sanitized.replace('-', '')):
                raise serializers.ValidationError("ISBN must be 10 or 13 digits.")
            return sanitized
        return value
    
    def validate_genre(self, value):
        """Sanitize genre"""
        sanitized = self.sanitize_string(value)
        if len(sanitized) < 2:
            raise serializers.ValidationError("Genre must be at least 2 characters long.")
        return sanitized
    
    def validate_description(self, value):
        """Sanitize description"""
        if value:
            sanitized = self.sanitize_string(value)
            return sanitized
        return value
    
    def validate_publication_date(self, value):
        """Ensure publication date is not in the future"""
        from datetime import date
        if value and value > date.today():
            raise serializers.ValidationError("Publication date cannot be in the future.")
        return value
    
    def validate_images(self, value):
        """Ensure no more than 5 images are uploaded"""
        if len(value) > 5:
            raise serializers.ValidationError("Cannot upload more than 5 images.")
        return value
    
    def to_internal_value(self, data):
        validated_data = super().to_internal_value(data)
        string_fields = ['title', 'author', 'isbn', 'genre', 'description']
        for field in string_fields:
            if field in validated_data and validated_data[field] is not None:
                validated_data[field] = self.sanitize_string(validated_data[field])
        # Ensure images are included in validated data
        if 'images' in data:
            validated_data['images'] = data.getlist('images')  # Handle multiple file uploads
        return validated_data

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
        read_only_fields = ['id', 'created_at', 'updated_at']