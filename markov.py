import sys
import random
from parser import MessageManager, CabochaParser


class CorpusCreator:
    def __init__(self):
        pass

    def _preprocess(self, string):
        if isinstance(string, str):
            tokens = sent.split(' ')
        else:
            tokens = string
        return tokens

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


if __name__ == '__main__':
    sent = 'One fish two fish red fish blue fish'
    path = 'data/デスノート.txt'
    with open(path, 'rt') as f:
        text = f.read()
    parser = CabochaParser()
    manager = MessageManager(parser=parser)
    token_list = manager.extract_message(text).bags

    creator = CorpusCreator()
    corpus = creator.create(token_list)

    generator = TokenGenerator(corpus)
    next_word = generator.generate('*START*')
    for i in range(100):
        sys.stdout.write(next_word)
        next_word = generator.generate(next_word)
        if next_word == '*END*':
            break


