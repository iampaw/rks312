# webku/models.py

from django.db import models

class Makanan(models.Model):
    nama_menu = models.CharField(max_length=100)
    harga = models.DecimalField(max_digits=10, decimal_places=2)
    gambar = models.ImageField(upload_to='makanan_images/')

    def __str__(self):
        return self.nama_menu
