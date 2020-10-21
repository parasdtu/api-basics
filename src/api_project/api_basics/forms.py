from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import authenticate

from .models import UserAPI


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Add a valid email address.')

    class Meta:
        model = UserAPI
        fields = ('email', 'name', 'password1', 'password2',)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserAPI
        fields = ('email', 'name',)
