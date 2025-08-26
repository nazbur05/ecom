from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, SubCategory, Product, Customer, Order
from .serializers import CategorySerializer, SubCategorySerializer, ProductSerializer, CustomerSerializer, OrderSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    @action(detail=True, methods=['get'])
    def favourites(self, request, pk=None):
        customer = self.get_object()
        products = customer.favourites.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_favourite(self, request, pk=None):
        customer = self.get_object()
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            customer.favourites.add(product)
            return Response({'status': 'added'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_favourite(self, request, pk=None):
        customer = self.get_object()
        product_id = request.data.get('product_id')
        try:
            product = Product.objects.get(pk=product_id)
            customer.favourites.remove(product)
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer