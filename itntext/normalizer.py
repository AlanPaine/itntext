from dataclasses import replace

from itntext.config import NormalizerConfig
from itntext.postprocess_fixes import apply_fixes

# 全局引擎缓存，避免重复加载 FST
_engine_cache = {}


class Normalizer:
    """
    itntext Normalizer - API 完全兼容 wetext.Normalizer

    基于 WeTextProcessing 核心引擎（pynini/OpenFST），在内部编译和运行 FST，
    并增加后处理修正层修复 WeText 已知问题：
    - 日期后缀保留（号/日）
    - 分数保护（3/4 不转 3月4日）
    - 时间格式（上午 10:30, 下午 14:00）
    - 身高转换（1.75m）
    - 大数字金额（1234567元）
    - 股票代码不拆分（600519）
    - 单位保留中文（公斤/公里/毫升）

    Args:
        lang: 语言 ("auto", "en", "zh", "ja")
        operator: 操作类型 ("tn" 文本规范化, "itn" 逆文本规范化)
        traditional_to_simple: 繁体转简体（TN 模式）
        full_to_half: 全角转半角（TN 模式）
        remove_interjections: 去除语气词
        remove_puncts: 去除标点（TN 模式）
        tag_oov: 标记 OOV 词（TN 模式）
        enable_0_to_9: 启用 0-9 数字转换（ITN 模式）
        remove_erhua: 去除儿化音（TN 模式）
    """

    def __init__(self, **kwargs):
        self.config = NormalizerConfig(**kwargs)
        self._engine = None
        self._cache_key = None
        self._init_engine()

    def _get_cache_key(self):
        """生成引擎缓存 key（基于影响 FST 编译的参数）"""
        c = self.config
        if c.operator == "itn":
            return f"zh_itn:{c.remove_interjections}:{c.enable_0_to_9}"
        else:
            return (f"zh_tn:{c.remove_interjections}:{c.remove_erhua}:"
                    f"{c.traditional_to_simple}:{c.remove_puncts}:"
                    f"{c.full_to_half}:{c.tag_oov}")

    def _init_engine(self):
        """初始化底层 FST 引擎，传递所有配置参数，使用全局缓存"""
        lang = self.config.lang
        operator = self.config.operator

        if lang in ("auto", "zh"):
            self._cache_key = self._get_cache_key()
            if self._cache_key in _engine_cache:
                self._engine = _engine_cache[self._cache_key]
                return

            if operator == "itn":
                from itntext.itn.chinese.inverse_normalizer import InverseNormalizer
                self._engine = InverseNormalizer(
                    remove_interjections=self.config.remove_interjections,
                    enable_standalone_number=True,
                    enable_0_to_9=self.config.enable_0_to_9,
                )
            else:  # tn
                from itntext.tn.chinese.normalizer import Normalizer as TNNormalizer
                self._engine = TNNormalizer(
                    remove_interjections=self.config.remove_interjections,
                    remove_erhua=self.config.remove_erhua,
                    traditional_to_simple=self.config.traditional_to_simple,
                    remove_puncts=self.config.remove_puncts,
                    full_to_half=self.config.full_to_half,
                    tag_oov=self.config.tag_oov,
                )
            _engine_cache[self._cache_key] = self._engine

        elif lang == "en":
            raise NotImplementedError(
                "English support is not yet implemented. "
                "Contributions are welcome!"
            )
        elif lang == "ja":
            raise NotImplementedError(
                "Japanese support is not yet implemented. "
                "Contributions are welcome!"
            )
        else:
            raise ValueError(f"Unsupported language: {lang}. Must be one of: auto, en, zh, ja")

    def normalize(self, text: str, **kwargs) -> str:
        """
        Normalize the text.

        Args:
            text: The text to normalize.
            **kwargs: The keyword arguments to override the config.
        """
        config = replace(self.config, **kwargs)

        # 使用内部 FST 引擎进行基础转换
        result = self._engine.normalize(text)

        # 对中文 ITN 应用后处理修正
        if config.lang in ("auto", "zh") and config.operator == "itn":
            result = apply_fixes(result, text)

        return result
