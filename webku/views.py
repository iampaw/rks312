from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Makanan

def home(request):
    return render(request, 'home.html')  # Pastikan Anda memiliki template 'home.html'

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Simpan pengguna baru
            username = form.cleaned_data.get('username')
            messages.success(request, f'Akun {username} telah berhasil dibuat! Anda sekarang dapat masuk.')
            return redirect('login')  # Alihkan ke halaman login setelah signup
    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Ganti 'home' dengan nama URL yang sesuai untuk homepage Anda
    else:
        form = AuthenticationForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Alihkan ke homepage setelah logout

def home_page(request):
    makanan_list = Makanan.objects.all()  # Ambil semua data makanan dari database
    context = {
        'makanan_list': makanan_list,
    }
    return render(request, 'home.html', context)
