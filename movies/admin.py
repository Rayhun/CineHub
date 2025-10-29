from django.contrib import admin

from .models import Category, Comment, Language, Movie


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_at")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("title", "release_year", "display_languages", "is_trending", "is_featured")
    list_filter = ("is_trending", "is_featured", "categories", "languages")
    search_fields = ("title", "tagline", "description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("categories", "languages")
    readonly_fields = ("created_at", "updated_at")

    @admin.display(description="Languages")
    def display_languages(self, obj):
        names = [language.name for language in obj.languages.all()]
        return ", ".join(names) if names else "—"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "movie", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    search_fields = ("name", "body", "movie__title")
    autocomplete_fields = ("movie",)
