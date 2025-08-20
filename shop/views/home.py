from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

@login_required
def home_view(request):
    return render(request, 'shop/home.html')