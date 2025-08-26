from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from shop.models import Customer

@login_required
def profile_view(request):
    customer = Customer.objects.get(user=request.user)
    context = {
        'customer': customer
    }
    return render(request, 'shop/profile.html', context)