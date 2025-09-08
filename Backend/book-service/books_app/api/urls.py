from django.urls import path
from ..controllers import BookCreateView

urlpatterns = [
    path('create/', BookCreateView.book_create, name='book-create'),
]