import pynini
from itntext.grammars.inverse_text_normalization.zh.utils import get_abs_path
from itntext.grammars.inverse_text_normalization.zh.graph_utils import (
    DAMO_DIGIT,
    DAMO_NOT_SPACE,
    DAMO_SIGMA,
    GraphFst,
    convert_space,
    delete_extra_space,
    delete_space,
    get_singulars,
    insert_space,
)
from pynini.lib import pynutil


class MoneyFst(GraphFst):
    """
    Finite state transducer for classifying money
        e.g. twelve dollars and five cents -> money { integer_part: "12" fractional_part: 05 currency: "$" }

    Args:
        cardinal: CardinalFst
        decimal: DecimalFst
    """

    def __init__(self, cardinal: GraphFst, decimal: GraphFst):
        super().__init__(name="money", kind="classify")
        # quantity, integer_part, fractional_part, currency

        cardinal_graph = cardinal.graph_no_exception
        decimal_graph = decimal.final_graph_wo_negative
        graph_code = pynini.string_file(get_abs_path("data/money/code.tsv"))
        graph_symbol = pynini.string_file(get_abs_path("data/money/symbol.tsv"))

        graph_unit = (
            pynutil.insert('currency: "')
            + (pynutil.add_weight(graph_symbol, 0.0) | pynutil.add_weight(graph_code, 1.0))
            + pynutil.insert('"')
        )

        graph_integer = (
            pynutil.insert('integer_part: "')
            + cardinal_graph
            + pynutil.insert('"')
            + pynutil.insert(" ")
            + graph_unit
        )

        graph_decimal = decimal_graph + pynutil.insert(" ") + graph_unit

        graph_yuan = (
            pynutil.insert('integer_part: "')
            + cardinal_graph
            + pynutil.insert('"')
            + pynutil.delete("元")
            + pynutil.insert(" ")
            + pynutil.insert('currency: "¥"')
        )
        graph_jiao = pynutil.insert('fractional_part: "') + cardinal_graph + pynutil.insert('"') + pynutil.delete("角")
        graph_fen = pynutil.insert('fractional_part: "0') + cardinal_graph + pynutil.insert('"') + pynutil.delete("分")
        graph_jiao_fen = (
            pynutil.insert('fractional_part: "')
            + cardinal_graph
            + pynutil.delete("角")
            + cardinal_graph
            + pynutil.insert('"')
            + pynutil.delete("分")
        )
        graph_yuan_subunit = graph_yuan + pynutil.insert(" ") + (graph_jiao_fen | graph_jiao | graph_fen)

        final_graph = graph_yuan_subunit | graph_integer | graph_decimal

        final_graph = self.add_tokens(final_graph)
        self.fst = final_graph.optimize()
