from django.urls import path
from ..controllers import UserController

urlpatterns = [
    path('register/', UserController.register_user, name='user-registration'),
    path('login/', UserController.login_user, name='user-login'),
    path('user/', UserController.get_user, name='get-user'),
]