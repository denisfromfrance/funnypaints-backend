from django.urls import path
from . import views


urlpatterns = [
    path("request", views.request_art),
    path("pay", views.make_payment),
    path("payment/stripe/webhook", views.stripe_webhook),
]