from ..models import Book

class BookCreateRepository:
    @staticmethod
    def create_book(data):
        return Book.objects.create(**data)
