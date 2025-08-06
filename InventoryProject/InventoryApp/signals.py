from itertools import product

from django.db.models import F, Sum, DecimalField
from django.db.models.signals import post_save, pre_save
from  django.dispatch import receiver

from .models import Product, Stocks, Customer, Order, IncomingStocks


@receiver(post_save, sender=Product)
def create_stocks_model(sender, instance, created, **kwargs):
    if created:
        total_quantity = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
                                 #total_price_per_insert = Product.objects.aggregate(total_value=Sum(('price') * F('quantity')), output_field=DecimalField())['total_value'] or 0
                                  # Multiply using F() and specify output_field
        total_price_per_insert = Product.objects.aggregate(total_value=Sum( F('price') * F('quantity'),output_field=DecimalField()))['total_value'] or 0

        Stocks.objects.create(
            product=instance,
            supplier=instance.supplier,
           actual_count = total_quantity,
            total_price = total_price_per_insert,
        )
        print("Stocks object from Django Signal")

#buhat  tag signal dri a pg mag update sa isa ka product mag insert padulong stocks model

@receiver(post_save, sender = Product)
def create_incoming_stock(sender, instance,created, **kwargs):
    if created:
        IncomingStocks.objects.create(
            product = instance,
            supplier = instance.supplier

        )






'''
@receiver(post_save, sender=Product)
def create_stocks_model(sender,instance, created, **kwargs):
    if created:
        Stocks.objects.create(product=instance)
'''