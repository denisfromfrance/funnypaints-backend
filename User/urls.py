from django.urls import path
from . import views


urlpatterns = [
    path("profile/update", views.update_user_profile),
    path("profile/get-information", views.get_user_profile),
    path("profile/upload-profile-image", views.upload_user_profile_image),
]