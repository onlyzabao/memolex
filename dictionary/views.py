from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from .api import WordsAPI


# Create your views here.
class TopicListView(TemplateView):
    template_name = "dictionary/topic_list.html"


class WordDetailView(View):
    def get(self, request):
        word = request.GET.get("word")
        if word:
            results = WordsAPI.get(word)

            context = {"word": word, "results": results}

            return render(request, "dictionary/word_detail.html", context)

        return redirect("home")
