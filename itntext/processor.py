# Copyright (c) 2022 Zhendong Peng (pzd17@tsinghua.org.cn)
# Copyright (c) 2024 WENET COMMUNITY.  Xingchen Song (sxc19@tsinghua.edu.cn).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
itntext Processor - 基于 kaldifst 的 FST 运行时

编译时使用 pynini 生成 FST 文件，运行时仅依赖 kaldifst 加载预编译 FST。
与 wetext 使用相同的运行时引擎。
"""

import os

from kaldifst import TextNormalizer

from itntext.token_parser import TokenParser


class Processor:
    """
    基于 kaldifst 的 FST 处理器

    加载预编译的 tagger.fst 和 verbalizer.fst，通过 kaldifst 运行。
    """

    def __init__(self, name, ordertype="itn"):
        self.name = name
        self.ordertype = ordertype
        self.tagger = None
        self.verbalizer = None

    def build_fst(self, fst_name, cache_dir, overwrite=False):
        """加载预编译的 FST 文件"""
        tagger_path = os.path.join(cache_dir, f"{fst_name}_tagger.fst")
        verbalizer_path = os.path.join(cache_dir, f"{fst_name}_verbalizer.fst")

        if not os.path.exists(tagger_path):
            raise FileNotFoundError(f"FST file not found: {tagger_path}. "
                                    f"Please run: python scripts/build_fsts.py")
        if not os.path.exists(verbalizer_path):
            raise FileNotFoundError(f"FST file not found: {verbalizer_path}. "
                                    f"Please run: python scripts/build_fsts.py")

        self.tagger = TextNormalizer(tagger_path)
        self.verbalizer = TextNormalizer(verbalizer_path)

    def tag(self, input_text):
        """Tag the text using the tagger FST."""
        if self.tagger is None:
            raise RuntimeError("FST not loaded. Call build_fst() first.")
        return self.tagger(input_text).strip()

    def verbalize(self, input_text):
        """Verbalize the text using the verbalizer FST."""
        if self.verbalizer is None:
            raise RuntimeError("FST not loaded. Call build_fst() first.")
        return self.verbalizer(input_text).strip()

    def normalize(self, input_text):
        """
        Normalize the text through tag -> reorder -> verbalize pipeline.
        """
        tagged = self.tag(input_text)
        if len(tagged) == 0:
            return input_text
        reordered = TokenParser("zh", self.ordertype).reorder(tagged)
        verbalized = self.verbalize(reordered)
        if len(verbalized) == 0:
            return input_text
        return verbalized
