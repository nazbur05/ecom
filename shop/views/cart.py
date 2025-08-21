from django.shortcuts import render
from shop.models import Order, Customer, Product

def cart_view(request):
    return render(request, 'shop/cart.html')