import os
import random
import string
from django.contrib import messages
from users.models import User
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic import FormView
from .forms import UsersCreationForm, GeneratePasswordForm



class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = UsersCreationForm
    success_url = reverse_lazy('mailings:home')




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
            f'{os.getenv('EMAIL_HOST_USER')}',
            [email],
        )
        return super().form_valid(form)
