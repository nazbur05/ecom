from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Category, SubCategory, Product, Customer, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class SubCategorySerializer(serializers.ModelSerializer):
    parent = CategorySerializer(read_only=True)
    parent_id = serializers.PrimaryKeyRelatedField(queryset=Category.get_all_categories(), source='parent', write_only=True)
    class Meta:
        model = SubCategory
        fields = ['id', 'name', 'parent', 'parent_id']

class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubCategorySerializer(read_only=True)
    subcategory_id = serializers.PrimaryKeyRelatedField(queryset=SubCategory.get_all_subcategories(), source='subcategory', write_only=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'subcategory', 'subcategory_id', 'description', 'image']

class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    favourites = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user', 'phone', 'favourites']

class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.get_all_products(), source='product', write_only=True)
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), source='customer', write_only=True)
    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_id', 'customer', 'customer_id',
            'quantity', 'price', 'address', 'phone', 'date', 'status'
        ]