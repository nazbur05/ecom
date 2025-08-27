from django.shortcuts import render, get_object_or_404
from shop.models import Category, SubCategory, Product

def product_api_detail(request, pk):
    return render(request, 'shop/product.html', {'product_id': pk})

def products_by_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    products = Product.get_all_products_by_categoryid(category_id)
    categories = Category.get_all_categories()
    return render(request, 'shop/products.html', {
        'products': products,
        'category': category,
        'subcategory': None,
        'categories': categories
    })

def products_by_subcategory(request, subcategory_id):
    subcategory = get_object_or_404(SubCategory, pk=subcategory_id)
    products = Product.get_all_products_by_subcategoryid(subcategory_id)
    categories = Category.get_all_categories()
    return render(request, 'shop/products.html', {
        'products': products,
        'category': subcategory.parent,
        'subcategory': subcategory,
        'categories': categories
    })