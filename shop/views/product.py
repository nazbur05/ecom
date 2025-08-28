from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from shop.models import Category, SubCategory, Product

def product_api_detail(request, pk):
    return render(request, 'shop/product.html', {
        'product_id': pk,
        'is_authenticated': request.user.is_authenticated,
    })

def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.get_all_products_by_categoryid(category_id).order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.get_all_categories()
    return render(request, 'shop/products.html', {
        'products': products,
        'category': category,
        'subcategory': None,
        'categories': categories,
        'is_authenticated': request.user.is_authenticated,
        'page_obj': page_obj,
    })

def products_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
    products = Product.get_all_products_by_subcategoryid(subcategory_id).order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    categories = Category.get_all_categories()
    return render(request, 'shop/products.html', {
        'products': products,
        'category': subcategory.parent,
        'subcategory': subcategory,
        'categories': categories,
        'is_authenticated': request.user.is_authenticated,
        'page_obj': page_obj,
    })