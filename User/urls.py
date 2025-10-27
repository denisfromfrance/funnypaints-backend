from django.urls import path
from . import views


urlpatterns = [
    path("profile/update", views.update_user_profile),
    path("profile/get-information", views.get_user_profile),
    path("profile/upload-profile-image", views.upload_user_profile_image),
    path("cart/add", views.add_item_to_cart),
    path("cart/clear", views.clear_cart),
    path("cart/items/get", views.get_items_in_cart),
]