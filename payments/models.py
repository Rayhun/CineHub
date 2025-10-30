from django.conf import settings
from django.db import models


class PlanFeature(models.Model):
    """Feature description that can be shown on a subscription plan."""

    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self) -> str:
        return self.name


class Plan(models.Model):
    """Subscription plan exposed on the pricing page."""

    title = models.CharField(max_length=100)
    subtitle = models.CharField(max_length=255, blank=True)
    currency = models.CharField(max_length=5, default="$")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    billing_period = models.CharField(max_length=50, default="/month")
    badge_text = models.CharField(max_length=50, blank=True)
    button_text = models.CharField(max_length=50, default="Choose Plan")
    is_active = models.BooleanField(default=True)
    is_recommended = models.BooleanField(default=False)
    features = models.ManyToManyField(
        PlanFeature,
        through="PlanFeatureAssignment",
        related_name="plans",
        blank=True,
    )
    display_order = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("display_order", "price")

    def __str__(self) -> str:
        return self.title


class PlanFeatureAssignment(models.Model):
    """Through model to mark whether a feature is available on a plan."""

    plan = models.ForeignKey(
        Plan, related_name="feature_assignments", on_delete=models.CASCADE
    )
    feature = models.ForeignKey(
        PlanFeature, related_name="plan_assignments", on_delete=models.CASCADE
    )
    is_included = models.BooleanField(default=True)
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")
        unique_together = ("plan", "feature")

    def __str__(self) -> str:
        return f"{self.plan} - {self.feature} ({'Yes' if self.is_included else 'No'})"


class FrequentlyQuestionAndAnswer(models.Model):
    """FAQ content displayed under the plans."""

    question = models.CharField(max_length=200)
    answer = models.TextField()
    display_order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")

    def __str__(self) -> str:
        return self.question


class Subscription(models.Model):
    """Represents a user's active or previous subscription to a plan."""

    class Status(models.TextChoices):
        INACTIVE = ("inactive", "Inactive")
        ACTIVE = ("active", "Active")
        CANCELLED = ("cancelled", "Cancelled")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name="subscription", on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        Plan, related_name="subscriptions", null=True, blank=True, on_delete=models.SET_NULL
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.INACTIVE)
    renewal_date = models.DateField(blank=True, null=True)
    price_override = models.DecimalField(
        max_digits=8, decimal_places=2, blank=True, null=True, help_text="Optional override price for promotions."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return f"{self.user} subscription"

    @property
    def price(self):
        if self.price_override is not None:
            return self.price_override
        if self.plan:
            return self.plan.price
        return None
