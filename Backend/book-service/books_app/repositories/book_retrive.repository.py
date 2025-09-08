from ..models import Book

class BookRetriveRepository:

    @staticmethod
    def get_all_books():
        return Book.objects.all()