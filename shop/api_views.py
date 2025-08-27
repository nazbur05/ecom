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
    
    @action(detail=True, methods=['get'])
    def cart(self, request, pk=None):
        customer = self.get_object()
        orders = Order.objects.filter(customer=customer, status=False)
        products = []
        for order in orders:
            product_data = ProductSerializer(order.product).data
            product_data['quantity'] = order.quantity
            product_data['order_id'] = order.id
            products.append(product_data)
        return Response(products)

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
        
    @action(detail=True, methods=['post'])
    def add_to_cart(self, request, pk=None):
        customer = self.get_object()
        product_id = request.data.get('product_id')
        product = Product.objects.filter(pk=product_id).first()
        if product:
            Order.objects.create(customer=customer, product=product, price=product.price, status=False)
            return Response({'status': 'added'}, status=status.HTTP_200_OK)
        return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def remove_from_cart(self, request, pk=None):
        customer = self.get_object()
        product_id = request.data.get('product_id')
        order = Order.objects.filter(customer=customer, product_id=product_id, status=False).first()
        if order:
            order.delete()
            return Response({'status': 'removed'}, status=status.HTTP_200_OK)
        return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=True, methods=['post'])
    def update_cart_quantity(self, request, pk=None):
        customer = self.get_object()
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))
        order = Order.objects.filter(customer=customer, product_id=product_id, status=False).first()
        if order:
            order.quantity = quantity
            order.save()
            return Response({'status': 'updated'}, status=status.HTTP_200_OK)
        return Response({'error': 'Product not in cart'}, status=status.HTTP_404_NOT_FOUND)
    
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer