from django.urls import path, re_path, include

from user.views import ProfileCreate, LoginView, UpdateProfileView, UpdatePasswordView, GetUsersView, UpdateUserView, \
    DeleteUserView

auth_urls = [
    path("users", GetUsersView.as_view(), name="get all users"),
    path('users/<int:id>', UpdateUserView.as_view(), name="update single user"),
    path('users/<int:id>/delete', DeleteUserView.as_view(), name='delete single user'),
    path("register", ProfileCreate.as_view(), name="register new account"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UpdateProfileView.as_view(), name="update user info"),
    path('password/update', UpdatePasswordView.as_view(), name="update password view")
]

urlpatterns = [
    re_path(r'^v1/', include(auth_urls)),
]

