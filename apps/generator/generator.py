import random


class TokenGenerator:
    def __init__(self, corpus):
        self.corpus = corpus

    def generate(self, word):
        predict_dict = self.corpus[word]
        predict_list = []
        for key, value in predict_dict.items():
            temp = [key] * value
            predict_list.extend(temp)

        return random.choice(predict_list)
