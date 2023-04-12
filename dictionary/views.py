from django.shortcuts import render, redirect
from django.template import loader
from . import api

# Create your views here.
def index(request):
    return render(request, "dictionary/index.html")

def detail(request):
    if request.method == "GET":
        word = request.GET.get("word")
        data = api.get_from_WordsAPI(word).json()

        results = {}
        if "results" in data:
            for i in range(0, len(data["results"])):
                pos = data["results"][i]["partOfSpeech"]
                if pos not in results:
                    results[pos] = {
                        "pronunciation": "",
                        "definitions": []
                    }

                if "pronunciation" in data:
                    if pos in data["pronunciation"]:
                        results[pos]["pronunciation"] = data["pronunciation"][pos]
                    else:
                        results[pos]["pronunciation"] = data["pronunciation"]["all"]
                
                definition = {}
                definition["key"] = i
                definition["text"] = data["results"][i]["definition"]
                if "examples" in data["results"][i]:
                    definition["examples"] = data["results"][i]["examples"]
                if "synonyms" in data["results"][i]:
                    definition["synonyms"] = data["results"][i]["synonyms"]
        
                results[pos]["definitions"].append(definition)

        return render(request, "dictionary/detail.html", { "word": word, "results": results })
    
    return redirect("dictionary:index")