from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, signup, login, cart, checkout, orders, favourites, profile
from .api_views import CategoryViewSet, SubCategoryViewSet, ProductViewSet, CustomerViewSet, OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', home.home_view, name='home'),
    path('signup/', signup.signup_view, name='signup'),
    path('login/', login.login_view, name='login'),
    path('logout/', login.logout_view, name='logout'),
    path('cart/', cart.cart_view, name='cart'),
    path('checkout/', checkout.checkout_view, name='checkout'),
    path('orders/', orders.orders_view, name='orders'),
    path('favourites/', favourites.favourites_view, name='favourites'),
    path('profile/', profile.profile_view, name='profile'),
    
    path('api/', include(router.urls)),
]