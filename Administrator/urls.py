from django.urls import path
from . import views


urlpatterns = [
    path("get-painting-requests", views.get_painting_requests),
    path("users", views.get_user_list),
    path("change-painting-request-status", views.change_painting_request_status),
    path("get-images-pf-categories", views.get_images_of_categories),
    path("category/add", views.add_new_category),
    path("model-images/add", views.add_model_images),
    path("wall-images/add", views.add_wall_images),
    path("wall-images/get", views.get_wall_images),
    path("painting-requests", views.get_all_painting_requests),
]