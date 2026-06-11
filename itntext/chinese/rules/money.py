from pynini import string_file
from pynini.lib.pynutil import delete, insert

from itntext.chinese.rules.cardinal import Cardinal
from itntext.processor import Processor
from itntext.utils import get_abs_path


class Money(Processor):

    def __init__(self, cardinal=None):
        super().__init__(name="money")
        self.cardinal = cardinal or Cardinal()
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        code = string_file(get_abs_path("chinese/data/money/code.tsv"))
        symbol = string_file(get_abs_path("chinese/data/money/symbol.tsv"))

        number = self.cardinal.number
        tagger = (
            insert('currency: "')
            + (code | symbol)
            + delete(" ").ques
            + insert('" ')
            + insert('value: "')
            + number
            + insert('"')
        )
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        value = delete('value: "') + self.SIGMA + delete('" ')
        currency = delete('currency: "') + self.SIGMA + delete('"')
        verbalizer = value + currency
        self.verbalizer = self.delete_tokens(verbalizer)
