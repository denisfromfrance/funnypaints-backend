from django.urls import path
from . import views


urlpatterns = [
    path("sign-in", views.login_user),
    path("sign-up", views.register_user),
    path("admin/sign-up", views.sign_in_admin),
]