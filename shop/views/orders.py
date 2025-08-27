from django.shortcuts import render
from shop.models import Order, Customer

def orders_view(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer, status=True).order_by('-date')
        return render(request, 'shop/orders.html', {'orders': orders})
    return render(request, 'shop/orders.html')