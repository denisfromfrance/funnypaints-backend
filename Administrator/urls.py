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

    path("category/delete", views.delete_category),
    path("size/delete", views.delete_size),
    path("category/rename", views.rename_category),
    path("category/model/delete", views.delete_model),
    path("category/model/change", views.change_model),

    # path("preview-images/add", views.add_preview_image),
    path("preview-images/get", views.get_preview_image),
    path("preview-images/delete", views.delete_preview_image),

    path("product/variations", views.get_product_variations),
    path("product/variations/add", views.add_product_variation),
    path("product/variations/delete", views.delete_product_variation),

    path("suits/add", views.add_suits),

    path("pages/home/update", views.update_home_page),
    path("pages/home/information/get", views.get_home_page_information),
]