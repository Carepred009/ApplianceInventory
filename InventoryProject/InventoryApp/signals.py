

from django.db.models.signals import post_save
from  django.dispatch import receiver

from . models import Product, Stocks

@receiver(post_save, sender=Product)
def create_stocks_model(sender, instance, created, **kwargs):
    if created:
        Stocks.objects.create(
            product=instance,
            supplier=instance.supplier,
            actual_count =+ instance.quantity

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