from audioop import reverse
from decimal import Decimal
from turtle import Turtle

from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import bisect_keep_left
from django.contrib.staticfiles.views import serve

from django.db import models
from django.db.models import ForeignKey


# Create your models here.



class Customer(models.Model):
    customer_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=False)
    number = models.CharField(max_length=255)
    address = models.TextField(max_length=255, blank=True,null=True)

    def __str__(self):
        return self.first_name +" "+ self.last_name

    def get_absolute_url(self):
        return reverse('order')

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return  self.category_name

class Supplier(models.Model):
    supplier_id  = models.AutoField(primary_key = True)
    supplier_name = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=False)
    address = models.TextField(max_length=255)

    def __str__(self):
        return self.supplier_name

class ProductName(models.Model):
    product_name_id = models.AutoField(primary_key = True)
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name


class Product(models.Model):
    product_id = models.AutoField(primary_key = True)
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE, null=True, blank=True)
    product_description = models.TextField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE,  null=True, blank=True) # on_delete = models.CASCADE sa Foreign key og OnetoOne rani pwde
    transaction_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    product_image = models.ImageField(null=True, blank=True,upload_to="images/")
    sum_per_transaction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return (f"{self.product_name} {self.price}")



class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product =models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=True)
    order_quantity = models.IntegerField(blank=True,null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )

    def __str__(self):
        return (f"{self.customer} {self.product}")

class Checkout(models.Model):
    checkout_id = models.AutoField(primary_key = True)
    product_name = models.ForeignKey(ProductName, on_delete=models.CASCADE, null=True,blank=True)
    customer_name = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product_price = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    checkout_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    checkout_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.product_name)

class Stocks(models.Model):
    stocks_id = models.AutoField(primary_key = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True) # Do not change. THe product name in stocks will disappear
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    actual_count = models.IntegerField(blank=True,null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)


    def __str__(self):
        return f"{self.actual_count}"


