class Message(object):
    _instance = None

    def __init__(self):
        self.text = str()
        self.sentences = []
        self.bags = []
        self.wakati_list = []

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __str__(self):
        return self.text

    def __repr__(self):
        return self.text

    def add_sentence(self, sentence):
        self.sentences.append(sentence)

    def display_sentences(self):
        for sentence in self.sentences:
            print(sentence)

    def clear(self):
        self.text = str()
        self.sentences.clear()
        self.bags.clear()
