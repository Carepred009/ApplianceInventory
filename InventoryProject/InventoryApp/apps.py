from django.apps import AppConfig

class InventoryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InventoryApp'

    def ready(self):
        import InventoryApp.signals  # make sure this matches your app name


#class AccountsConfig(AppConfig):
    #default_auto_field = 'django.db.models.BigAutoField'
    #name = 'accounts'

  #  def ready(self):
       # import accounts.signals  # 👈 import



'''
from django.apps import AppConfig


class InventoryappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'InventoryApp'

'''