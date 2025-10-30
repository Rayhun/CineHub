from django.db.models import Prefetch
from django.views.generic import TemplateView

from .models import FrequentlyQuestionAndAnswer, Plan, PlanFeatureAssignment


class SubscriptionView(TemplateView):
    template_name = "payments/subscription.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plans = (
            Plan.objects.filter(is_active=True)
            .prefetch_related(
                Prefetch(
                    "feature_assignments",
                    queryset=PlanFeatureAssignment.objects.select_related("feature"),
                )
            )
            .order_by("display_order", "price")
        )
        faqs = FrequentlyQuestionAndAnswer.objects.all()
        context.update(
            {
                "plans": plans,
                "faqs": faqs,
                "active_page": "plan",
            }
        )
        return context
