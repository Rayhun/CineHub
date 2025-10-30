from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path("plan/", views.Subscription.as_view(), name="plan"),
]
