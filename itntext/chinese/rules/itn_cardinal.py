from pynini import accep, cross, string_file, union
from pynini.lib.pynutil import add_weight, delete, insert

from itntext.processor import Processor
from itntext.utils import get_abs_path


class Cardinal(Processor):

    def __init__(self):
        super().__init__("cardinal", ordertype="itn")
        self.number = None
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        zero = string_file(get_abs_path("chinese/data/number/suffix_zero.tsv"))
        digit = string_file(get_abs_path("chinese/data/number/suffix_digit.tsv"))
        teen = string_file(get_abs_path("chinese/data/number/suffix_teen.tsv"))
        sign = string_file(get_abs_path("chinese/data/number/suffix_sign.tsv"))
        dot = string_file(get_abs_path("chinese/data/number/suffix_dot.tsv"))

        digits = zero | digit

        # 11 => 11, 10 => 10
        ten = teen + (digit | zero)
        # 21 => 21, 30 => 30
        tens = digit + (digit | zero)
        # 111 => 111, 101 => 101, 100 => 100
        hundred = digit + (tens | (zero + digit) | zero**2)
        # 1111 => 1111, 1001 => 1001, 1000 => 1000
        thousand = digit + (hundred | (zero + tens) | (zero**2 + digit) | zero**3)

        # exactly 4 input digits
        four = thousand | (zero + hundred) | (zero**2 + tens) | (zero**3 + digit) | zero**4

        # 万级
        ten_thousand = (thousand | hundred | ten | digit) + four

        # 亿级
        hundred_million = (thousand | hundred | ten | digit) + (
            four + four
            | zero**4 + (zero + hundred | zero**2 + tens | zero**3 + digit | thousand)
            | zero**8
        )

        number = digits | ten | hundred | thousand | ten_thousand | hundred_million
        number = sign.ques + number + (dot + digits.plus).ques
        percent = insert("百分之") + number + delete("%")
        self.number = accep("约").ques + accep("人均").ques + (number | percent)

        # special cases
        special_tilde = string_file(get_abs_path("chinese/data/number/special_tilde.tsv"))
        special_dash = string_file(get_abs_path("chinese/data/number/special_dash.tsv"))
        repeat_digit = string_file(get_abs_path("chinese/data/number/repeat_digit.tsv"))

        cardinal = number | special_tilde | special_dash | repeat_digit
        tagger = insert('value: "') + cardinal + insert('"')
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        super().build_verbalizer()
