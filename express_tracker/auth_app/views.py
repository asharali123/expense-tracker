from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile

def register(request):
    #Step 1: If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = request.POST.get('phone')

        #Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        #Create user
        user = User.objects.create_user(username=username, email=email, password=password)

        #Create related profile
        Profile.objects.create(user=user, phone=phone)

        messages.success(request, 'Account created successfully! You can now log in.')
        return redirect('login')

    return render(request, 'register.html')

def user_login(request):
    #Step 1: If user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    #Step 2: Handle login form submission
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('login')

    #Step 3: Render login page if not logged in
    return render(request, 'login.html')

@login_required(login_url='login')
def user_logout(request):
    logout(request)  #This clears the user session
    messages.info(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to login page