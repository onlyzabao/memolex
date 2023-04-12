from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MemoLexLoginView

app_name = "community"
urlpatterns = [
    path("login/", MemoLexLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="dictionary:index"), name="logout")
]
