from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import render

# Create your views here.
class MemoLexLoginView(LoginView):
    template_name = "community/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("dictionary:index") # TODO: Redirect after successfully login
    
    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password")
        return self.render_to_response(self.get_context_data(form=form))
    
