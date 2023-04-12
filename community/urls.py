from django.urls import path
from django.urls import reverse_lazy
from django.contrib.auth.views import (
    LogoutView, 
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)
from .views import MemoLexLoginView, MemoLexSignupView

app_name = "community"
urlpatterns = [
    path("login/", MemoLexLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="dictionary:index"), name="logout"),
    path("signin/", MemoLexSignupView.as_view(), name="signup"),
    path("password-reset/", 
        PasswordResetView.as_view(
            template_name="community/password_reset.html", 
            email_template_name="community/password_reset_email.html",
            success_url=reverse_lazy("community:password_reset_done")
        ), 
        name="password-reset"
    ),
    path("password-reset/done/", 
        PasswordResetDoneView.as_view(
            template_name="community/password_reset_done.html"
        ), 
        name="password_reset_done"
    ),
    path("password-reset/confirm/<uidb64>/<token>/", 
        PasswordResetConfirmView.as_view(
            template_name="community/password_reset_confirm.html",
            success_url=reverse_lazy("community:password_reset_complete")
        ),
        name="password_reset_confirm"
    ),
    path("password-reset/complete/", 
        PasswordResetCompleteView.as_view(
            template_name="community/password_reset_complete.html"
        ),
        name="password_reset_complete"
    ),
]
