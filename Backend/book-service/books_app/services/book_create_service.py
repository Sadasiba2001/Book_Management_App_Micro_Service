from rest_framework.exceptions import ValidationError
from ..repositories import BookCreateRepository, BookRetriveRepository

class BookCreateService:
    
    @staticmethod
    def create_book(data):
        if not data.get('title') or not data.get('author'):
            raise ValidationError("Title and author are required.")
        
        if data.get('isbn') and BookRetriveRepository.get_all_books().filter(isbn=data['isbn']).exists():
            raise ValidationError("ISBN already exists.")
        
        return BookCreateRepository.create_book(data)