from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from shop.models import Customer, Product, Order, Category, SubCategory

# --- Auth Views ---

def signup_view(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")

        errors = []
        if password1 != password2:
            errors.append('Passwords do not match.')
        if User.objects.filter(email=email).exists():
            errors.append('Email is already in use.')
        if User.objects.filter(username=username).exists():
            errors.append('Username is already taken.')
        if not first_name or not last_name:
            errors.append('First name and last name are required.')

        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'shop/signup.html')
        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password1,
                first_name=first_name,
                last_name=last_name
            )
            login(request, user)
            return redirect('/shop/')
    return render(request, 'shop/signup.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'shop/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

# --- Profile View ---

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
        if email:
            customer.user.email = email
        customer.user.save()
        customer.phone = phone
        customer.save()
        return redirect('profile')
    return render(request, 'shop/profile.html', {'customer': customer})

# --- Home View ---

def home_view(request):
    products = Product.objects.all().order_by('id')
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    favourites = set()
    cart_products = set()
    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)
        favourites = set(customer.get_favourites().values_list('id', flat=True))
        cart_products = set(Order.objects.filter(customer=customer, status=False).values_list('product_id', flat=True))
    return render(request, 'shop/home.html', {
        'products': products,
        'page_obj': page_obj,
        'favourites': favourites,
        'cart_products': cart_products,
        'is_authenticated': request.user.is_authenticated,
    })

# --- Product Views ---

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

# --- Favourites View ---

@login_required(login_url='login')
def favourites_view(request):
    customer = Customer.objects.get(user=request.user)
    favourites = customer.get_favourites().order_by('id')
    paginator = Paginator(favourites, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/favourites.html', {
        'favourites': favourites,
        'page_obj': page_obj,
        'is_authenticated': request.user.is_authenticated,
    })

# --- Cart View ---

@login_required(login_url='login')
def cart_view(request):
    customer = Customer.objects.get(user=request.user)
    cart_orders = Order.objects.filter(customer=customer, status=False)
    cart_products = Product.objects.filter(id__in=cart_orders.values_list('product_id', flat=True)).order_by('id')
    paginator = Paginator(cart_products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/cart.html', {
        'products': cart_products,
        'page_obj': page_obj,
        'is_authenticated': request.user.is_authenticated,
    })

# --- Checkout View ---

@login_required(login_url='login')
def checkout_view(request):
    customer = Customer.objects.get(user=request.user)
    return render(request, 'shop/checkout.html', {'customer': customer})

# --- Orders View ---

@login_required(login_url='login')
def orders_view(request):
    customer = Customer.objects.get(user=request.user)
    orders = Order.objects.filter(customer=customer, status=True).order_by('-date')
    return render(request, 'shop/orders.html', {'orders': orders})