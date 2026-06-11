from pynini.lib.pynutil import delete, insert

from itntext.chinese.rules.cardinal import Cardinal
from itntext.processor import Processor


class Fraction(Processor):

    def __init__(self, cardinal=None):
        super().__init__(name="fraction")
        self.cardinal = cardinal or Cardinal()
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        rmspace = delete(" ").ques
        number = self.cardinal.number

        tagger = (
            insert('numerator: "')
            + number
            + rmspace
            + delete("/")
            + rmspace
            + insert('" denominator: "')
            + number
            + insert('"')
        ).optimize()
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        denominator = delete('denominator: "') + self.SIGMA + delete('" ')
        numerator = delete('numerator: "') + self.SIGMA + delete('"')
        verbalizer = denominator + insert("分之") + numerator
        self.verbalizer = self.delete_tokens(verbalizer)
