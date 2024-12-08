# webku/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from django.utils.timezone import now

class Makanan(models.Model):
    nama_menu = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar = models.ImageField(upload_to='makanan_images/')

    def __str__(self):
        return self.nama_menu

class makanan2(models.Model):
    nama_category = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar = models.ImageField(upload_to='category_makanan/')
    category = models.CharField(max_length=50, default='', choices=[
        ('Ice Cream', 'Ice Cream'),
        ('Maccarone', 'Maccarone'),
        ('Cookies', 'Cookies'),
    

    ])

    def __str__(self):
        return self.nama_category

class UserProfileAdmin(models.Model):
    list_display = ('user', 'full_name', 'user_email', 'last_login', 'is_active')

    # Fungsi untuk menampilkan email dari User
    def user_email(self, obj):
        return obj.user.email
    user_email.short_description = 'Email'

    # Fungsi untuk menampilkan login terakhir dari User
    def last_login(self, obj):
        return obj.user.last_login
    last_login.short_description = 'Last Login'

    # Fungsi untuk menampilkan status aktif
    def is_active(self, obj):
        return obj.user.is_active
    is_active.short_description = 'Active'
    is_active.boolean = True

class LoginHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_history')
    email = models.EmailField()
    login_time = models.DateTimeField(default=now)
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time}"
    

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    birth_date = models.DateField()

    def __str__(self):
        return self.user.username