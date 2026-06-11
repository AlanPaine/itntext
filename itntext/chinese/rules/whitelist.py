from pynini import accep, string_file
from pynini.lib.pynutil import add_weight, delete, insert

from itntext.processor import Processor
from itntext.utils import get_abs_path


class Whitelist(Processor):

    def __init__(self, remove_erhua=True):
        super().__init__(name="whitelist")
        self.remove_erhua = remove_erhua
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        whitelist = string_file(get_abs_path("chinese/data/default/whitelist.tsv"))

        erhua = add_weight(insert('erhua: "') + accep("儿"), 0.1)
        tagger = (erhua | (insert('value: "') + whitelist)) + insert('"')
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        super().build_verbalizer()
        if self.remove_erhua:
            verbalizer = self.delete_tokens(delete('erhua: "儿"'))
        else:
            verbalizer = self.delete_tokens(delete('erhua: "') + accep("儿") + delete('"'))
        self.verbalizer |= verbalizer
