from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shop.models import Customer

@login_required(login_url='login')
def favourites_view(request):
    customer = Customer.objects.get(user=request.user)
    favourites = customer.get_favourites()
    return render(request, 'shop/favourites.html', {
        'favourites': favourites,
        'is_authenticated': request.user.is_authenticated,
    })