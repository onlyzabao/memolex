from dictionary.api import WordsAPI
from random_word import Wordnik
import math

class Test:
    def generate(level, word, progress):
        question = {}
        
        if level == 1:
            results = WordsAPI.get(word, type="definitions")
            if results:
                definitionNum = len(results["definitions"])
                definition = results["definitions"][math.floor((definitionNum * progress) / 100)]["definition"]

                question["text"] = definition
                question["key"] = word
                question["coeff"] = definitionNum
            else:
                question["error"] = "Error create test. Couldn't get word's definition."

        elif level == 2:
            question["text"] = word

            results = WordsAPI.get(word, type="synonyms")
            if results:
                synonymNum = len(results["synonyms"])
                synonym = results["synonyms"][math.floor((synonymNum * progress) / 100)]

                question["key"] = synonym
                question["coeff"] = synonymNum
            else:
                question["key"] = "This word doesn't have any synonyms."
                question["coeff"] = 1

            while True:
                choices = Wordnik().get_random_words(limit=3)
                if isinstance(choices, list):
                    break
                
            choices.append(question["key"])
            question["choices"] = choices

        return question
