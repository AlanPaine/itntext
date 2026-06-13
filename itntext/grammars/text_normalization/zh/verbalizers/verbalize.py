import pynini
from itntext.grammars.text_normalization.zh.graph_utils import GraphFst
from itntext.grammars.text_normalization.zh.verbalizers.cardinal import Cardinal
from itntext.grammars.text_normalization.zh.verbalizers.char import Char
from itntext.grammars.text_normalization.zh.verbalizers.date import Date
from itntext.grammars.text_normalization.zh.verbalizers.fraction import Fraction
from itntext.grammars.text_normalization.zh.verbalizers.math_symbol import MathSymbol
from itntext.grammars.text_normalization.zh.verbalizers.measure import Measure
from itntext.grammars.text_normalization.zh.verbalizers.money import Money
from itntext.grammars.text_normalization.zh.verbalizers.time import Time
from itntext.grammars.text_normalization.zh.verbalizers.whitelist import Whitelist


class VerbalizeFst(GraphFst):
    """
    Composes other verbalizer grammars.
    For deployment, this grammar will be compiled and exported to OpenFst Finate State Archiv (FAR) File.
    More details to deployment at NeMo/tools/text_processing_deployment.
    Args:
        deterministic: if True will provide a single transduction option,
            for False multiple options (used for audio-based normalization)
    """

    def __init__(self, deterministic: bool = True):
        super().__init__(name="verbalize", kind="verbalize", deterministic=deterministic)

        date = Date(deterministic=deterministic)
        cardinal = Cardinal(deterministic=deterministic)
        char = Char(deterministic=deterministic)
        fraction = Fraction(deterministic=deterministic)
        math_symbol = MathSymbol(deterministic=deterministic)
        money = Money(deterministic=deterministic)
        measure = Measure(deterministic=deterministic)
        time = Time(deterministic=deterministic)
        whitelist = Whitelist(deterministic=deterministic)

        graph = pynini.union(
            date.fst,
            cardinal.fst,
            fraction.fst,
            char.fst,
            math_symbol.fst,
            money.fst,
            measure.fst,
            time.fst,
            whitelist.fst,
        )

        self.fst = graph.optimize()
