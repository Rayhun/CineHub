from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from payments.models import Plan

from .models import UserProfile

User = get_user_model()


class SignUpForm(UserCreationForm):
    full_name = forms.CharField(
        max_length=150,
        label="Full Name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your full name"}),
    )
    email = forms.EmailField(
        label="Email Address",
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "Enter your email"}),
    )
    accept_terms = forms.BooleanField(label="I agree to the Terms of Service and Privacy Policy")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("full_name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop("username", None)
        password_placeholders = {
            "password1": "Create a password",
            "password2": "Confirm your password",
        }
        for field_name, field in self.fields.items():
            if field.widget.attrs.get("class"):
                continue
            field.widget.attrs["class"] = "form-control"
            if field_name in password_placeholders:
                field.widget.attrs["placeholder"] = password_placeholders[field_name]
        self.fields["accept_terms"].widget.attrs["class"] = "form-check-input"

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get("full_name", "")
        parts = full_name.strip().split()
        if parts:
            user.first_name = parts[0]
            if len(parts) > 1:
                user.last_name = " ".join(parts[1:])
        user.email = self.cleaned_data["email"]
        user.username = user.email
        if commit:
            user.save()
        return user


class StyledAuthenticationForm(AuthenticationForm):
    """Wrapper around AuthenticationForm to inject bootstrap classes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing_classes = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing_classes} form-control".strip()
            if not field.widget.attrs.get("placeholder"):
                field.widget.attrs["placeholder"] = field.label
        if "username" in self.fields:
            self.fields["username"].label = "Email or Username"


class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "First name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Last name"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "Email address"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        qs = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("Another user with this email already exists.")
        return email


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = (
            "phone_number",
            "bio",
            "avatar",
            "current_plan",
            "email_notifications",
            "sms_notifications",
            "promo_notifications",
        )
        widgets = {
            "phone_number": forms.TextInput(attrs={"class": "form-control", "placeholder": "Phone number"}),
            "bio": forms.Textarea(
                attrs={"class": "form-control", "rows": 3, "placeholder": "Tell us about yourself"}
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "current_plan": forms.Select(attrs={"class": "form-select"}),
            "email_notifications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "sms_notifications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "promo_notifications": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["current_plan"].queryset = Plan.objects.filter(is_active=True)
        self.fields["current_plan"].required = False
        self.fields["current_plan"].empty_label = "Select a plan"


class PasswordUpdateForm(PasswordChangeForm):
    """Password form styled with bootstrap classes."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
            field.widget.attrs.setdefault("placeholder", field.label)


class PlanSelectionForm(forms.Form):
    plan = forms.ModelChoiceField(
        queryset=Plan.objects.none(),
        empty_label="Select a plan",
        widget=forms.Select(attrs={"class": "form-select"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["plan"].queryset = Plan.objects.filter(is_active=True)


class AccountDeleteForm(forms.Form):
    confirmation = forms.CharField(
        label="Type DELETE to confirm",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Type DELETE"}),
    )

    def clean_confirmation(self):
        value = self.cleaned_data["confirmation"].strip().lower()
        if value != "delete":
            raise forms.ValidationError("Please type DELETE to confirm account removal.")
        return value
