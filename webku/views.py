# webku/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def home(request):
    return render(request, 'home.html')

def signup(request):
    # Jika request POST untuk login
    if 'login' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')

    # Jika request POST untuk signup
    elif 'signup' in request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully!')
            return redirect('signup')

    else:
        form = UserCreationForm()

    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('home')
