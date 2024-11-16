from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Makanan, makanan2
from django.http import HttpResponse
from django.contrib.auth.models import User



def home(request):
    return render(request, 'home.html')  # Pastikan Anda memiliki template 'home.html'

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validasi form secara manual
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')  # Kembali ke halaman signup

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('signup')

        # Memeriksa apakah email sudah ada
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use another email.")
            return redirect('signup')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()

            # Membuat profil pengguna baru jika diperlukan
            user_profile = UserProfile(user=user)
            user_profile.save()

            messages.success(request, "Account created successfully!")
            return redirect('user_profile', user_id=user.id)  # Mengarahkan pengguna ke halaman profil

        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('signup')
    
    return render(request, 'signup.html')  # Pastikan Anda merender form signup jika GET request

def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Autentikasi pengguna
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Jika autentikasi berhasil, login pengguna
            login(request, user)  # Gunakan login dari Django
            messages.success(request, "Login successful!")
            return redirect('home')  # Alihkan ke halaman home setelah login berhasil
        else:
            # Jika login gagal
            messages.error(request, "Invalid username or password!")
            return redirect('custom_login')  # Kembali ke halaman login jika login gagal

    return render(request, 'home.html')  # Render halaman login jika metode GET

def logout_view(request):
    logout(request)
    return redirect('home')  # Alihkan ke homepage setelah logout

def home_page(request):
    makanan_list = Makanan.objects.all()  # Ambil semua data makanan dari database
    makanan2_list = makanan2.objects.all() 
    context = {
        'makanan_list': makanan_list,
        'makanan2_list': makanan2_list,
    }
    return render(request, 'home.html', context)

