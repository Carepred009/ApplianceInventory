from tkinter.constants import CASCADE
#WE need this model to access the right user and use the Profile model
from django.contrib.auth.models import User
from django.db import models
from django.db.models import AutoField

# Create your models here.
class Position(models.Model):
    position_id  = models.AutoField(primary_key = True)
    position  =  models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.position

class Department(models.Model):
    department_id = models.AutoField(primary_key = True)
    department = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.department

class Profile(models.Model):
    profile_id = models.AutoField(primary_key = True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True,upload_to="images/")
    position = models.ForeignKey(Position, on_delete=models.CASCADE, null=True, blank=True)
    date_hire = models.DateTimeField(auto_now_add=False, blank=True,null=True)
    #We will create another model for this in the the future
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.user.username)







