from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True )
    last_name = forms.CharField(max_length=50, required=True )
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "first_name","last_name","email","password1","password2"]