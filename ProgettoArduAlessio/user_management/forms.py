from django import forms
from django.contrib.auth.forms import UserCreationForm

from user_management.models import MyUser


class MyUserCreationForm(UserCreationForm):
    #email = forms.EmailField(required=True)

    class Meta:
        model = MyUser
        fields = ("username", "email", "password1", "password2", "first_name", "last_name", "birth_date", "photo",)
