from django.contrib import admin
from .models import Makanan, makanan2
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

admin.site.register(Makanan)
admin.site.register(makanan2)
admin.site.register(UserProfile)

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

class Meta:
    model = User
    list_display = ['username', 'email', 'password1', 'password2']




