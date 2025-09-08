from .user_controller import UserController

register_user = UserController.register_user
login_user = UserController.login_user
logout_user = UserController.logout_user

__all__ = ["register_user", "login_user", "logout_user"]
