from pynini import string_file
from pynini.lib.pynutil import delete, insert

from itntext.processor import Processor
from itntext.utils import get_abs_path


class Date(Processor):

    def __init__(self):
        super().__init__(name="date", ordertype="itn")
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        digit = string_file(get_abs_path("chinese/data/number/suffix_digit.tsv"))
        zero = string_file(get_abs_path("chinese/data/number/suffix_zero.tsv"))

        # 年份: 二零二四, 一九九九
        year_digit = digit | zero
        year = year_digit + year_digit + year_digit + year_digit + insert('年')

        # 月份: 四月, 十一月
        month = string_file(get_abs_path("chinese/data/date/suffix_m.tsv"))

        # 日期: 二十三日, 一日
        day = string_file(get_abs_path("chinese/data/date/suffix_d.tsv"))

        # 号: 二十三号
        rihao = string_file(get_abs_path("chinese/data/date/suffix_rihao.tsv"))

        # 组合: 四月二十三日, 四月二十三号, 二零二四年四月二十三日
        date = (
            (year.ques + month + day)
            | (year.ques + month + rihao)
            | month
            | day
            | rihao
        )
        tagger = insert('value: "') + date + insert('"')
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        super().build_verbalizer()
