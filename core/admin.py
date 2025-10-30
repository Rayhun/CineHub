from django.contrib import admin

from .models import DownloadHistory, FavoriteMovie, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone_number", "plan_status", "current_plan")
    list_filter = ("plan_status", "current_plan")
    search_fields = ("user__username", "user__email", "phone_number")


@admin.register(DownloadHistory)
class DownloadHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "downloaded_at", "quality")
    list_filter = ("quality", "downloaded_at")
    search_fields = ("user__username", "movie__title")


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created_at")
    search_fields = ("user__username", "movie__title")
