from django.urls import reverse_lazy
from django.db.models import F
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.views.generic.list import ListView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignupForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile


# Create your views here.
class MemoLexLoginView(LoginView):
    template_name = "community/login.html"
    redirect_authenticated_user = False

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))


class MemoLexSignupView(FormView):
    template_name = "community/signup.html"
    redirect_authenticated_user = True
    form_class = SignupForm

    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()

        if user:
            login(self.request, user)

        return super(MemoLexSignupView, self).form_valid(form)


class MemoLexProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

        context = {"user_form": user_form, "profile_form": profile_form}

        return render(request, "community/profile.html", context)

    def post(self, request):
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile
        )

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            messages.success(request, "Your profile has been updated successfully")

            return redirect("community:profile")
        else:
            context = {"user_form": user_form, "profile_form": profile_form}
            messages.error(request, "Error updating you profile")

            return render(request, "community/profile.html", context)
        
class UserListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "users"
    template_name = "community/user_list.html"
    paginate_by = 15

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = get_object_or_404(User, pk=self.request.user.id)
        profile = get_object_or_404(Profile, user=user)

        context["meta"] = {
            "user": user,
            "profile": profile
        }

        return context

    def get_queryset(self):
        base_qs = super(UserListView, self).get_queryset()
        ordered_qs = base_qs.annotate(score=F('profile__score')).order_by('-score').select_related('profile')
        return ordered_qs
