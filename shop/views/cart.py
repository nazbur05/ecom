from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from shop.models import Order, Customer, Product

@login_required(login_url='login')
def cart_view(request):
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/cart.html', {
        'products': products,
        'page_obj': page_obj,
        'is_authenticated': request.user.is_authenticated,
    })