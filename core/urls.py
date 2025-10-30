from django.urls import path

from .views import (
    CustomLoginView, CustomLogoutView, ProfileView, SignUpView,
    AccountSettings, SubscriptionView, DownloadHistoryView, FavoritesViews
)

app_name = "core"

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("settings/", AccountSettings.as_view(), name='settings'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path(
        'downloads-history/', DownloadHistoryView.as_view(),
        name='download_history'
    ),
    path('favorites/', FavoritesViews.as_view(), name='favorites'),
]
