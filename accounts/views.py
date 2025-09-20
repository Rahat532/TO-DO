from django.contrib import messages
from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .forms import ProfileForm 
from .forms import (
    AdminUserCreateForm,
    PublicSignUpForm,
    StyledAuthenticationForm,
    AssignGroupForm,
)

User = get_user_model()

ADMIN_GROUP_NAME = "admin"
USER_GROUP_NAME = "user"


# ---------- Group helpers ----------
def ensure_group(name: str) -> Group:
    group, _ = Group.objects.get_or_create(name=name)
    return group

def _in_group(user, group_name: str) -> bool:
    return user.is_authenticated and user.groups.filter(name=group_name).exists()

def _admin_count_excluding(user_to_exclude=None) -> int:
    qs = User.objects.filter(is_active=True).distinct()
    qs = qs.filter(Q(is_superuser=True) | Q(groups__name=ADMIN_GROUP_NAME))
    if user_to_exclude is not None:
        qs = qs.exclude(pk=user_to_exclude.pk)
    return qs.count()

def admin_required(view_func):
    """
    Allow superusers or members of the 'admin' group to access.
    """
    check = lambda u: u.is_superuser or _in_group(u, ADMIN_GROUP_NAME)
    return user_passes_test(check, login_url=reverse_lazy("accounts:login"))(view_func)


# ---------- Role-aware Login ----------
class RoleAwareLoginView(LoginView):
    """
    Redirect after login based on role/group:
      - superuser or in 'admin' group -> accounts:dashboard
      - others -> accounts:home
    Respects safe ?next=... param.
    """
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        request = self.request
        user = request.user

        # 1) Honor safe next
        next_url = request.POST.get("next") or request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return next_url

        # 2) Group-based default
        if user.is_superuser or _in_group(user, ADMIN_GROUP_NAME):
            return reverse_lazy("accounts:dashboard")
        return reverse_lazy("accounts:home")

    def form_valid(self, form):
        """Called when the form is valid. Add a welcome-back flash message."""
        user = form.get_user()
        try:
            # friendly welcome message after successful login
            messages.success(self.request, f"Welcome back, {user.username}!")
        except Exception:
            # don't break login if messages subsystem has issues
            pass
        return super().form_valid(form)


# ---------- Public pages ----------
@login_required
@require_http_methods(["GET"])
def home(request):
    """Redirect the logged-in user to their task list.

    This avoids rendering a missing `accounts/home.html` template and
    ensures users (including admins) land on a useful page.
    """
    return redirect("tasks:task_list")


@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already signed in.")
        return redirect("accounts:home")

    if request.method == "POST":
        form = PublicSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Add to user group
            ensure_group(USER_GROUP_NAME).user_set.add(user)
            # Auto-login
            auth_login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("accounts:home")
    else:
        form = PublicSignUpForm()

    return render(request, "accounts/signup.html", {"form": form})


# ---------- Admin dashboard & actions ----------
@admin_required
@require_http_methods(["GET"])
def dashboard(request):
    q = (request.GET.get("q") or "").strip()
    page = request.GET.get("page") or 1
    per_page = request.GET.get("per_page") or 10
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    if per_page not in (10, 25, 50, 100):
        per_page = 10

    users_qs = User.objects.all().order_by("-date_joined").prefetch_related("groups")
    if q:
        users_qs = users_qs.filter(Q(username__icontains=q) | Q(email__icontains=q))

    paginator = Paginator(users_qs, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    # compute memberships for just the current page (efficient)
    page_user_ids = [u.id for u in page_obj.object_list]
    admin_group_ids = list(
        User.objects.filter(id__in=page_user_ids, groups__name=ADMIN_GROUP_NAME)
        .values_list("id", flat=True)
    )
    user_group_ids = list(
        User.objects.filter(id__in=page_user_ids, groups__name=USER_GROUP_NAME)
        .values_list("id", flat=True)
    )

    context = {
        "total_users": User.objects.count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "blocked_users": User.objects.filter(is_active=False).count(),
        "staff_users": User.objects.filter(is_staff=True).count(),

        "users": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,

        "q": q,
        "per_page": per_page,

        # NEW: lists you can use with "in" in the template
        "admin_group_ids": admin_group_ids,
        "user_group_ids": user_group_ids,
    }
    return render(request, "accounts/dashboard.html", context)

    q = (request.GET.get("q") or "").strip()
    page = request.GET.get("page") or 1
    per_page = request.GET.get("per_page") or 10
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    if per_page not in (10, 25, 50, 100):
        per_page = 10

    users_qs = User.objects.all().order_by("-date_joined")
    if q:
        users_qs = users_qs.filter(Q(username__icontains=q) | Q(email__icontains=q))

    paginator = Paginator(users_qs, per_page)
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        "total_users": User.objects.count(),
        "active_users": User.objects.filter(is_active=True).count(),
        "blocked_users": User.objects.filter(is_active=False).count(),
        "staff_users": User.objects.filter(is_staff=True).count(),

        # table data
        "users": page_obj.object_list,
        "page_obj": page_obj,
        "paginator": paginator,

        # search + paging state
        "q": q,
        "per_page": per_page,
    }
    return render(request, "accounts/dashboard.html", context)
@admin_required
@require_http_methods(["GET", "POST"])
def create_user(request):
    if request.method == "POST":
        form = AdminUserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User created successfully.")
            return redirect("accounts:dashboard")
    else:
        form = AdminUserCreateForm()
    return render(request, "accounts/create_user.html", {"form": form})


@admin_required
@require_POST
def assign_group(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    form = AssignGroupForm(request.POST)
    if not form.is_valid():
        messages.error(request, "Invalid group submission.")
        return redirect("accounts:dashboard")

    selected = form.cleaned_data["group"]

    # Prevent demoting yourself if you'd be the last admin
    if target == request.user and selected != ADMIN_GROUP_NAME:
        if _admin_count_excluding(user_to_exclude=request.user) == 0:
            messages.error(request, "You are the last admin. Create another admin before demoting yourself.")
            return redirect("accounts:dashboard")

    # Only superusers can modify superusers
    if target.is_superuser and not request.user.is_superuser:
        messages.error(request, "Only superusers can modify superuser accounts.")
        return redirect("accounts:dashboard")

    form.apply(target)
    messages.success(request, f"Updated {target.username}'s group to: {selected}.")
    return redirect("accounts:dashboard")


@admin_required
@require_POST
def block_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, "You cannot block your own account.")
        return redirect("accounts:dashboard")
    if target.is_superuser:
        messages.error(request, "Refusing to block a superuser.")
        return redirect("accounts:dashboard")
    if not target.is_active:
        messages.info(request, "User is already blocked.")
        return redirect("accounts:dashboard")

    target.is_active = False
    target.save(update_fields=["is_active"])
    messages.success(request, f"Blocked {target.username}.")
    return redirect("accounts:dashboard")


@admin_required
@require_POST
def unblock_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, "You cannot modify your own status here.")
        return redirect("accounts:dashboard")
    if target.is_superuser:
        messages.error(request, "Refusing to modify a superuser here.")
        return redirect("accounts:dashboard")
    if target.is_active:
        messages.info(request, "User is already active.")
        return redirect("accounts:dashboard")

    target.is_active = True
    target.save(update_fields=["is_active"])
    messages.success(request, f"Unblocked {target.username}.")
    return redirect("accounts:dashboard")


@admin_required
@require_POST
def delete_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    if target == request.user:
        messages.error(request, "You cannot delete your own account.")
        return redirect("accounts:dashboard")
    if target.is_superuser:
        messages.error(request, "Refusing to delete a superuser.")
        return redirect("accounts:dashboard")

    username = target.username
    target.delete()
    messages.success(request, f"Deleted {username}.")
    return redirect("accounts:dashboard")
@login_required
@require_http_methods(["GET", "POST"])
def profile_edit(request):
    profile = getattr(request.user, "profile", None)
    if profile is None:
        from .models import Profile
        profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("accounts:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile_form.html", {"form": form})

@login_required
@require_http_methods(["GET"])
def profile_detail(request):
    return render(request, "accounts/profile_detail.html", {"profile": request.user.profile})


@require_http_methods(["GET", "POST"])
def logout_view(request):
    """Logout the current user (accepts GET and POST) and redirect to login."""
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")