from pynini import accep
from pynini.lib.pynutil import insert

from itntext.processor import Processor


class Char(Processor):

    def __init__(self):
        super().__init__(name="char")
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        digit = accep("0") | accep("1") | accep("2") | accep("3") | accep("4") | accep("5") | accep("6") | accep("7") | accep("8") | accep("9")
        alpha = self.ALPHA
        char = digit | alpha
        tagger = insert('value: "') + char + insert('"')
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        super().build_verbalizer()
