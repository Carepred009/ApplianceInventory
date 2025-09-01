
#WE need this model to access the right user and use the Profile model
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Profile(models.Model):
    profile_id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True,upload_to="images/")
    position = models.CharField(max_length=255)
    date_hire = models.DateTimeField(auto_now_add=False, blank=True,null=True)
    #We will create another model for this in the the future
    department = models.CharField(max_length=255)




