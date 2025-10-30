from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView

from payments.models import Plan, Subscription

from .forms import ProfileForm, SignUpForm, StyledAuthenticationForm, UserDetailsForm
from .models import UserProfile


class SignUpView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignUpForm
    success_url = reverse_lazy("core:profile")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "signup"
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, "Welcome to CineHub! Your account has been created.")
        # Ensure the user has a subscription placeholder.
        Subscription.objects.get_or_create(user=user)
        return super().form_valid(form)


class CustomLoginView(LoginView):
    template_name = "accounts/login.html"
    authentication_form = StyledAuthenticationForm
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_page"] = "login"
        return context

    def get_success_url(self):
        return self.get_redirect_url() or reverse_lazy("core:profile")


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("core:login")


class ProfileView(LoginRequiredMixin, View):
    template_name = "accounts/profile.html"

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserDetailsForm(instance=request.user)
        profile_form = ProfileForm(instance=profile)
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        plans = Plan.objects.filter(is_active=True)
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "subscription": subscription,
            "plans": plans,
            "active_page": "profile",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        user_form = UserDetailsForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile = profile_form.save(commit=False)
            if profile.current_plan:
                profile.plan_status = "active"
            else:
                profile.plan_status = "inactive"
            profile.save()

            subscription, _ = Subscription.objects.get_or_create(user=request.user)
            subscription.plan = profile.current_plan
            subscription.status = (
                Subscription.Status.ACTIVE if profile.current_plan else Subscription.Status.INACTIVE
            )
            subscription.renewal_date = profile.plan_renewal_date
            subscription.save()

            messages.success(request, "Your profile has been updated.")
            return redirect("core:profile")

        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        plans = Plan.objects.filter(is_active=True)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
            "subscription": subscription,
            "plans": plans,
            "active_page": "profile",
        }
        return render(request, self.template_name, context)


class AccountSettings(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    def get(self, request):
        return render(request, self.template_name)


class SubscriptionView(LoginRequiredMixin, View):
    template_name = "accounts/subscription.html"

    def get(self, request):
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        plans = Plan.objects.filter(is_active=True)
        context = {
            "subscription": subscription,
            "plans": plans,
            "active_page": "subscription",
        }
        return render(request, self.template_name, context)


class DownloadHistoryView(LoginRequiredMixin, View):
    template_name = "accounts/download_history.html"

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        context = {
            "active_page": "download_history",
        }
        return render(request, self.template_name, context)


class FavoritesViews(LoginRequiredMixin, View):
    template_name = "accounts/favorites.html"

    def get(self, request):
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        context = {
            "active_page": "favorites",
        }
        return render(request, self.template_name, context)
