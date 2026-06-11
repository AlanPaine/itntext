from pynini import string_file
from pynini.lib.pynutil import delete, insert

from itntext.processor import Processor
from itntext.utils import get_abs_path


class Date(Processor):

    def __init__(self):
        super().__init__(name="date")
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        digit = string_file(get_abs_path("chinese/data/number/digit.tsv"))
        zero = string_file(get_abs_path("chinese/data/number/zero.tsv"))

        yyyy = digit + (digit | zero) ** 3
        m = string_file(get_abs_path("chinese/data/date/m.tsv"))
        mm = string_file(get_abs_path("chinese/data/date/mm.tsv"))
        d = string_file(get_abs_path("chinese/data/date/d.tsv"))
        dd = string_file(get_abs_path("chinese/data/date/dd.tsv"))
        rmsign = (delete("/") | delete("-") | delete(".")) + insert(" ")

        year = insert('year: "') + yyyy + insert('年"')
        month = insert('month: "') + (m | mm) + insert('"')
        month_two_digit = insert('month: "') + mm + insert('"')
        day = insert('day: "') + (d | dd) + insert('"')

        # yyyy/m/d | yyyy/mm/dd | dd/mm/yyyy
        # yyyy/0m | 0m/yyyy | 0m/dd
        date = (
            (year + rmsign + month + rmsign + day)
            | (day + rmsign + month + rmsign + year)
            | (year + rmsign + month_two_digit)
            | (month_two_digit + rmsign + year)
            | (month_two_digit + rmsign + day)
        )
        tagger = self.add_tokens(date)

        to = (delete("-") | delete("~")) + insert(' char { value: "到" } ')
        self.tagger = tagger + (to + tagger).ques

    def build_verbalizer(self):
        year = delete('year: "') + self.SIGMA + delete('" ')
        month = delete('month: "') + self.SIGMA + delete('"')
        day = delete(' day: "') + self.SIGMA + delete('"')
        verbalizer = year.ques + month + day.ques
        self.verbalizer = self.delete_tokens(verbalizer)
