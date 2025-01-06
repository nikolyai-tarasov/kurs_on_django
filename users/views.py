import random
import string
from django.contrib import messages
from config.settings import DEFAULT_FROM_EMAIL
from users.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, View
from django.views.generic import FormView
from .forms import UsersCreationForm, GeneratePasswordForm


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UsersCreationForm
    success_url = reverse_lazy('mailings:home')

    def form_valid(self, form):
        user = form.save()
        self.send_welcome_email(user.email)
        return super().form_valid(form)

    def send_welcome_email(self, user_email):
        subject = 'Добро пожаловать в наш сервис'
        message = 'Спасибо за ваше доверие !'
        from_email = DEFAULT_FROM_EMAIL
        recipient_list = [user_email, ]
        send_mail(subject, message, from_email, recipient_list)


class UserGenericPasswordView(FormView):
    form_class = GeneratePasswordForm
    template_name = 'generate_password.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = User.objects.filter(email=email).first()
        if not User:
            messages.error(self.request, "Вы ввели не верный email")
            return self.form_invalid(form)

        new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        user.set_password(new_password)
        user.save()
        send_mail(
            'Восстановить пароль',
            f'Ваш новый пароль: {new_password}',
            'djangoskypro@yandex.ru',
            [email],
        )
        return super().form_valid(form)
