# accounts/views.py
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import login as auth_login
from django.contrib.auth import get_user_model
from .forms import AdminUserCreateForm,PublicSignUpForm


User = get_user_model()


@staff_member_required
@require_http_methods(["GET"])
def dashboard(request):
     q = request.GET.get("q", "").strip()
     users = User.objects.all().order_by("-date_joined")
     if q:
       users = users.filter(username__icontains=q) | users.filter(email__icontains=q)


     context = {
    "total_users": User.objects.count(),
    "active_users": User.objects.filter(is_active=True).count(),
    "blocked_users": User.objects.filter(is_active=False).count(),
    "staff_users": User.objects.filter(is_staff=True).count(),
    "users": users,
    "q": q,
     }
     return render(request, "accounts/dashboard.html", context)


@staff_member_required
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


@staff_member_required
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


@staff_member_required
@require_POST
def unblock_user(request, user_id):
    target = get_object_or_404(User, pk=user_id)
    target.is_active = True
    target.save(update_fields=["is_active"])
    messages.success(request, f"Unblocked {target.username}.")
    return redirect("accounts:dashboard")


@staff_member_required
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

@staff_member_required
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

    # IMPORTANT: always return a response for GET or invalid POST
    return render(request, "accounts/create_user.html", {"form": form})

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.user.is_authenticated:
        messages.info(request, "You are already signed in.")
        return redirect("/")
    if request.method == "POST":
        form = PublicSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Auto-login after signup
            auth_login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("/")
    else:
        form = PublicSignUpForm()
    return render(request, "accounts/signup.html", {"form": form})
