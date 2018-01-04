import sys
import random
from pymongo import MongoClient


class CorpusCreator:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.db = client.sample

    def _preprocess(self, string):
        if isinstance(string, str):
            tokens = string.split(' ')
        else:
            tokens = string
        return tokens

    def create_collection(self, collection, data):
        collection = self.db[collection]
        corpus = self.create(data)
        collection.insert_one(corpus)

    def create(self, input_data):
        corpus = {}
        tokens = self._preprocess(input_data)
        end = ['*END*']
        tokens.extend(end)
        for i, token in enumerate(tokens):
            if i == 0:
                corpus['*START*'] = {}
                corpus['*START*'][token] = 1
            if token == '*END*':
                break
            if token not in corpus.keys():
                corpus[token] = {}
                corpus[token][tokens[i + 1]] = 1
            else:
                if tokens[i + 1] not in corpus[token].keys():
                    corpus[token][tokens[i + 1]] = 1
                else:
                    corpus[token][tokens[i + 1]] += 1

        return corpus


