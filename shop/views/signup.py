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
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        errors = []
        if password1 != password2:
            errors.append('Passwords do not match.')
        if User.objects.filter(email=email).exists():
            errors.append('Email is already in use.')
        if User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        if not first_name or not last_name:
            errors.append('First name and last name are required.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'shop/signup.html')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('/shop/')
    return render(request, 'shop/signup.html')