from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MyUser

# Register your models here.
admin.site.register(MyUser)