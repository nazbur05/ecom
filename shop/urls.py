from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import home, signup, login, cart, checkout, orders, favourites, profile, product
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
    path('product/<int:pk>/', product.product_api_detail, name='product'),
    path('products/category/<int:category_id>/', product.products_by_category, name='products_by_category'),
    path('products/subcategory/<int:subcategory_id>/', product.products_by_subcategory, name='products_by_subcategory'),
    path('orders/', orders.orders_view, name='orders'),
    path('profile/', profile.profile_view, name='profile'),

]