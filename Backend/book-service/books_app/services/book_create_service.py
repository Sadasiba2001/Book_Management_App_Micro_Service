from rest_framework.exceptions import ValidationError
from ..repositories import BookCreateRepository, BookRetrieveRepository
from django.db import IntegrityError, DatabaseError
import logging

logger = logging.getLogger(__name__)

class BookCreateService:
    def __init__(self, create_repo: BookCreateRepository = None, retrieve_repo: BookRetrieveRepository = None):
        self.create_repo = create_repo or BookCreateRepository()
        self.retrieve_repo = retrieve_repo or BookRetrieveRepository()

    def create_book(self, title: str, author: str, isbn: str, publication_date: str, genre: str, description: str):
        try:
            data = {
                'title': title,
                'author': author,
                'isbn': isbn,
                'publication_date': publication_date,
                'genre': genre,
                'description': description
            }

            # Check for duplicate ISBN (domain logic)
            if self.retrieve_repo.get_all_books().filter(isbn=data['isbn']).exists():
                raise ValidationError({"isbn": "A book with this ISBN already exists."})

            # Create book through repository
            book = self.create_repo.create_book(data)

            logger.info(f"Book created successfully: {book.id} - {book.title}")
            return book

        except ValidationError as ve:
            logger.warning(f"Validation error during book creation: {ve.detail}")
            raise

        except IntegrityError as ie:
            logger.error(f"Database integrity error during book creation: {str(ie)}")
            raise ValidationError({"error": "Database integrity error. Please check the provided data."})

        except DatabaseError as de:
            logger.error(f"Database error during book creation: {str(de)}")
            raise ValidationError({"error": "Database error occurred. Please try again."})

        except Exception as e:
            logger.error(f"Unexpected error during book creation: {str(e)}", exc_info=True)
            raise ValidationError({"error": "An unexpected error occurred while creating the book."})