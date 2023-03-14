from django.shortcuts import render
from django.http import JsonResponse
from http import HTTPStatus
import requests

# Create your views here.
def get_word_data(word, key):
    response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={key}")
    return response.json()

def search(request):
    query = request.GET.get('q')
    if query:
        results = get_word_data(query, "c6f0f020-6846-46e7-bcc6-3fab213e84c8")
        return JsonResponse(results, safe=False)
    else:
        return render(request, 'search.html')
