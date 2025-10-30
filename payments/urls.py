from django.urls import path

from .views import SubscriptionView

app_name = "payments"

urlpatterns = [
    path("plan/", SubscriptionView.as_view(), name="plan"),
]
