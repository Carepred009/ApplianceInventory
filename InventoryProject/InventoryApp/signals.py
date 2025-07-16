from django.db.models import F, Sum, DecimalField
from django.db.models.signals import post_save, pre_save
from  django.dispatch import receiver

from .models import Product, Stocks, Customer,Order


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
'''
@receiver(post_save,sender=Customer)
def create_order_fullname(sender, instance,created, **kwargs):
    if created:
            #call the price from product
        # total_amount = Order.objects.aggregate()

        Order.objects.create(
            customer = instance,   # the inputed  first_name will be the  inserted into customer in Order model
        )
'''


@receiver(post_save, sender=Product)
def create_order_quantity(sendder, intance,created, **kwargs):
    if created:
        total_amount = Product.objects.aggregate()
        Order.objects.create(
            amount = total_amount
        )


'''
@receiver(post_save, sender=Product)
def create_or_update_stocks_model(sender, instance, created, **kwargs):
    if created:
        # Try to get existing stock entry for this product and supplier
        stock, stock_created = Stocks.objects.get_or_create(
            product=instance,
            supplier=instance.supplier,
            defaults={'actual_count': instance.quantity}  # if new, just set quantity
        )
        if not stock_created:
            # if stock already exists, just add the quantity
            stock.actual_count += instance.quantity
            stock.save()


'''






'''
@receiver(post_save, sender=Product)
def create_stocks_model(sender,instance, created, **kwargs):
    if created:
        Stocks.objects.create(product=instance)
'''