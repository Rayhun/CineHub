from __future__ import annotations

from typing import Iterable

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm
from .models import Category, Language, Movie


def home(request):
    languages = Language.objects.filter(is_active=True).order_by("name")
    trending_movies = (
        Movie.objects.filter(is_trending=True)
        .prefetch_related("categories", "languages")
        .order_by("-release_date", "-created_at")[:8]
    )
    latest_movies = (
        Movie.objects.all()
        .prefetch_related("categories", "languages")
        .order_by("-release_date", "-created_at")[:12]
    )

    context = {
        "active_page": "home",
        "languages": languages,
        "trending_movies": trending_movies,
        "latest_movies": latest_movies,
    }
    return render(request, "index.html", context)


def movie_detail(request, slug: str):
    movie = get_object_or_404(
        Movie.objects.prefetch_related("categories", "comments", "languages"),
        slug=slug,
    )
    related_movies = (
        Movie.objects.filter(categories__in=movie.categories.all())
        .exclude(pk=movie.pk)
        .distinct()
        .prefetch_related("languages")
        .order_by("-release_date", "-created_at")[:8]
    )
    comments = movie.comments.filter(is_approved=True)

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.movie = movie
            new_comment.save()
            messages.success(request, "Thanks for sharing your thoughts!")
            return redirect(f"{movie.get_absolute_url()}#comments")
        messages.error(request, "Please correct the errors below.")
    else:
        comment_form = CommentForm()

    context = {
        "active_page": "details",
        "movie": movie,
        "related_movies": related_movies,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, "movie-details.html", context)


def movie_download(request, slug: str):
    movie = get_object_or_404(Movie.objects.prefetch_related("languages"), slug=slug)

    context = {
        "active_page": "download",
        "movie": movie,
        "quality_options": movie.get_download_options(),
        "server_options": movie.get_server_options(),
    }
    return render(request, "download.html", context)


def movie_search(request):
    movies = Movie.objects.all().prefetch_related("categories", "languages")
    query = request.GET.get("q", "").strip()
    if query:
        movies = movies.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(tagline__icontains=query)
        )

    category_slugs = request.GET.getlist("categories")
    if category_slugs:
        movies = movies.filter(categories__slug__in=category_slugs).distinct()

    language_slugs = request.GET.getlist("languages")
    if language_slugs:
        movies = movies.filter(languages__slug__in=language_slugs).distinct()

    active_year = request.GET.get("year", "").strip()
    if active_year:
        if "-" in active_year:
            start_year, end_year = (int(value) for value in active_year.split("-", 1))
            movies = movies.filter(release_year__gte=start_year, release_year__lte=end_year)
        else:
            movies = movies.filter(release_year=int(active_year))

    active_qualities = request.GET.getlist("qualities")
    if active_qualities:
        movies = movies.filter(quality__in=active_qualities)

    active_sort = request.GET.get("sort", "latest")
    sort_mapping = {
        "latest": ("-release_date", "-created_at"),
        "trending": ("-is_trending", "-release_date"),
        "rating-high": ("-rating", "-release_date"),
        "rating-low": ("rating", "-release_date"),
        "name-asc": ("title",),
        "name-desc": ("-title",),
    }
    order_by_fields: Iterable[str] = sort_mapping.get(active_sort, ("-release_date", "-created_at"))
    movies = movies.order_by(*order_by_fields)

    categories = Category.objects.all()
    available_languages = Language.objects.all()
    quality_choices = Movie.QUALITY_CHOICES
    year_choices = sorted(
        set(Movie.objects.values_list("release_year", flat=True)),
        reverse=True,
    )

    context = {
        "active_page": "search",
        "query": query,
        "movies": movies,
        "categories": categories,
        "languages": available_languages,
        "quality_choices": quality_choices,
        "year_choices": year_choices,
        "sort_options": [
            ("latest", "Latest"),
            ("trending", "Trending"),
            ("rating-high", "Rating (High to Low)"),
            ("rating-low", "Rating (Low to High)"),
            ("name-asc", "Name (A-Z)"),
            ("name-desc", "Name (Z-A)"),
        ],
        "active_categories": category_slugs,
        "active_languages": language_slugs,
        "active_qualities": active_qualities,
        "active_year": active_year,
        "active_sort": active_sort,
    }
    return render(request, "search.html", context)
