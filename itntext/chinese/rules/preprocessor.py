from pynini import string_file

from itntext.processor import Processor
from itntext.utils import get_abs_path


class PreProcessor(Processor):

    def __init__(self, traditional_to_simple=True):
        super().__init__(name="preprocessor")
        traditional2simple = string_file(get_abs_path("chinese/data/char/traditional_to_simple.tsv"))

        processor = self.build_rule("")
        if traditional_to_simple:
            processor @= self.build_rule(traditional2simple)

        self.processor = processor.optimize()
