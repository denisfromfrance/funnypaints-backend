from django.urls import path
from . import views


urlpatterns = [
    path("categories", views.get_categories),
    path("painting-status", views.get_painting_status),
    path("location-data", views.get_location_data),
    path("sizes", views.get_painting_sizes),
    path("sizes/add", views.add_painting_size),
    path("suits", views.get_suits),
]