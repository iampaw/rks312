from django.contrib import admin
from .models import Makanan, makanan2
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


admin.site.register(Makanan)
admin.site.register(makanan2)


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

class Meta:
    model = User
    list_display = ['username', 'email', 'password1', 'password2']

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff')  # Tambahkan kolom yang diinginkan
    list_filter = ('is_active', 'is_staff')  # Filter
    search_fields = ('username', 'email')  # Pencarian

admin.site.unregister(User)  # Unregister User default
admin.site.register(User, CustomUserAdmin)


