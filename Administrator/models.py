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
    priority = models.IntegerField(default=0)
    category = models.CharField(max_length=100)

class SubCategory(models.Model):
    id = models.AutoField(primary_key=True)
    subcategory = models.CharField(max_length=100)
    main_category = models.ForeignKey(ImageCategories, on_delete=models.CASCADE)

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


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    company = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    billing_street_address = models.CharField(max_length=100)
    shipping_street_address = models.CharField(max_length=100)
    shipping_destination_type = models.CharField(max_length=50)
    post_code = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    province = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email_address = models.CharField(max_length=50)
    notes = models.CharField(max_length=500)
    payment_status = models.IntegerField(default=-1)
    user_selected_image = models.FileField(upload_to="users/requests/images", null=True, blank=True)


class UserSelectedImage(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.FileField(upload_to="images/user-selected-images")
    paintRequest = models.ForeignKey(
        PaintRequest, on_delete=models.CASCADE, null=True)


class PaintRequestHasProductVariantHasSize(models.Model):
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(ModelImage, on_delete=models.CASCADE)
    wallImage = models.ForeignKey(WallImage, on_delete=models.CASCADE)
    variation = models.ForeignKey(ProductVariation, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user_uploaded_image = models.ForeignKey(UserSelectedImage, on_delete=models.CASCADE, null=True)

class Suit(models.Model):
    id = models.AutoField(primary_key=True)
    suit_image = models.FileField(upload_to='images/suits')


class HomePageData(models.Model):
    id = models.AutoField(primary_key=True)
    mainHeading = models.CharField(max_length=50)
    subheading = models.CharField(max_length=100)
    heroImage = models.FileField(upload_to='image/pages/home/hero-section-image')

class TempUploads(models.Model):
    id = models.AutoField(primary_key=True)
    file = models.FileField(upload_to="tempUploads")

class Invoice(models.Model):
    id = models.AutoField(primary_key=True)
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField(null=True)
    payment_date = models.DateField(null=True)
    currency = models.CharField(max_length=5, null=True)
    amount = models.FloatField(default=0)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

