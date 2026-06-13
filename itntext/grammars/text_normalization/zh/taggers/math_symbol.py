import pynini
from itntext.grammars.text_normalization.zh.graph_utils import GraphFst
from itntext.grammars.text_normalization.zh.taggers.cardinal import Cardinal
from itntext.grammars.text_normalization.zh.utils import get_abs_path
from pynini.lib import pynutil


class MathSymbol(GraphFst):
    """
    + -> tokens { sign: "加" }
    """

    def __init__(self, deterministic: bool = True, lm: bool = False):
        super().__init__(name="sign", kind="classify", deterministic=deterministic)
        """
            add your sign in data/math/symbol.tsv,this graph just convert sigh to character,you can add more 
            cases with detailed cases 
        """
        score_sign = pynini.string_file(get_abs_path("data/math/score.tsv"))
        score = (
            pynutil.insert('score: "')
            + Cardinal().graph_cardinal
            + score_sign
            + Cardinal().graph_cardinal
            + pynutil.insert('"')
        )
        graph = score
        self.fst = graph.optimize()
