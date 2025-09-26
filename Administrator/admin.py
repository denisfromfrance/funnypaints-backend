from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([ImageCategories, ModelImage, WallImage, RegisteredUser, UserSelectedImage, PaintRequest, RequestStatus])
