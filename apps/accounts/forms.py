from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import OpenspritesUser

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class':'form-input', 'placeholder': 'Username'}))
    password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'form-input', 'placeholder': 'Password'}))


class JoinForm(UserCreationForm):
    username = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}))
    password1 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}))
    password2 = forms.CharField(required=True, widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm Password'}))

    class Meta:
        model = OpenspritesUser
        fields = ("username", "password1", "password2")

    def save(self, commit=True): # todo
        user = super(SignupForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        if commit:
            user.save()
        return user