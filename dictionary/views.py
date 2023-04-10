from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.http import JsonResponse
from . import api

# Create your views here.
def index(request):
    return HttpResponse("Index")

def detail(request, word):
    data = api.get(word)

    results = {}
    if "results" in data:
        for i in range(0, len(data["results"])):
            pos = data["results"][i]["partOfSpeech"]
            if pos not in results:
                results[pos] = {
                    "pronunciation": "",
                    "definitions": []
                }

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

    context = {
        "word": word,
        "results": results
    }
    template = loader.get_template("dictionary/detail.html")

    return HttpResponse(template.render(context, request))