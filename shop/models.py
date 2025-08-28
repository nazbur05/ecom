from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=50)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')

    class Meta:
        verbose_name = 'SubCategory'
        verbose_name_plural = 'SubCategories'

    @staticmethod
    def get_all_subcategories():
        return SubCategory.objects.all()

    def __str__(self):
        return f"{self.name} in {self.parent.name}"

class Product(models.Model):
    name = models.CharField(max_length=60)
    price = models.IntegerField(default=0)
    subcategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=1)
    description = models.CharField(max_length=250, default='', blank=True, null=True)
    image = models.ImageField(upload_to='uploads/products/')

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_products_by_id(ids):
        return Product.objects.filter(id__in=ids)
  
    @staticmethod
    def get_all_products_by_subcategoryid(subcategory_id):
        return Product.objects.filter(subcategory_id=subcategory_id)

    @staticmethod
    def get_all_products_by_categoryid(category_id):
        return Product.objects.filter(subcategory__parent_id=category_id)

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=10)
    favourites = models.ManyToManyField(Product, related_name='favourited_by', blank=True)

    @staticmethod
    def get_all_customers():
        return Customer.objects.all()

    def get_full_name(self):
        if self.user:
            return f"{self.user.first_name} {self.user.last_name}".strip()
        return ""

    def get_email(self):
        return self.user.email if self.user else ""

    def get_favourites(self):
        return self.favourites.all()

    def __str__(self):
        return self.user.username if self.user else "No user"
    
@receiver(post_save, sender=User)
def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_customer(sender, instance, **kwargs):
    if hasattr(instance, "customer"):
        instance.customer.save()

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)
    price = models.IntegerField()
    address = models.CharField(max_length=50, default='', blank=True)
    phone = models.CharField(max_length=50, default='', blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_all_orders():
        return Order.objects.all()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer_id=customer_id).order_by('-date')