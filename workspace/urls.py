from django.urls import path
from .views import PackageListView, PackageDetailView, PackageCreateView, PackageUpdateView

app_name = "workspace"
urlpatterns = [
    path("", PackageListView.as_view(), name="package_list"),
    path("package/<int:pk>/", PackageDetailView.as_view(), name="package_detail"),
    path("package/create/", PackageCreateView.as_view(), name="package_create"),
    path("package/update/<int:pk>/", PackageUpdateView.as_view(), name="package_update")
]
