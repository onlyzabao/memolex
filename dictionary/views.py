from django.shortcuts import render, redirect
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from workspace.models import Package
from .api import WordsAPI
from .models import Topic, Word
import enchant

# Create your views here.
class TopicListView(ListView):
    model = Topic
    context_object_name = "topics"
    template_name = "dictionary/topic_list.html"

class TopicDetailView(DetailView):
    model = Topic
    context_object_name = "topic"
    template_name = "dictionary/topic_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
                context["packages"] = Package.objects.filter(user=self.request.user)

        return context

class WordDetailView(View):
    def get(self, request):
        word = request.GET.get("word")
        dictionary = enchant.Dict("en_US")

        if word:
            if dictionary.check(word):
                results = WordsAPI.get(word)
                context = {"word": word}
                if len(results) != 0:
                    context["results"] = results
            else:
                suggestions = dictionary.suggest(word)
                context = {"word": word, "suggestions": suggestions}

            if request.user.is_authenticated:
                context["packages"] = Package.objects.filter(user=request.user)
            
            return render(request, "dictionary/word_detail.html", context)

        return redirect("home")
