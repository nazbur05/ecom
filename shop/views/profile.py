from django.shortcuts import render
from shop.models import Customer

def profile_view(request):
    return render(request, 'shop/profile.html')