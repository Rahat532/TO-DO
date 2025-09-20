from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group
from .models import Profile  # add this import

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "bio", "avatar", "timezone"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "w-full rounded-xl border border-gray-300 px-4 py-2"}),
            "bio": forms.Textarea(attrs={"class": "w-full rounded-xl border border-gray-300 px-4 py-2", "rows": 4}),
            "timezone": forms.TextInput(attrs={"class": "w-full rounded-xl border border-gray-300 px-4 py-2", "placeholder": "e.g. Asia/Dhaka"}),
        }

User = get_user_model()

ADMIN_GROUP_NAME = "admin"
USER_GROUP_NAME = "user"

GROUP_CHOICES = [
    (ADMIN_GROUP_NAME, "Admin"),
    (USER_GROUP_NAME, "User"),
    ("none", "None"),
]

def ensure_group(name: str) -> Group:
    group, _ = Group.objects.get_or_create(name=name)
    return group


class AdminUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    is_staff = forms.BooleanField(
        required=False,
        initial=False,
        help_text="Allow access to this admin panel",
        widget=forms.CheckboxInput(),
    )
    group = forms.ChoiceField(
        choices=GROUP_CHOICES,
        required=False,
        initial=USER_GROUP_NAME,
        help_text="Default group for the new user",
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_staff", "group")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common = "w-full rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        self.fields["username"].widget.attrs.update({"class": common, "placeholder": "john_doe"})
        self.fields["email"].widget.attrs.update({"class": common, "placeholder": "john@example.com"})
        self.fields["password1"].widget.attrs.update({"class": common + " pr-10"})
        self.fields["password2"].widget.attrs.update({"class": common + " pr-10"})
        self.fields["is_staff"].widget.attrs.update({"class": "h-4 w-4 rounded"})
        self.fields["group"].widget.attrs.update({"class": common})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        # is_staff is a convenience flag for admin UX (not equal to superuser)
        user.is_staff = self.cleaned_data.get("is_staff", False)

        if commit:
            user.save()

        # Assign to the chosen group (clear both first)
        selected = self.cleaned_data.get("group")
        ensure_group(ADMIN_GROUP_NAME).user_set.remove(user)
        ensure_group(USER_GROUP_NAME).user_set.remove(user)

        if selected == ADMIN_GROUP_NAME:
            ensure_group(ADMIN_GROUP_NAME).user_set.add(user)
            if not user.is_staff:
                user.is_staff = True
                user.save(update_fields=["is_staff"])
        elif selected == USER_GROUP_NAME:
            ensure_group(USER_GROUP_NAME).user_set.add(user)

        return user

class PublicSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common = "w-full rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        self.fields["username"].widget.attrs.update({"class": common, "placeholder": "john_doe"})
        self.fields["email"].widget.attrs.update({"class": common, "placeholder": "john@example.com"})
        self.fields["password1"].widget.attrs.update({"class": common + " pr-10"})
        self.fields["password2"].widget.attrs.update({"class": common + " pr-10"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email


class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common = "w-full rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        self.fields["username"].widget.attrs.update({"class": common, "placeholder": "username"})
        self.fields["password"].widget.attrs.update({"class": common + " pr-10", "placeholder": "password"})


class AssignGroupForm(forms.Form):
    group = forms.ChoiceField(choices=GROUP_CHOICES, required=True)

    def apply(self, target_user: User):
        selected = self.cleaned_data["group"]
        ensure_group(ADMIN_GROUP_NAME).user_set.remove(target_user)
        ensure_group(USER_GROUP_NAME).user_set.remove(target_user)

        if selected == ADMIN_GROUP_NAME:
            ensure_group(ADMIN_GROUP_NAME).user_set.add(target_user)
            target_user.is_staff = True  # convenience: admins get staff UX
        elif selected == USER_GROUP_NAME:
            ensure_group(USER_GROUP_NAME).user_set.add(target_user)
            # don't force staff here

        target_user.save(update_fields=["is_staff"])
