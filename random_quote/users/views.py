from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse_lazy
from users.forms import ProfileForm, RegisterUserForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from random_quote.settings import DEFAULT_IMAGE
from quotes.models import Quote
from users.services.delete_saved_quotes_service import DeleteSavedQuotesService


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    success_url = reverse_lazy("users:suggested_quotes")
    template_name = "users/user_register.html"
    extra_context = {"title": "Регистрация", "button": "Зарегистрироваться"}


class LoginUser(LoginView):
    template_name = "users/login.html"
    form_class = AuthenticationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("users:suggested_quotes")
        return super().dispatch(request, *args, **kwargs)


class EditProfileUserView(LoginRequiredMixin, UpdateView):
    template_name = "users/edit_profile.html"
    form_class = ProfileForm
    success_url = reverse_lazy("users:edit_profile")
    extra_context = {"default_photo": DEFAULT_IMAGE}

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Ваш профиль успешно обновлен!")
        return super().form_valid(form)


class ProfileUserSuggestedQuotesView(LoginRequiredMixin, ListView):
    template_name = "users/user_suggested_quotes.html"
    context_object_name = "suggested_quotes"
    extra_context = {"default_photo": DEFAULT_IMAGE}

    def get_queryset(self):
        return (
            Quote.objects.select_related("author")
            .prefetch_related("category")
            .filter(user=self.request.user)
        )


class ProfileUserSavedQuotesView(LoginRequiredMixin, ListView):
    template_name = "users/user_saved_quotes.html"
    context_object_name = "saved_quotes"
    extra_context = {"default_photo": DEFAULT_IMAGE}

    def get_queryset(self):
        user = get_user_model().objects.get(id=self.request.user.id)
        return user.profile.saved_quotes.all()


class ProfileUserDeleteSavedQuotesView(LoginRequiredMixin, UpdateView):
    template_name = "users/saved_quotes"
    model = get_user_model()
    fields = []

    def get_object(self, queryset=None):
        return get_user_model().objects.get(id=self.request.user.id)

    def get(self, request, *args, **kwargs):
        user = self.get_object()

        if DeleteSavedQuotesService(self.kwargs["id"], user).delete():
            messages.success(self.request, "Цитата успешно удалена")

        else:
            messages.error(self.request, "Цитата не найдена!")

        return redirect("users:saved_quotes")
