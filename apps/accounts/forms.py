from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import OpenspritesUser

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-input', 'placeholder': 'Password'}))


class JoinForm(UserCreationForm):
    username = forms.CharField()
    email = forms.CharField()
    password1 = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = OpenspritesUser
        fields = ("username", "password1", "password2")