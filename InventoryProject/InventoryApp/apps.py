from django.apps import AppConfig

class InventoryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InventoryApp'

    def ready(self):
        import InventoryApp.signals  # make sure this matches your app name



'''
from django.apps import AppConfig


class InventoryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InventoryApp'

'''