from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.contrib.auth import login 
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render
from .forms import SignupForm

# Create your views here.
class MemoLexLoginView(LoginView):
    template_name = "community/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dictionary:index") # TODO: Redirect after successfully login
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))
    
class MemoLexSignupView(FormView):
    template_name = "community/signup.html"
    redirect_authenticated_user = True
    form_class = SignupForm

    success_url = reverse_lazy("dictionary:index")

    def form_valid(self, form):
        user = form.save()

        if user:
            login(self.request, user)

        return super(MemoLexSignupView, self).form_valid(form)