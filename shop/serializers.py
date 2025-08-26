from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, SubCategory, Product, Customer, Order

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'parent']

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)
    class Meta:
        model = Category
        fields = ['id', 'name', 'subcategories']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    subcategory = SubCategorySerializer(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'description', 'image', 'category', 'subcategory']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    favourites = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'favourites']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product', 'customer', 'quantity', 'price', 'date', 'status']