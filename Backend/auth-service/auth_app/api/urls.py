from django.urls import path
from ..controllers import register_user, login_user, logout_user

urlpatterns = [
    path('register/', register_user, name='user-registration'),
    path('login/', login_user, name='user-login'),
    path('logout/', logout_user, name='user-logout'),
]