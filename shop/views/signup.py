from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")

        errors = []
        if password1 != password2:
            errors.append('Passwords do not match.')
        if User.objects.filter(email=email).exists():
            errors.append('Email is already in use.')
        if User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'shop/signup.html')
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            login(request, user)
            return redirect('home')
    return render(request, 'shop/signup.html')