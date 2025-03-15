from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm
from .models import User

class UsersCreationForm(UserCreationForm):
    username = forms.CharField(max_length=50, required=True)
    usable_password = None

    class Meta:
        model = User
        fields = ('email', 'username','password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super(UsersCreationForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control'})

class GeneratePasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields = ['email']

