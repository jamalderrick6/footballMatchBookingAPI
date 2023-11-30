from django.urls import path, re_path, include

from user.views import ProfileCreate, LoginView, UpdateProfileView, UpdatePasswordView

auth_urls = [
    path("register", ProfileCreate.as_view(), name="register new account"),
    path("login", LoginView.as_view(), name="login"),
    path("me", UpdateProfileView.as_view(), name="update user info"),
    path('password/update', UpdatePasswordView.as_view(), name="update password view")
]

urlpatterns = [
    re_path(r'^v1/', include(auth_urls)),
]

