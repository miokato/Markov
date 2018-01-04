import sys

from django.shortcuts import render
from django.views.generic import TemplateView

from preprosessor.parser import MessageManager, CabochaParser
from .corpus import CorpusCreator
from .generator import TokenGenerator


class IndexView(TemplateView):
    template_name = 'generator/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        generator = TokenGenerator('eva')
        sent = generator.generate(num_of_word=20)
        context['sent'] = sent

        return context

