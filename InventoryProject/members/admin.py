from django.contrib import admin

from .models import Profile, Position, Department
# Register your models here.

#Afterh this go to settings.py url import this class. Make sure to register in to Installed APP
class MembersAdminArea(admin.AdminSite):
    site_header = "Member Admin Area" #This will be displayed when you log in in the admin

members_site = MembersAdminArea(name='MembersAdmin')

members_site.register(Profile)
members_site.register(Position)
members_site.register(Department)

#this will change to members_site, now both default admin and custom admin has the models
admin.site.register(Profile)
admin.site.register(Position)
admin.site.register(Department)


