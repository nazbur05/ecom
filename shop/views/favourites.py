from django.shortcuts import render
from shop.models import Customer

def favourites_view(request):
    customer = Customer.objects.get(user=request.user)
    favourites = customer.get_favourites()
    return render(request, 'shop/favourites.html', {'favourites': favourites})