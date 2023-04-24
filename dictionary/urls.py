from django.urls import path
from .views import TopicListView, WordDetailView

app_name = "dictionary"
urlpatterns = [
    path("", TopicListView.as_view(), name="topic_list"),
    path("detail/", WordDetailView.as_view(), name="word_detail")
]