# webku/models.py

from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin

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
        ('makanan', 'Makanan'),
        ('minuman', 'Minuman'),
        ('cake', 'Cake'),
        ('cookies', 'Cookies'),

    ])

    def __str__(self):
        return self.nama_category

class UserProfileAdmin(admin.ModelAdmin):
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