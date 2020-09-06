from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password2']  # Removing password2 to avoid password confirmation while registering

    class Meta:
        model = User
        fields = ['username', 'password1', 'email']
