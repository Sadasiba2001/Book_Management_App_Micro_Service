from django.apps import AppConfig


class BooksAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'books_app'

    """
        # This import is necessary to ensure the custom User model is registered
        # before any other code tries to use it.
    """
    def ready(self):
        from . import models