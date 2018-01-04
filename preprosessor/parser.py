import re
import os

from gensim import corpora, similarities, models

from .cabocha_analyzer import CaboChaAnalyzer
from .message import Message
from .sentence import Sentence
from pyknp import Jumanpp


class MessageManager:
    def __init__(self, parser):
        self.parser = parser

    def extract_message(self, text):
        message = self.parser.parse_message(text)
        message = self.parser.parse(message)
        return message


class Parser:
    def __init__(self):
        split_pattern = r'(。|？|\?|！|\!|\n)'
        self.split_compiled = re.compile(split_pattern)

    def parse_message(self, raw_text):
        message = Message()
        message.clear()
        message.text = raw_text.lower()
        try:
            raw_sents = self.split_compiled.split(message.text)
        except AttributeError:
            return None

        raw_sents = [s.strip() for s in raw_sents if s]
        #raw_sents = [s for s in raw_sents if len(s) > 1]
        for raw_sent in raw_sents:
            sent = Sentence()
            sent.text = raw_sent
            message.add_sentence(sent)
        return message


class CabochaParser(Parser):
    def __init__(self):
        super().__init__()
        remove_pattern = r'・|、|\,|\.| |　'
        self.remove_compiled = re.compile(remove_pattern)
        self.analyzer = CaboChaAnalyzer('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

    def parse(self, message):
        for sent in message.sentences:
            #sent.text = self.remove_compiled.sub('', sent.text)
            sent.tree = self.analyzer.parse(sent.text)
            sent.bag = self.create_bags(sent)
            message.wakati_list += self.execute_wakati(sent)
            message.bags += sent.bag
        return message

    @staticmethod
    def execute_wakati(sent):
        wakati_list = []
        for token in sent.tree.tokens:
            wakati_list.append(token.surface)
        return wakati_list

    @staticmethod
    def create_bags(sent):
        bag = []
        for token in sent.tree.tokens:
            #if token.pos == '名詞' or token.pos == '動詞':
            bag.append(token.surface)
        return bag


class JumanParser(Parser):
    def __init__(self):
        super().__init__()
        remove_pattern = r'・|、|\,|\.| |　'
        self.remove_compiled = re.compile(remove_pattern)
        self.analyzer = Jumanpp()

    def parse(self, message):
        for sent in message.sentences:
            sent.text = self.remove_compiled.sub('', sent.text)
            parsed = self.analyzer.analysis(sent.text)
            mrph_list = parsed.mrph_list()
            sent.bag = self.create_bags(mrph_list)
            message.bags += sent.bag
        return message

    @staticmethod
    def create_bags(mrph_list):
        bag = []
        for mrph in mrph_list:
            if mrph.hinsi == '名詞' or mrph.hinsi == '動詞':
                bag.append(mrph.genkei)
        return bag
