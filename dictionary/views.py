from django.shortcuts import render
from django.http import JsonResponse
from http import HTTPStatus
import requests

# Create your views here.

# Search request handler
def search(request):
    # Check if request is valied
    if request.method == 'GET':
        api_key = "c6f0f020-6846-46e7-bcc6-3fab213e84c8"
        query = request.GET.get('q')
        # Check if syntax is correct
        if query:
            response = requests.get(f"https://www.dictionaryapi.com/api/v3/references/collegiate/json/{query}?key={api_key}")
            # Check if request success
            if response.status_code == HTTPStatus.OK:
                response_status = HTTPStatus.OK
                response_json = response.json()
                # Check if word was found
                if len(response_json) == 0:
                    return JsonResponse({'error':'Word was not found.'}, status=404)
                
                if not "meta" in response_json[0]:  
                    response_status = HTTPStatus.PARTIAL_CONTENT

                return JsonResponse(response_json, status=response_status, safe=False)
            
            return JsonResponse({'error':'Request failed.'}, status=response.status_code)
        
        return JsonResponse({'error':'Parameter is missing.'}, status=400)
    
    return JsonResponse({'error':'Invalid request.'}, status=400) 
