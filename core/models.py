from django.conf import settings
from django.db import models
from django.utils import timezone

from payments.models import Plan


def user_avatar_upload_path(instance, filename):
    return f"avatars/{instance.user_id}/{filename}"


class UserProfile(models.Model):
    """Additional information stored for each user."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE
    )
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to=user_avatar_upload_path, blank=True, null=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    promo_notifications = models.BooleanField(default=True)
    current_plan = models.ForeignKey(
        Plan, related_name="profiles", on_delete=models.SET_NULL, null=True, blank=True
    )
    plan_status = models.CharField(
        max_length=20,
        choices=(
            ("inactive", "Inactive"),
            ("active", "Active"),
            ("cancelled", "Cancelled"),
        ),
        default="inactive",
    )
    plan_renewal_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("user__username",)

    def __str__(self) -> str:
        return f"Profile for {self.user}"

    def activate_trial(self):
        """Simple helper to set a default trial subscription on signup."""
        if not self.current_plan:
            return
        self.plan_status = "active"
        if not self.plan_renewal_date:
            self.plan_renewal_date = timezone.now().date() + timezone.timedelta(days=30)
        self.save(update_fields=["plan_status", "plan_renewal_date"])


class DownloadHistory(models.Model):
    """Tracks what a user has downloaded from the site."""

    QUALITY_CHOICES = (
        ("SD", "SD (480p)"),
        ("HD", "HD (720p)"),
        ("FHD", "Full HD (1080p)"),
        ("UHD", "4K Ultra HD"),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="download_history", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        "movies.Movie", related_name="downloads", on_delete=models.CASCADE
    )
    downloaded_at = models.DateTimeField(default=timezone.now)
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, blank=True)
    file_size = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ("-downloaded_at",)

    def __str__(self) -> str:
        return f"{self.user} downloaded {self.movie}"


class FavoriteMovie(models.Model):
    """Stores the movies a user has marked as favourite."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="favorite_movies", on_delete=models.CASCADE
    )
    movie = models.ForeignKey(
        "movies.Movie", related_name="favorited_by", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)
        unique_together = ("user", "movie")

    def __str__(self) -> str:
        return f"{self.user} likes {self.movie}"
