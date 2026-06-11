from pynini import cross, string_file
from pynini.lib.pynutil import delete, insert

from itntext.chinese.rules.cardinal import Cardinal
from itntext.processor import Processor
from itntext.utils import get_abs_path


class Math(Processor):

    def __init__(self, cardinal=None):
        super().__init__(name="math")
        self.cardinal = cardinal or Cardinal()
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        operator = string_file(get_abs_path("chinese/data/math/operator.tsv"))
        unambiguous_operator = string_file(get_abs_path("chinese/data/math/operator_unambiguous.tsv"))
        symbols = cross("~", "到") | cross(":", "比") | cross("<", "小于") | cross(">", "大于")

        number = self.cardinal.number
        tagger = number + (delete(" ").ques + (operator | symbols) + delete(" ").ques + number).star
        tagger |= unambiguous_operator
        tagger = insert('value: "') + tagger + insert('"')
        self.tagger = self.add_tokens(tagger)
