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
        definitions = []
        for result in results:
            if 'meta' in result and 'id' in result['meta']:
                definition = {
                    'word': result['meta']['id'],
                    'part_of_speech': result['fl'],
                    'definition': result['shortdef'][0],
                }
                if 'sseq' in result and result['sseq'][0][0][0] == 'sense':
                    examples = result['sseq'][0][0][1].get('examples')
                    if examples:
                        definition['examples'] = [example['t'] for example in examples]
                definitions.append(definition)
        return render(request, 'search.html', {'definitions': definitions, 'query': query})
    else:
        return render(request, 'search.html')
