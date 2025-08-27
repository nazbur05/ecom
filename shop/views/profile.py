from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from shop.models import Customer

@login_required(login_url='login')
def profile_view(request):
    customer = Customer.objects.get(user=request.user)
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        if full_name:
            names = full_name.split(' ', 1)
            customer.user.first_name = names[0]
            customer.user.last_name = names[1] if len(names) > 1 else ''
            customer.user.save()
        if email:
            customer.user.email = email
            customer.user.save()
        customer.phone = phone
        customer.save()
        return redirect('profile')
    return render(request, 'shop/profile.html', {'customer': customer})