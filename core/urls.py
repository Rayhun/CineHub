from django.urls import path

from .views import (
    AccountSettingsView,
    AccountSubscriptionView,
    CustomLoginView,
    CustomLogoutView,
    DownloadHistoryView,
    FavoritesView,
    ProfileView,
    SignUpView,
)

app_name = "core"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", AccountSettingsView.as_view(), name="settings"),
    path("subscription/", AccountSubscriptionView.as_view(), name="subscription"),
    path("downloads/", DownloadHistoryView.as_view(), name="download_history"),
    path("favorites/", FavoritesView.as_view(), name="favorites"),
]
