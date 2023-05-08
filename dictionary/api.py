import requests

class WordsAPI:
    @staticmethod
    def request(word, type):
        if type == "everything":
            type = ""

        KEY = "cf95cee5bamsh5a61f362b771fc3p14f9dfjsn1cfc7c3b88c6"
        url = f"https://wordsapiv1.p.rapidapi.com/words/{word}/{type}"

        headers = {
            "X-RapidAPI-Key": KEY,
            "X-RapidAPI-Host": "wordsapiv1.p.rapidapi.com"
        }

        return requests.request("GET", url, headers=headers)
    
    @staticmethod
    def clean_for_everything(data):
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
                    elif "all" in data["pronunciation"]:
                        results[pos]["pronunciation"] = data["pronunciation"]["all"]
                    else:
                        results[pos]["pronunciation"] = data["pronunciation"]
                
                definition = {}
                definition["key"] = i
                definition["text"] = data["results"][i]["definition"]
                if "examples" in data["results"][i]:
                    definition["examples"] = data["results"][i]["examples"]
                if "synonyms" in data["results"][i]:
                    definition["synonyms"] = data["results"][i]["synonyms"]
        
                results[pos]["definitions"].append(definition)

        return results

    @staticmethod
    def clean_for_definitions(data):
        results = {}
        if "definitions" in data:
            results["definitions"] = data["definitions"]

        return results

    @staticmethod
    def get(word, type="everything"):
        response = WordsAPI.request(word, type)
        results = {}
        if response.status_code == 200:
            data = response.json()
            if type == "everything":
                results = WordsAPI.clean_for_everything(data)
            elif type == "definitions":
                results = WordsAPI.clean_for_definitions(data)

        return results