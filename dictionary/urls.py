from django.urls import path
from .views import TopicListView, detail

app_name = "dictionary"
urlpatterns = [
    path("", TopicListView.as_view(), name="topic_list"),
    path("detail/", detail, name="detail")
]