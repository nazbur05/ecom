from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render
from shop.models import Customer, Product

@login_required(login_url='login')
def favourites_view(request):
    customer = Customer.objects.get(user=request.user)
    favourites = customer.get_favourites()
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/favourites.html', {
        'favourites': favourites,
        'page_obj': page_obj,
        'is_authenticated': request.user.is_authenticated,
    })