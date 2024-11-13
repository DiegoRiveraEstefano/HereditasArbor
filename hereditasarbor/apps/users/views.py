from typing import Any

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import QuerySet
from django.db.models.base import Model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import RedirectView
from django.views.generic import UpdateView

from hereditasarbor.apps.users.models import User

from .forms import UserCreationForm
from .forms import UserLoginForm
from .forms import UserLogOutForm


class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    template_name = "users/user_create.html"

    def get_object(self, queryset: QuerySet[Any] | None) -> Model:
        return super().get_object(queryset)()

    def get_success_url(self) -> str:
        return reverse("users:login")


user_create_view = UserCreateView.as_view()


class UserLoginFormView(FormView):
    form_class = UserLoginForm
    template_name = "users/user_login.html"

    def get_success_url(self) -> str:
        if self.request.user.has_personal_data:
            return reverse("users:me")
        return reverse("personal:create")

    def form_valid(self, form: UserLoginForm):
        user = authenticate(
            request=self.request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            return super().form_invalid(form)
        login(
            request=self.request,
            user=user,
            backend="django.contrib.auth.backends.ModelBackend",
        )
        return super().form_valid(form)


user_login_view = UserLoginFormView.as_view()


class UserLogOutView(FormView, LoginRequiredMixin, SuccessMessageMixin):
    template_name = "users/views/user_logout.html"
    form_class = UserLogOutForm
    success_message = "Session Cerrada Correctamente"

    def get_success_url(self):
        return reverse("home")

    def form_valid(self, form):
        logout(self.request)
        return super().form_valid(form)


user_log_out_view = UserLogOutView.as_view()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"

    def get_queryset(self) -> QuerySet[Any]:
        return self.model.objects.filter(pk=self.request.user.pk)

    def get_object(self, queryset: QuerySet[Any] | None = None) -> Model:
        return User.objects.get(pk=self.request.user.pk)


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    fields = ["name"]
    success_message = _("Information successfully updated")

    def get_success_url(self) -> str:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user.get_absolute_url()

    def get_object(self, queryset: QuerySet | None = None) -> User:
        assert self.request.user.is_authenticated  # type guard
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self) -> str:
        return reverse("users:detail", kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()
