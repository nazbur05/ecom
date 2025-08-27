from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from shop.models import Order, Customer, Product

@login_required(login_url='login')
def cart_view(request):
    return render(request, 'shop/cart.html')