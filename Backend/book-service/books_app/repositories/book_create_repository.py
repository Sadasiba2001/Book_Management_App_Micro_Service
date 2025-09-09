from ..models import Book

class BookCreateRepository:

    def create_book(self, data):
        return Book.objects.create(**data)
