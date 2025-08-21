# from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shop.models import Category, Product, SubCategory

def home_view(request):
    categories = Category.get_all_categories()
    subcategories = SubCategory.get_all_subcategories()
    products = Product.objects.all().order_by('-id')[:8]
    return render(request, 'shop/home.html', {'categories': categories, 'subcategories': subcategories, 'products': products})