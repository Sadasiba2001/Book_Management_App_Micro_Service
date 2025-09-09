from ..models import Book

class BookRetrieveRepository:
    
    def get_all_books(self):
        print("Enter into BookRetrieveRepository get_all_books method")
        return Book.objects.all()