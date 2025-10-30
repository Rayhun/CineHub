from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import FormView

from payments.models import Plan, Subscription

from .forms import (
    AccountDeleteForm,
    PlanSelectionForm,
    PasswordUpdateForm,
    ProfileForm,
    SignUpForm,
    StyledAuthenticationForm,
    UserDetailsForm,
)
from .models import DownloadHistory, FavoriteMovie, UserProfile


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
            "profile": profile,
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
            "profile": profile,
            "active_page": "profile",
        }
        return render(request, self.template_name, context)


class AccountSettingsView(LoginRequiredMixin, View):
    template_name = "accounts/settings.html"

    def get(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        context = {
            "password_form": PasswordUpdateForm(user=request.user),
            "delete_form": AccountDeleteForm(),
            "profile": request.user.profile,
            "active_page": "settings",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        if "change_password" in request.POST:
            password_form = PasswordUpdateForm(user=request.user, data=request.POST)
            delete_form = AccountDeleteForm()
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Your password has been updated.")
                return redirect("core:settings")
            context = {
                "password_form": password_form,
                "delete_form": delete_form,
                "profile": request.user.profile,
                "active_page": "settings",
            }
            return render(request, self.template_name, context)

        if "delete_account" in request.POST:
            delete_form = AccountDeleteForm(request.POST)
            password_form = PasswordUpdateForm(user=request.user)
            if delete_form.is_valid():
                user = request.user
                user_email = user.email or user.username
                logout(request)
                user.delete()
                messages.success(request, f"Account for {user_email} has been deleted.")
                return redirect("movies:home")
            context = {
                "password_form": password_form,
                "delete_form": delete_form,
                "profile": request.user.profile,
                "active_page": "settings",
            }
            return render(request, self.template_name, context)

        return redirect("core:settings")


class AccountSubscriptionView(LoginRequiredMixin, View):
    template_name = "accounts/subscription.html"

    def get(self, request):
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        plan_form = PlanSelectionForm(initial={"plan": subscription.plan})
        context = {
            "subscription": subscription,
            "profile": profile,
            "plan_form": plan_form,
            "plans": Plan.objects.filter(is_active=True),
            "active_page": "subscription",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        action = request.POST.get("action")
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        plan_form = PlanSelectionForm(initial={"plan": subscription.plan})

        if action == "change_plan":
            plan_form = PlanSelectionForm(request.POST)
            if plan_form.is_valid():
                new_plan = plan_form.cleaned_data["plan"]
                subscription.plan = new_plan
                if new_plan:
                    subscription.status = Subscription.Status.ACTIVE
                    subscription.renewal_date = timezone.now().date() + timezone.timedelta(days=30)
                    profile.current_plan = new_plan
                    profile.plan_status = "active"
                    profile.plan_renewal_date = subscription.renewal_date
                    messages.success(request, f"Your plan has been updated to {new_plan.title}.")
                else:
                    subscription.status = Subscription.Status.INACTIVE
                    subscription.renewal_date = None
                    profile.current_plan = None
                    profile.plan_status = "inactive"
                    profile.plan_renewal_date = None
                    messages.info(request, "Subscription removed. You can pick a new plan anytime.")
                subscription.save()
                profile.save()
                return redirect("core:subscription")
        elif action == "cancel_subscription":
            subscription.status = Subscription.Status.CANCELLED
            subscription.renewal_date = None
            profile.plan_status = "cancelled"
            profile.plan_renewal_date = None
            profile.save()
            subscription.save()
            messages.info(request, "Your subscription has been cancelled.")
            return redirect("core:subscription")

        context = {
            "subscription": subscription,
            "profile": profile,
            "plan_form": plan_form,
            "plans": Plan.objects.filter(is_active=True),
            "active_page": "subscription",
        }
        return render(request, self.template_name, context)


class DownloadHistoryView(LoginRequiredMixin, View):
    template_name = "accounts/download_history.html"

    def get(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        history = (
            DownloadHistory.objects.filter(user=request.user)
            .select_related("movie")
            .order_by("-downloaded_at")
        )
        context = {
            "downloads": history,
            "profile": request.user.profile,
            "active_page": "download_history",
        }
        return render(request, self.template_name, context)


class FavoritesView(LoginRequiredMixin, View):
    template_name = "accounts/favorites.html"

    def get(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        favorites = (
            FavoriteMovie.objects.filter(user=request.user)
            .select_related("movie")
            .order_by("-created_at")
        )
        context = {
            "favorites": favorites,
            "profile": request.user.profile,
            "active_page": "favorites",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        UserProfile.objects.get_or_create(user=request.user)
        movie_id = request.POST.get("movie_id")
        if movie_id:
            FavoriteMovie.objects.filter(user=request.user, movie_id=movie_id).delete()
            messages.info(request, "Movie removed from favourites.")
        return redirect("core:favorites")
