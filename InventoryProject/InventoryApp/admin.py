from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Customer
from .models import Customer, Category, Supplier, Product, Order, Stocks, ProductName, Checkout, IncomingStocks


# Register your models here.
#Arrange to Display data from Customer model
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','last_name','number')

admin.site.register(Customer,CustomerAdmin) # this is Error


#admin.site.register(Customer) Remove the other registered model
admin.site.register(Category)
admin.site.register(Supplier)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Stocks)
admin.site.register(ProductName)
admin.site.register(Checkout)
admin.site.register(IncomingStocks)


