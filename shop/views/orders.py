from django.shortcuts import render
from shop.models import Order, Customer, Product

def orders_view(request):
    return render(request, 'shop/orders.html')