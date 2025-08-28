from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import Customer

@login_required(login_url='login')
def profile_view(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if first_name:
            customer.user.first_name = first_name
        if last_name:
            customer.user.last_name = last_name
        customer.user.save()
        if email:
            customer.user.email = email
            customer.user.save()
        customer.phone = phone
        customer.save()
        return redirect('profile')
    return render(request, 'shop/profile.html', {'customer': customer})