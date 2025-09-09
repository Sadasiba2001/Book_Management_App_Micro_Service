from django.urls import path
from ..controllers import BookCreateView, CloudinaryUploadView

urlpatterns = [
    path('create/', BookCreateView.as_view(), name='book-create'),
    path('image-upload/', CloudinaryUploadView.as_view(), name='cloudinary-upload'),
]