
from django.db import models
from django.contrib.auth.models import User


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_price(self):
        return sum(item.subtotal() for item in self.cartitem_set.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def _str_(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)

    def _str_(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
# make seller nullable temporarily
    # Seller can be null temporarily to avoid migration prompt
    seller = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # Link to category
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.name