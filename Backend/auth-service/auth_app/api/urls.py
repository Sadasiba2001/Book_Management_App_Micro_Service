from django.urls import path
from ..controllers import register_user, login_user

urlpatterns = [
    path('register/', register_user, name='user-registration'),
    path('login/', login_user, name='user-login'),
]