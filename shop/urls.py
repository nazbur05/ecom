from django.urls import path
from .views import home, signup, login, cart, checkout, orders, favourites, profile

urlpatterns = [
    path('', home.home_view, name='home'),
    path('signup/', signup.signup_view, name='signup'),
    path('login/', login.login_view, name='login'),
    path('logout/', login.logout_view, name='logout'),
    path('cart/', cart.cart_view, name='cart'),
    path('checkout/', checkout.checkout_view, name='checkout'),
    path('orders/', orders.orders_view, name='orders'),
    path('favourites/', favourites.favourites_view, name='favourites'),
    path('profile/', profile.profile_view, name='profile')
]
