from importlib_resources import files
from pynini.lib.pynutil import add_weight, delete

from itntext.chinese.rules.itn_cardinal import Cardinal
from itntext.chinese.rules.itn_date import Date
from itntext.chinese.rules.itn_measure import Measure
from itntext.chinese.rules.char import Char
from itntext.processor import Processor


class InverseNormalizer(Processor):

    def __init__(
        self,
        cache_dir=None,
        overwrite_cache=False,
    ):
        super().__init__(name="zh_inverse_normalizer", ordertype="itn")
        if cache_dir is None:
            cache_dir = files("itntext")
        self.build_fst("zh_itn", cache_dir, overwrite_cache)

    def build_tagger_and_verbalizer(self):
        cardinal = Cardinal()
        date = Date()
        measure = Measure(cardinal=cardinal)
        char = Char()

        tagger = (
            add_weight(date.tagger, 1.02)
            | add_weight(measure.tagger, 1.05)
            | add_weight(cardinal.tagger, 1.06)
            | add_weight(char.tagger, 100)
        ).optimize()
        self.tagger = tagger.star @ self.build_rule(delete(" "), r="[EOS]")

        verbalizer = (
            cardinal.verbalizer
            | char.verbalizer
            | date.verbalizer
            | measure.verbalizer
        ).optimize()
        self.verbalizer = verbalizer.star
