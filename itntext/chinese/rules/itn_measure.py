from pynini import accep, cross, string_file
from pynini.lib.pynutil import add_weight, delete, insert

from itntext.chinese.rules.itn_cardinal import Cardinal
from itntext.processor import Processor
from itntext.utils import get_abs_path


class Measure(Processor):

    def __init__(self, cardinal=None):
        super().__init__(name="measure", ordertype="itn")
        self.cardinal = cardinal or Cardinal()
        self.build_tagger()
        self.build_verbalizer()

    def build_tagger(self):
        units_en = string_file(get_abs_path("chinese/data/measure/units_en.tsv"))
        units_zh = string_file(get_abs_path("chinese/data/measure/units_zh.tsv"))
        units = add_weight((cross("k", "千") | cross("w", "万")), 0.1).ques + (units_en | units_zh)
        rmspace = delete(" ").ques
        to = cross("-", "到") | cross("~", "到") | accep("到")

        number = self.cardinal.number
        strip_comma = self.build_rule(delete(",") | delete("，"), self.DIGIT, self.DIGIT)
        number = strip_comma @ number
        number @= self.build_rule(cross("两", "二"), "[BOS]", "[EOS]")

        # 身高一米七五 => 1.75m
        # 一米七五 = 1米75
        height_pattern = (
            insert('value: "')
            + number
            + rmspace
            + units
            + insert('"')
        )

        # 1-11个，1个-11个
        prefix = number + (rmspace + units).ques + to
        measure = prefix.ques + number + rmspace + units

        for unit in ["两", "月", "号"]:
            measure @= self.build_rule(cross("两" + unit, "二" + unit), l="[BOS]")
            measure @= self.build_rule(cross("到两" + unit, "到二" + unit), r="[EOS]")

        # xxxx年, xxxx-xxxx年
        digits = self.cardinal.number
        yyyy = digits**4
        unit = accep("年") | accep("年度") | accep("赛季")
        prefix = yyyy + (rmspace + unit).ques + to
        annual = prefix.ques + yyyy + unit

        tagger = insert('value: "') + (measure | annual | height_pattern) + insert('"')

        # 10km/h
        rmsign = rmspace + delete("/") + rmspace
        tagger |= insert('numerator: "') + measure + rmsign + insert('" denominator: "') + (measure | units) + insert('"')
        self.tagger = self.add_tokens(tagger)

    def build_verbalizer(self):
        super().build_verbalizer()
        denominator = delete('denominator: "') + self.SIGMA + delete('" ')
        numerator = delete('numerator: "') + self.SIGMA + delete('"')
        verbalizer = insert("每") + denominator + numerator
        self.verbalizer |= self.delete_tokens(verbalizer)
