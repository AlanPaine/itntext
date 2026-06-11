from pynini import string_file
from pynini.lib.pynutil import delete, insert

from itntext.processor import Processor
from itntext.utils import get_abs_path


class Time(Processor):

    def __init__(self):
        super().__init__(name="time")
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        h = string_file(get_abs_path("chinese/data/time/hour.tsv"))
        m = string_file(get_abs_path("chinese/data/time/minute.tsv"))
        s = string_file(get_abs_path("chinese/data/time/second.tsv"))
        noon = string_file(get_abs_path("chinese/data/time/noon.tsv"))
        colon = delete(":") | delete("：")

        tagger = (
            insert('hour: "')
            + h
            + insert('" ')
            + colon
            + insert('minute: "')
            + m
            + insert('"')
            + (colon + insert(' second: "') + s + insert('"')).ques
            + delete(" ").ques
            + (insert(' noon: "') + noon + insert('"')).ques
        )
        tagger = self.add_tokens(tagger)

        to = (delete("-") | delete("~")) + insert(' char { value: "到" } ')
        self.tagger = tagger + (to + tagger).ques

    def build_verbalizer(self):
        noon = delete('noon: "') + self.SIGMA + delete('" ')
        hour = delete('hour: "') + self.SIGMA + delete('" ')
        minute = delete('minute: "') + self.SIGMA + delete('"')
        second = delete(' second: "') + self.SIGMA + delete('"')
        verbalizer = noon.ques + hour + minute + second.ques
        self.verbalizer = self.delete_tokens(verbalizer)
