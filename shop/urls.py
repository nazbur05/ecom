from django.urls import path
from .views import home, signup, login

urlpatterns = [
    path('', home.home_view, name='home'),
    path('signup/', signup.signup_view, name='signup'),
    path('login/', login.login_view, name='login'),
    path('logout/', login.logout_view, name='logout'),
]
