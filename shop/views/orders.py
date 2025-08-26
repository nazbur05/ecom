from django.shortcuts import render
from django.contrib.auth.models import User
from shop.models import Order, Customer, Product

def orders_view(request):
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        orders = Order.objects.filter(customer=customer).order_by('-date')
        for order in orders:
            product_ids = [int(pid) for pid in order.product_ids.split(',') if pid.isdigit()]
            products = Product.get_products_by_id(product_ids)
            order.products = products
        return render(request, 'shop/orders.html', {'orders': orders})
    return render(request, 'shop/orders.html')