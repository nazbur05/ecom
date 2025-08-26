from django.shortcuts import render

def product_api_detail(request, pk):
    return render(request, 'shop/product.html', {'product_id': pk})