from django.shortcuts import render
from django.views import View
from .models import Plan


class Subscription(View):
    def get(self, request):
        plans = Plan.objects.filter(is_active=True)
        context = {"plans": plans}
        return render(request, "payments/subscription.html", context)
