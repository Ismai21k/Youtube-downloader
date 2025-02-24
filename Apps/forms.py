from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True, help_text="Enter your first name")
    last_name = forms.CharField(max_length=50, required=True, help_text="Enter your last name")
    email = forms.EmailField(required=True, help_text="Enter your Email address")

    class Meta:
        model = User
        fields = ["username", "first_name","last_name","email","password1","password2"]