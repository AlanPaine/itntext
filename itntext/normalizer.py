from dataclasses import replace

from itntext.config import NormalizerConfig
from itntext.postprocess_fixes import apply_fixes

# 全局引擎缓存，避免重复加载 FST
_engine_cache = {}

# 全角 -> 半角映射表（从 TSV 加载）
_FULLWIDTH_TO_HALFWIDTH = {}

# 语气词黑名单
_INTERJECTIONS = set()

# 中文标点
_PUNCTS = set()


def _init_postprocess_data():
    """加载 postprocess 所需数据"""
    global _FULLWIDTH_TO_HALFWIDTH, _INTERJECTIONS, _PUNCTS
    if _FULLWIDTH_TO_HALFWIDTH:
        return

    import os

    base_dir = os.path.dirname(os.path.abspath(__file__))

    # 全角半角映射
    f2h_path = os.path.join(base_dir, "tn", "chinese", "data", "char", "fullwidth_to_halfwidth.tsv")
    if os.path.exists(f2h_path):
        with open(f2h_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and "\t" in line:
                    full, half = line.split("\t", 1)
                    _FULLWIDTH_TO_HALFWIDTH[full] = half

    # 语气词黑名单
    blacklist_path = os.path.join(base_dir, "tn", "chinese", "data", "default", "blacklist.tsv")
    if os.path.exists(blacklist_path):
        with open(blacklist_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    _INTERJECTIONS.add(line)

    # 中文标点
    puncts_path = os.path.join(base_dir, "tn", "chinese", "data", "char", "punctuations_zh.tsv")
    if os.path.exists(puncts_path):
        with open(puncts_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    _PUNCTS.add(line)


_init_postprocess_data()


def _full_to_half(text):
    """全角转半角"""
    return text.translate(str.maketrans(_FULLWIDTH_TO_HALFWIDTH))


def _remove_interjections(text):
    """去除语气词"""
    for word in sorted(_INTERJECTIONS, key=len, reverse=True):
        text = text.replace(word, "")
    return text.strip()


def _remove_puncts(text):
    """去除标点符号（中文标点 + 英文标点）"""
    import string
    puncts = _PUNCTS | set(string.punctuation)
    return "".join(c for c in text if c not in puncts).strip()


class Normalizer:
    """
    itntext Normalizer - API 完全兼容 wetext.Normalizer

    基于 WeTextProcessing 核心引擎（kaldifst），在内部运行预编译 FST，
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
            # TN 基础 FST 只受 remove_erhua 和 traditional_to_simple 影响
            return f"zh_tn:{c.remove_erhua}:{c.traditional_to_simple}"

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
                    remove_interjections=False,  # 运行时处理
                    remove_erhua=self.config.remove_erhua,
                    traditional_to_simple=self.config.traditional_to_simple,
                    remove_puncts=False,  # 运行时处理
                    full_to_half=False,  # 运行时处理
                    tag_oov=False,  # 运行时处理
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

        # TN 后处理（运行时处理，与 wetext 一致）
        if config.lang in ("auto", "zh") and config.operator == "tn":
            if config.remove_interjections:
                result = _remove_interjections(result)
            if config.remove_puncts:
                result = _remove_puncts(result)
            if config.full_to_half:
                result = _full_to_half(result)

        # 对中文 ITN 应用后处理修正
        if config.lang in ("auto", "zh") and config.operator == "itn":
            result = apply_fixes(result, text)

        return result
