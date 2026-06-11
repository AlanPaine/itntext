from importlib_resources import files
from pynini.lib.pynutil import add_weight, delete

from itntext.chinese.rules.cardinal import Cardinal
from itntext.chinese.rules.char import Char
from itntext.chinese.rules.date import Date
from itntext.chinese.rules.fraction import Fraction
from itntext.chinese.rules.math import Math
from itntext.chinese.rules.measure import Measure
from itntext.chinese.rules.money import Money
from itntext.chinese.rules.postprocessor import PostProcessor
from itntext.chinese.rules.preprocessor import PreProcessor
from itntext.chinese.rules.time import Time
from itntext.chinese.rules.whitelist import Whitelist
from itntext.processor import Processor


class Normalizer(Processor):

    def __init__(
        self,
        cache_dir=None,
        overwrite_cache=False,
        remove_interjections=True,
        remove_erhua=True,
        traditional_to_simple=True,
        remove_puncts=False,
        full_to_half=True,
        tag_oov=False,
    ):
        super().__init__(name="zh_normalizer")
        self.remove_interjections = remove_interjections
        self.remove_erhua = remove_erhua
        self.traditional_to_simple = traditional_to_simple
        self.remove_puncts = remove_puncts
        self.full_to_half = full_to_half
        self.tag_oov = tag_oov
        if cache_dir is None:
            cache_dir = files("itntext")
        self.build_fst("zh_tn", cache_dir, overwrite_cache)

    def build_tagger_and_verbalizer(self):
        processor = PreProcessor(traditional_to_simple=self.traditional_to_simple).processor
        cardinal = Cardinal()
        date = Date()
        whitelist = Whitelist(remove_erhua=self.remove_erhua)
        fraction = Fraction(cardinal=cardinal)
        measure = Measure(cardinal=cardinal)
        money = Money(cardinal=cardinal)
        time = Time()
        math = Math(cardinal=cardinal)
        char = Char()

        tagger = (
            add_weight(date.tagger, 1.02)
            | add_weight(whitelist.tagger, 1.03)
            | add_weight(fraction.tagger, 1.05)
            | add_weight(measure.tagger, 1.05)
            | add_weight(money.tagger, 1.05)
            | add_weight(time.tagger, 1.05)
            | add_weight(cardinal.tagger, 1.06)
            | add_weight(math.tagger, 90)
            | add_weight(char.tagger, 100)
        ).optimize()
        tagger = (processor @ tagger).star
        self.tagger = tagger @ self.build_rule(delete(" "), r="[EOS]")

        verbalizer = (
            cardinal.verbalizer
            | char.verbalizer
            | date.verbalizer
            | fraction.verbalizer
            | math.verbalizer
            | measure.verbalizer
            | money.verbalizer
            | time.verbalizer
            | whitelist.verbalizer
        ).optimize()

        postprocessor = PostProcessor(
            remove_interjections=self.remove_interjections,
            remove_puncts=self.remove_puncts,
            full_to_half=self.full_to_half,
            tag_oov=self.tag_oov,
        ).processor
        self.verbalizer = (verbalizer @ postprocessor).star
