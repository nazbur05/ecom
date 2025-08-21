from django.shortcuts import render
from shop.models import Order, Customer, Product

def checkout_view(request):
    return render(request, 'shop/checkout.html')