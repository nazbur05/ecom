from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from shop.models import Customer, Product, Order

def home_view(request):
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        favourites = set(customer.get_favourites().values_list('id', flat=True))
        cart_products = set(Order.objects.filter(customer=customer, status=False).values_list('product_id', flat=True))
    else:
        favourites = set()
        cart_products = set()
    return render(request, 'shop/home.html', {
        'products': products,
        'page_obj': page_obj,
        'favourites': favourites,
        'cart_products': cart_products,
        'is_authenticated': request.user.is_authenticated,
    })