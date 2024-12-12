from django.contrib import admin
from .models import Makanan, Makanan2, LoginHistory, Address
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

admin.site.register(Profile)
admin.site.register(Makanan)
admin.site.register(Makanan2)


class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

class Meta:
    model = User
    list_display = ['username', 'email', 'password1', 'password2']

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_login', 'is_active', 'is_staff')  # Tambahkan kolom yang diinginkan
    list_filter = ('is_active', 'is_staff')  # Filter
    search_fields = ('username', 'email')  # Pencarian
    
@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'login_time', 'ip_address')
    search_fields = ('user__username', 'email')
    list_filter = ('login_time',)

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'full_name', 'phone', 'city', 'postal_code')

admin.site.unregister(User)  # Unregister User default
admin.site.register(User, CustomUserAdmin)


