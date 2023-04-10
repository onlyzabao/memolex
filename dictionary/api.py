import requests

# TODO: Interface

def get_from_WordsAPI(word, type=""):
    KEY = "cf95cee5bamsh5a61f362b771fc3p14f9dfjsn1cfc7c3b88c6"
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/{type}"

    headers = {
        "X-RapidAPI-Key": KEY,
        "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
    }

    return requests.request("GET", url, headers=headers)