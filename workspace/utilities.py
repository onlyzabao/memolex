import random
import math

class SpellingTest:
    def generate(words):
        questions = []
        for word in words:
            word_len = len(word.spelling)
            num_blanks =  math.ceil(word_len / 3)
            blank_indices = random.sample(range(word_len), num_blanks)
            key = word.spelling
            text = ""
            for i in range(word_len):
                if i in blank_indices:
                    text += "_"
                else:
                    text += word.spelling[i]
            questions.append({"text":text, "key":key})

        return questions