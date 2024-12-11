from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from .models import Makanan, Makanan2, LoginHistory, Profile, Address
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.utils.timezone import now
import logging
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm, UserUpdateForm
from .forms import AddressForm

logger = logging.getLogger(__name__)

def profile(request):
    return render(request, 'profile.html')

def home(request):
    return render(request, 'home.html', {
        'user_authenticated': request.user.is_authenticated
    })  # Pastikan Anda memiliki template 'home.html'

def checkout(request):
    cart = request.session.get("cart", [])
    return render(request, "checkout.html", {"cart": cart})

def address_view(request):
    return render(request, 'address.html')

@login_required
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
    else:
        # Jika user tidak login, redirect ke halaman signup
        return redirect('signup')  # Atau bisa juga 'login' jika ingin halaman login terlebih dahulu

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

def user_login(request):
    if request.method == "POST":
        # Mendapatkan data username dan password dari form POST
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Mencoba untuk mengautentikasi pengguna
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Jika autentikasi berhasil, login pengguna
            login(request, user)

            # Log keberhasilan login
            logger.info(f"User {username} berhasil login.")
            logger.info(f"Email: {user.email}, IP: {get_client_ip(request)}")

            # Simpan riwayat login ke database
            try:
                LoginHistory.objects.create(
                    user=user,
                    email=user.email,
                    login_time=now(),
                    ip_address=get_client_ip(request)
                )
                logger.info("Riwayat login berhasil disimpan.")
            except Exception as e:
                logger.error(f"Error saat menyimpan riwayat login: {str(e)}")

            # Redirect pengguna ke halaman 'next' atau halaman home
            next_url = request.GET.get('next', 'home')  # Jika tidak ada 'next', default ke 'home'
            return redirect(next_url)

        else:
            # Jika autentikasi gagal, log kegagalan login
            logger.warning(f"Login gagal untuk {username}.")
            messages.error(request, "Username atau password tidak valid.")
            return redirect('login')  # Kembali ke halaman login untuk mencoba lagi

    # Jika request menggunakan metode GET, tampilkan halaman login
    return render(request, 'login.html')
        
def logout_view(request):
    logout(request)
    return redirect('home')  # Alihkan ke homepage setelah logout

def home_page(request):
    makanan_list = Makanan.objects.all()  # Ambil semua data makanan dari database
    makanan2_list = Makanan2.objects.all() 
    context = {
        'makanan_list': makanan_list,
        'makanan2_list': makanan2_list,
    }
    return render(request, 'home.html', context)


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)  # Ambil data profile yang terkait dengan user yang sedang login
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        gender = request.POST.get('gender')
        birth_date = request.POST.get('birth_date')
        
        # Update data profile
        profile.phone_number = phone_number
        profile.gender = gender
        profile.birth_date = birth_date
        profile.save()
        
        return redirect('profile')  # Redirect ke halaman profile setelah update

    return render(request, 'profile.html', {'profile': profile})

@login_required
def address_view(request):
    if request.method == 'POST':
        # Mengambil data dari request.POST
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        province = request.POST.get('province')
        city = request.POST.get('city')
        postal_code = request.POST.get('postal_code')
        housing_address = request.POST.get('housing_address')

        # Validasi data (bisa disesuaikan dengan kebutuhan)
        if full_name and phone and province and city and postal_code and housing_address:
            # Menyimpan data ke database
            address = Address(
                user=request.user,  # Pastikan menyimpan data dengan user yang sedang login
                full_name=full_name,
                phone=phone,
                province=province,
                city=city,
                postal_code=postal_code,
                housing_address=housing_address
            )
            address.save()
            return redirect('address')  # Setelah berhasil simpan, redirect ke halaman yang sama
        else:
            # Jika ada data yang kosong, bisa menambahkan pesan error atau penanganan lainnya
            error_message = 'Please fill out all fields.'
            return render(request, 'address.html', {'error_message': error_message})
    else:
        return render(request, 'address.html')
    
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip