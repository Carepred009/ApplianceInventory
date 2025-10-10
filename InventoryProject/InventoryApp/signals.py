from itertools import product
from venv import create

from django.db.models import F, Sum, DecimalField

from django.db.models.signals import post_save, pre_save
from  django.dispatch import receiver
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.conf import settings


from .models import Product, Stocks, Customer, Order, IncomingStocks

@receiver(post_save, sender=Product)
def update_stocks_from_product(sender, instance, **kwargs):
    # Always update or create the stock record for this product
    total_quantity = instance.quantity
    total_price = instance.price * instance.quantity

    Stocks.objects.update_or_create(
        product=instance,
        defaults={
            'supplier': instance.supplier,
            'actual_count': total_quantity,
            'total_price': total_price
        }
    )

@receiver(post_save, sender = Product)
def create_incoming_stock(sender, instance,created, **kwargs):
    if created:

        product_quantity = instance.quantity
        product_date = instance.transaction_date

        IncomingStocks.objects.create(
            product = instance,
            supplier = instance.supplier,
            incoming_count=product_quantity,
            incoming_date= product_date

        )

#send email the new user by the email given
@receiver(post_save,sender=User)
def send_welcome_mail(sender, instance, created, **kwargs):
    if created: #only send email for new users
        subject = "Welcome to our Appliance Inventory System"
        message = f"Hi {instance.username}, thank you for registering!"
        sender_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [instance.email]

        send_mail(subject,message,sender_email,recipient_list)
        print("✅ Welcome email sent to: ", instance.email)






'''
@receiver(post_save, sender=Product)
def create_stocks_model(sender, instance, created, **kwargs):
    if created:
        #total_quantity = Product.objects.aggregate(total=Sum('quantity'))['total'] or 0
                                 #total_price_per_insert = Product.objects.aggregate(total_value=Sum(('price') * F('quantity')), output_field=DecimalField())['total_value'] or 0
                                  # Multiply using F() and specify output_field
        total_quantity = Product.quantity
        total_price_per_insert = Product.objects.aggregate(total_value=Sum( F('price') * F('quantity'),output_field=DecimalField()))['total_value'] or 0

        Stocks.objects.create(
            product=instance,
            supplier=instance.supplier,
           actual_count = total_quantity,
            total_price = total_price_per_insert,
        )
        print("Stocks object from Django Signal")

#buhat  tag signal dri a pg mag update sa isa ka product mag insert padulong stocks model
'''


'''
@receiver(post_save, sender=Product)
def create_stocks_model(sender,instance, created, **kwargs):
    if created:
        Stocks.objects.create(product=instance)
'''