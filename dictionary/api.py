import requests

# TODO: Interface

KEY = "cf95cee5bamsh5a61f362b771fc3p14f9dfjsn1cfc7c3b88c6"

def get(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"

    headers = {
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }

    return requests.request("GET", url, headers=headers).json()