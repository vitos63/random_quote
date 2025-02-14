from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()


class ProfileForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label="Логин")
    email = forms.EmailField(disabled=True, required=False, label="E-mail")
    photo = forms.ImageField(required=False, label="Фото")

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]
        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
            "last_name": forms.TextInput(attrs={"class": "form-input"}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        photo = self.cleaned_data.get("photo")
        if photo:
            user.profile.photo = photo
            user.profile.save()

        user.save()

        return user


class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "id": "password_field1"}
        ),
    )
    password2 = forms.CharField(
        label="Повтор пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-input", "id": "password_field2"}
        ),
    )
    username = forms.CharField(max_length=150, label="Логин")
    last_name = forms.CharField(max_length=150, required=False, label="Фамилия")
    email = forms.EmailField(label="E-mail")

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "password1",
            "password2",
        ]

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким E-mail уже существует")
        return email
