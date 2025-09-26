from django.db import models
from django.contrib.auth.models import User

from Data.models import Country, State, City

# Create your models here.
class RegisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=12)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class ImageCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=15)

class WallImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/wall-images")

class ModelImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/model-images")
    image_category = models.ForeignKey(ImageCategories, on_delete=models.CASCADE)
    wall_images = models.ManyToManyField(WallImage, through='ModelImageHasWallImage')

class ModelImageHasWallImage(models.Model):
    id = models.AutoField(primary_key=True)
    wall_image = models.ForeignKey(WallImage, on_delete=models.CASCADE, null=True)
    model_image = models.ForeignKey(ModelImage, on_delete=models.CASCADE, null=True)


class RequestStatus(models.Model):
    id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=20)


class PaintRequest(models.Model):
    id = models.AutoField(primary_key=True)
    wall_image = models.ForeignKey(WallImage, on_delete=models.CASCADE, null=True)
    model_image = models.ForeignKey(ModelImage, on_delete=models.CASCADE, null=True, blank=True)
    request_status = models.ForeignKey(RequestStatus, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class UserSelectedImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/user-selected-images")
    paintRequest = models.ForeignKey(PaintRequest, on_delete=models.CASCADE, null=True)
