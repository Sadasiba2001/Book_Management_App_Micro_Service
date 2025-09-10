from django.urls import path
from ..controllers import BookController, CloudinaryUploadView

urlpatterns = [
    path('create/', BookController.as_view(), name='book-create'),
    path('image-upload/', CloudinaryUploadView.as_view(), name='cloudinary-upload'),
]