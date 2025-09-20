from django.urls import path
from .forms import StyledAuthenticationForm
from .views import (
    RoleAwareLoginView,
    dashboard,
    create_user,
    block_user,
    unblock_user,
    delete_user,
    assign_group,
    signup,
    home,
    logout_view,
)
from .views import profile_edit, profile_detail
app_name = "accounts"

urlpatterns = [
    # Admin panel
    path("", dashboard, name="dashboard"),
    path("users/create/", create_user, name="create_user"),
    path("users/<int:user_id>/block/", block_user, name="block_user"),
    path("users/<int:user_id>/unblock/", unblock_user, name="unblock_user"),
    path("users/<int:user_id>/delete/", delete_user, name="delete_user"),
    path("users/<int:user_id>/assign-group/", assign_group, name="assign_group"),
    path("profile/", profile_detail, name="profile"),
    path("profile/edit/", profile_edit, name="profile_edit"),
    # Auth
    path(
        "login/",
        RoleAwareLoginView.as_view(
            template_name="accounts/login.html",
            authentication_form=StyledAuthenticationForm,
        ),
        name="login",
    ),
    # Use our logout_view which accepts GET and POST (safer for simple UIs)
    path("logout/", logout_view, name="logout"),

    # Public
    path("signup/", signup, name="signup"),
    path("home/", home, name="home"),  # user landing used by RoleAwareLoginView
]
