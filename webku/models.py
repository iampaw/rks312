# webku/models.py

from django.db import models
from django.contrib.auth.models import User

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

    def __str__(self):
        return self.nama_category\

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Menghubungkan model ini dengan model User
    full_name = models.CharField(max_length=100)

    
    def __str__(self):
        return self.user.username