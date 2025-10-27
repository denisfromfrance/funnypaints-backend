from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from Data.models import Country, State, City, Size

# Create your models here.
class RegisteredUser(models.Model):
    id = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=12)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    street = models.CharField(max_length=100, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profileImage = models.FileField(upload_to='user/profile-images', null=True)


class ImageCategories(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=100)

class WallImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/wall-images")


class ProductVariation(models.Model):
    id = models.AutoField(primary_key=True)
    variation = models.CharField(max_length=50)
    small = models.FloatField(default=0)
    medium = models.FloatField(default=0)
    large = models.FloatField(default=0)
    sizes = models.ManyToManyField(Size, through="ProductVariantHasSize")


class ModelImage(models.Model):
    id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=20)
    image = models.FileField(upload_to="images/model-images")
    image_category = models.ForeignKey(ImageCategories, on_delete=models.CASCADE)
    wall_images = models.ManyToManyField(WallImage, through='ModelImageHasWallImage')
    small_size_price = models.FloatField(default=0)
    medium_size_price = models.FloatField(default=0)
    large_size_price = models.FloatField(default=0)
    small_size_oil_paint_on_canvas_price = models.FloatField(default=0)
    medium_size_oil_paint_on_canvas_price = models.FloatField(default=0)
    large_size_oil_paint_on_canvas_price = models.FloatField(default=0)
    small_size_print_on_metal = models.FloatField(default=0)
    medium_size_print_on_metal = models.FloatField(default=0)
    large_size_print_on_metal = models.FloatField(default=0)
    small_size_print_on_paper = models.FloatField(default=0)
    medium_size_print_on_paper = models.FloatField(default=0)
    large_size_print_on_paper = models.FloatField(default=0)


class ProductVariantHasSize(models.Model):
    id = models.AutoField(primary_key=True)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.FloatField(default=0)
    product = models.ForeignKey(ModelImage, on_delete=models.CASCADE)


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
    datetime = models.DateTimeField(default=timezone.datetime.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


class UserSelectedImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/user-selected-images")
    paintRequest = models.ForeignKey(PaintRequest, on_delete=models.CASCADE, null=True)



class Suit(models.Model):
    id = models.AutoField(primary_key=True)
    suit_image = models.FileField(upload_to='images/suits')


class HomePageData(models.Model):
    id = models.AutoField(primary_key=True)
    mainHeading = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100)
    heroImage = models.FileField(upload_to='image/pages/home/hero-section-image')
