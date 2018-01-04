import random
from pymongo import MongoClient


class TokenGenerator:
    def __init__(self, collection):
        client = MongoClient('localhost', 27017)
        db = client.sample
        self.collection = db[collection]

    def generate(self, num_of_word=10):
        sentence = str()
        lim = self.collection.count() - 1
        random_id = random.randint(1, lim)
        # ランダムに最初のトークンを選ぶ
        document = self.collection.find().limit(-1).skip(random_id).next()
        token = document.get('this')
        for i in range(num_of_word):
            sentence += token
            token = self._generate_token(token)

        return sentence

    def _generate_token(self, token):
        document = self.collection.find_one({'this': token})
        probability_dict = document.get('next')
        probability_tokens = []
        for k, v in probability_dict.items():
            temp = [k] * v
            probability_tokens.extend(temp)

        return random.choice(probability_tokens)
