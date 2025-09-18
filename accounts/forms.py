# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

User = get_user_model()

class AdminUserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput())
    is_staff = forms.BooleanField(required=False, initial=False, help_text="Allow access to this admin panel", widget=forms.CheckboxInput())

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "is_staff")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common = "w-full rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        self.fields["username"].widget.attrs.update({"class": common, "placeholder": "john_doe"})
        self.fields["email"].widget.attrs.update({"class": common, "placeholder": "john@example.com"})
        self.fields["password1"].widget.attrs.update({"class": common + " pr-10"})
        self.fields["password2"].widget.attrs.update({"class": common + " pr-10"})
        self.fields["is_staff"].widget.attrs.update({"class": "h-4 w-4 rounded"})

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.is_staff = self.cleaned_data.get("is_staff", False)
        if commit:
            user.save()
        return user


# --- Public Sign Up form (no is_staff) ---
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


# --- Styled AuthenticationForm for LoginView ---
class StyledAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common = "w-full rounded-xl border border-gray-300 px-4 py-2 focus:outline-none focus:ring-2 focus:ring-emerald-500"
        self.fields["username"].widget.attrs.update({"class": common, "placeholder": "username"})
        self.fields["password"].widget.attrs.update({"class": common + " pr-10", "placeholder": "password"})
