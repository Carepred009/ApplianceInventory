from turtle import Turtle

from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Customer(models.Model):
    customer_id = models.AutoField(primary_key = True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255,unique=False)
    number = models.CharField(max_length=255)
    address = models.TextField(max_length=255, blank=True,null=True)

    def __str__(self):
        return self.first_name

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


class Product(models.Model):
    product_id = models.AutoField(primary_key = True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField(max_length=255)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ManyToManyField(Supplier,  null=True, blank=True) # on_delete = models.CASCADE sa Foreign key og OnetoOne rani pwde

    def __str__(self):
        return self.product_name


class Order(models.Model):
    order_id = models.AutoField(primary_key = True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product =models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(auto_now_add=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True )

    def __str__(self):
        return (f"{self.customer} {self.product}")

class Stocks(models.Model):
    stocks_id = models.AutoField(primary_key = True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    percentage = models.CharField(max_length=100)

    def __str__(self):
        return self.percentage
