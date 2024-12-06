from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Makanan, makanan2, LoginHistory
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.utils.timezone import now
import logging
logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'home.html')  # Pastikan Anda memiliki template 'home.html'

def checkout(request):
    cart = request.session.get("cart", [])
    return render(request, "checkout.html", {"cart": cart})

def add_to_cart(request):
    if request.method == "POST":
        item = request.POST
        cart = request.session.get("cart", [])
        cart.append({
            "name": item.get("name"),
            "price": float(item.get("price")),
            "image": item.get("image"),
        })
        request.session["cart"] = cart
        return JsonResponse({"success": True})

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        # Validasi password
        if password1 != password2:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # Memeriksa ketersediaan username dan email
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose another one.")
            return redirect('signup')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists. Please use another email.")
            return redirect('signup')

        # Membuat user baru
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('signup')  # Kembali ke form login di halaman yang sama
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('signup')

    return render(request, 'signup.html')

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
        logger.info(f"IP Address obtained from X-Forwarded-For: {ip}")
    else:
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f"IP Address obtained from REMOTE_ADDR: {ip}")
    return ip

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Log jika login berhasil
            logger.info(f"User {username} logged in successfully.")
            logger.info(f"Email: {user.email}, IP: {get_client_ip(request)}")

            # Simpan riwayat login
            try:
                LoginHistory.objects.create(
                    user=user,
                    email=user.email,
                    login_time=now(),
                    ip_address=get_client_ip(request)
                )
                logger.info("Login history saved successfully.")
            except Exception as e:
                logger.error(f"Error saving login history: {str(e)}")

            return redirect('home')  # Redirect ke halaman home setelah login
        else:
            logger.warning(f"Login failed for {username}.")
            messages.error(request, "Invalid username or password.")
            return redirect('signup')
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


