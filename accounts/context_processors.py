from typing import Dict
from django.contrib.auth import get_user_model

User = get_user_model()

def ensure_profile(request) -> Dict:
    """Ensure the authenticated user has a Profile and expose it as `profile` in templates.

    Usage: add 'accounts.context_processors.ensure_profile' to TEMPLATES OPTIONS.context_processors
    """
    profile = None
    user = getattr(request, 'user', None)
    if user and user.is_authenticated:
        # Import lazily to avoid startup ordering issues
        from .models import Profile
        profile, _ = Profile.objects.get_or_create(user=user)
        # Determine admin membership
        is_admin = user.is_superuser or user.groups.filter(name="admin").exists()
    else:
        is_admin = False
    return {"profile": profile, "is_admin": is_admin}
