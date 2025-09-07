from django.urls import path
from ..controllers import register_user, login_user, logout_user

urlpatterns = [
    path('register/', UserController.register_user, name='user-registration'),
    path('login/', UserController.login_user, name='user-login'),
]