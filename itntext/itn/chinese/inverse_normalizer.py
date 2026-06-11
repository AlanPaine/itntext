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

import os

from itntext.processor import Processor


class InverseNormalizer(Processor):

    def __init__(
        self,
        cache_dir=None,
        overwrite_cache=False,
        remove_interjections=True,
        enable_standalone_number=True,
        enable_0_to_9=False,
        enable_million=False,
    ):
        super().__init__(name="zh_inverse_normalizer", ordertype="itn")
        self.remove_interjections = remove_interjections
        self.convert_number = enable_standalone_number
        self.enable_0_to_9 = enable_0_to_9
        self.enable_million = enable_million
        if cache_dir is None:
            cache_dir = os.path.dirname(os.path.abspath(__file__))
        self.build_fst("zh_itn", cache_dir, overwrite_cache)
