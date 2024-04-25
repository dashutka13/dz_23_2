from random import randint

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect

from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views import View

from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserForm
from users.models import User


class LoginView(BaseLoginView):
    template_name = 'users/login.html'


class LogoutView(LoginRequiredMixin, BaseLogoutView):
    pass


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        new_user = form.save()

        token = get_random_string(length=50)
        new_user.verify_key = token

        new_user.save()

        current_site = get_current_site(self.request)

        send_mail(
            subject='Завершение регистрации',
            message=f'Для подтверждения электронной почты перейдите по следующей ссылке: \n'
                    f'http://{current_site.domain}{reverse("users:verify", kwargs={"uid": new_user.pk, "token": token})}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],

        )
        return super().form_valid(form)


class VerifyView(View):
    def get(self, request, uid, token):
        user = get_object_or_404(User, pk=uid, verify_key=token)
        user.is_verified = True
        user.save()
        return render(request, 'users/verified.html')


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    success_url = reverse_lazy('users:profile')
    form_class = UserForm

    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_verified:
            return HttpResponseForbidden("Подтвердите электронную почту перейдя по ссылке из письма. ")
        return super().dispatch(request, *args, **kwargs)


def generate_new_password(request):
    new_password = ''.join([str(randint(0, 9)) for _ in range(12)])

    send_mail(
        subject='Вы сменили пароль!',
        message=f'Ваш новый пароль: {new_password}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[request.user.email]
    )
    request.user.set_password(new_password)
    request.user.save()

    return render(request, 'users/password_reset.html')
