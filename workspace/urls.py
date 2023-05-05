from django.urls import path
from .views import (
    PackageListView, 
    PackageDetailView, 
    PackageCreateView, 
    PackageUpdateView,
    PackageDeleteView,
    AddWordView,
    ReviewSpellingView
)

app_name = "workspace"
urlpatterns = [
    path("", PackageListView.as_view(), name="package_list"),
    path("package/<int:pk>/", PackageDetailView.as_view(), name="package_detail"),
    path("package/create/", PackageCreateView.as_view(), name="package_create"),
    path("package/update/<int:pk>/", PackageUpdateView.as_view(), name="package_update"),
    path("package/delete/<int:pk>/", PackageDeleteView.as_view(), name="package_delete"),
    path("package/add-word/", AddWordView.as_view(), name="package_add_word"),
    path("package/review/spelling/<int:pk>/", ReviewSpellingView.as_view(), name="package_review")
]
