from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm

class UserSignUpForm(UserCreationForm):
    # refid = forms.CharField(initial='class', max_length=100, widget = forms.HiddenInput())
    # phone_number = forms.CharField(label='Phone number', max_length=100)
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "gender"]
