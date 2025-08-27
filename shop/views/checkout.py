from django.shortcuts import render
from shop.models import Order, Customer, Product

def checkout_view(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, 'shop/checkout.html', {'customer': customer})