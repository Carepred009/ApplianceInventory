from django.contrib import admin

from .models import Customer, Category, Supplier, Product, Order, Stocks, ProductName, Checkout, IncomingStocks

# Register your models here.

admin.site.register(Customer)
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Stocks)
admin.site.register(ProductName)
admin.site.register(Checkout)
admin.site.register(IncomingStocks)
