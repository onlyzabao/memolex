from django.urls import path
from .views import (
    PackageListView, 
    PackageDetailView, 
    PackageCreateView, 
    PackageUpdateView,
    PackageDeleteView,
    AddWordView,
    PackageReviewView,
    TestGenerateView,
    QuestionDisplayView
)

app_name = "workspace"
urlpatterns = [
    path("", PackageListView.as_view(), name="package_list"),
    path("package/<int:pk>/", PackageDetailView.as_view(), name="package_detail"),
    path("package/create/", PackageCreateView.as_view(), name="package_create"),
    path("package/update/<int:pk>/", PackageUpdateView.as_view(), name="package_update"),
    path("package/delete/", PackageDeleteView.as_view(), name="package_delete"),
    path("package/add-word/", AddWordView.as_view(), name="package_add_word"),
    path("package/review/<int:level>/<int:pk>/", PackageReviewView.as_view(), name="package_review"),
    path("package/review/test-generate/", TestGenerateView.as_view(), name="test_generate"),
    path("package/review/question-display/", QuestionDisplayView.as_view(), name="question_display")
]
