from django.urls import path
from .views import TopicListView, TopicDetailView, WordDetailView

app_name = "dictionary"
urlpatterns = [
    path("", TopicListView.as_view(), name="topic_list"),
    path("topic/<int:pk>/", TopicDetailView.as_view(), name="topic_detail"),
    path("detail/", WordDetailView.as_view(), name="word_detail")
]