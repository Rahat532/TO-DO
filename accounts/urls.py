# accounts/urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .forms import StyledAuthenticationForm
from . import views

app_name = "accounts"

urlpatterns = [
    # Custom admin panel
    path("", views.dashboard, name="dashboard"),
    path("users/create/", views.create_user, name="create_user"),
    path("users/<int:user_id>/block/", views.block_user, name="block_user"),
    path("users/<int:user_id>/unblock/", views.unblock_user, name="unblock_user"),
    path("users/<int:user_id>/delete/", views.delete_user, name="delete_user"),

    # Auth
    path("login/", auth_views.LoginView.as_view(
        template_name="accounts/login.html",
        authentication_form=StyledAuthenticationForm
    ), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", views.signup, name="signup"),
    
]
