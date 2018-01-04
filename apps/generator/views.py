import sys

from django.shortcuts import render
from django.views.generic import TemplateView

from preprosessor.parser import MessageManager, CabochaParser
from .markov import CorpusCreator, TokenGenerator


class SentenceMixin(object):
    @staticmethod
    def create_sentence():
        sent = str()
        path = 'data/フリーザ.txt'
        with open(path, 'rt') as f:
            text = f.read()
        parser = CabochaParser()
        manager = MessageManager(parser=parser)
        token_list = manager.extract_message(text).bags

        creator = CorpusCreator()
        corpus = creator.create(token_list)

        generator = TokenGenerator(corpus)
        next_word = generator.generate('*START*')
        for i in range(30):
            sent += next_word
            next_word = generator.generate(next_word)
            if next_word == '*END*':
                break
        return sent


class IndexView(SentenceMixin, TemplateView):
    template_name = 'generator/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sent'] = self.create_sentence()

        return context

