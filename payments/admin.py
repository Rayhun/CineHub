from django.contrib import admin

from .models import (
    FrequentlyQuestionAndAnswer,
    Plan,
    PlanFeature,
    PlanFeatureAssignment,
    Subscription,
)


class PlanFeatureAssignmentInline(admin.TabularInline):
    model = PlanFeatureAssignment
    extra = 1


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "billing_period", "is_active", "is_recommended")
    list_filter = ("is_active", "is_recommended")
    search_fields = ("title", "subtitle")
    inlines = (PlanFeatureAssignmentInline,)
    ordering = ("display_order", "price")


@admin.register(PlanFeature)
class PlanFeatureAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(FrequentlyQuestionAndAnswer)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "display_order")
    ordering = ("display_order",)
    search_fields = ("question",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "renewal_date")
    list_filter = ("status", "plan")
    search_fields = ("user__username", "user__email")
