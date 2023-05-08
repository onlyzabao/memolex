from dictionary.api import WordsAPI
import random
import math

class Test:
    def spelling_test_generate(word, progress):
        question = {}
        definition = ""

        results = WordsAPI.get(word, type="definitions")
        if results:
            definitionNum = len(results["definitions"])
            definition = results["definitions"][math.floor((definitionNum * progress) / 100)]

        question = {"text":definition["definition"], "key":word, "coeff": definitionNum}

        return question
    
    def definition_test_generate(word, progress):
        
        return
    
    def synonym_test_generate(word, progress):
        return