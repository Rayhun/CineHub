from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Category(models.Model):
    """High level grouping for movies e.g. Bangla, Anime, Action."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Language(models.Model):
    """Represents a spoken language available for movies."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Movie(models.Model):
    """Represents a single movie entry rendered across the CineHub templates."""

    QUALITY_CHOICES = (
        ("SD", "SD (480p)"),
        ("HD", "HD (720p)"),
        ("FHD", "Full HD (1080p)"),
        ("UHD", "4K Ultra HD"),
    )

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    tagline = models.CharField(max_length=255, blank=True)
    description = models.TextField()
    poster_url = models.URLField(blank=True)
    banner_url = models.URLField(blank=True)
    release_year = models.PositiveSmallIntegerField()
    release_date = models.DateField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    imdb_rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        blank=True,
        null=True,
        help_text="Optional IMDb rating",
    )
    download_url = models.URLField(blank=True)
    download_options = models.JSONField(default=list, blank=True)
    server_options = models.JSONField(default=list, blank=True)
    trailer_url = models.URLField(blank=True)
    is_trending = models.BooleanField(default=False)
    is_featured = models.BooleanField(
        default=False,
        help_text="Marks movie as a highlighted/latest entry on the home page",
    )
    categories = models.ManyToManyField(Category, related_name="movies", blank=True)
    languages = models.ManyToManyField(Language, related_name="movies", blank=True)
    screenshots = models.JSONField(default=list, blank=True)
    quality = models.CharField(max_length=10, choices=QUALITY_CHOICES, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-release_date", "-created_at")

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("movies:movie_detail", kwargs={"slug": self.slug})

    def get_download_url(self) -> str:
        if self.download_url:
            return self.download_url
        return reverse("movies:movie_download", kwargs={"slug": self.slug})

    def get_download_options(self) -> list[dict]:
        if self.download_options:
            return self.download_options
        # Sensible defaults keep the download page populated until real data is provided
        return [
            {
                "label": "Full HD (1080p)",
                "badge": "Popular",
                "resolution": "1920 x 1080",
                "file_size": "2-4 GB",
                "file_format": "MP4 / MKV",
                "bitrate": "8-12 Mbps",
                "download_url": self.get_download_url(),
                "cta_text": "Download 1080p",
            }
        ]

    def get_server_options(self) -> list[dict]:
        if self.server_options:
            return self.server_options
        return [
            {
                "name": "Server 1 - Direct Download",
                "badge": "Fast",
                "badge_variant": "success",
                "description": "Direct download link - No waiting",
                "speed": "10 MB/s",
                "active_users": "1,234",
                "url": self.get_download_url(),
                "cta_text": "Select Server 1",
            }
        ]

    def language_names(self) -> list[str]:
        return [language.name for language in self.languages.all()]


class Comment(models.Model):
    """Visitor feedback tied to a movie detail page."""

    movie = models.ForeignKey(Movie, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    email = models.EmailField(blank=True)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.name} on {self.movie}"
