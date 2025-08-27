# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shop.models import Customer, Category, Product, SubCategory, Order

def home_view(request):
    customer = Customer.objects.get(user=request.user)
    favourites = set(customer.get_favourites().values_list('id', flat=True))
    cart_products = set(Order.objects.filter(customer=customer, status=False).values_list('product_id', flat=True))
    categories = Category.get_all_categories()
    subcategories = SubCategory.get_all_subcategories()
    products = Product.objects.all().order_by('-id')[:8]
    return render(request, 'shop/home.html', {'categories': categories, 'subcategories': subcategories, 'products': products, 'favourites': favourites, 'cart_products': cart_products})