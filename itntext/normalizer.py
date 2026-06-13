from itntext.config import NormalizerConfig
from itntext.fst_processor import FstProcessor, ITN_LANGUAGES, TN_LANGUAGES


_engine_cache = {}


class Normalizer:
    """itntext Normalizer，保持 wetext 风格 API。"""

    def __init__(self, **kwargs):
        self.config = NormalizerConfig(**kwargs)
        self._engine = None
        self._cache_key = None
        self._init_engine()

    def _get_cache_key(self):
        lang = "zh" if self.config.lang == "auto" else self.config.lang
        return f"{lang}:{self.config.operator}"

    def _init_engine(self):
        lang = "zh" if self.config.lang == "auto" else self.config.lang
        operator = self.config.operator
        supported = ITN_LANGUAGES if operator == "itn" else TN_LANGUAGES
        if lang not in supported:
            raise ValueError(
                f"Unsupported {operator.upper()} language: {lang}. "
                f"Supported languages: auto, {', '.join(supported)}"
            )

        self._cache_key = self._get_cache_key()
        if self._cache_key in _engine_cache:
            self._engine = _engine_cache[self._cache_key]
            return
        self._engine = FstProcessor(lang=lang, operator=operator)
        _engine_cache[self._cache_key] = self._engine

    def normalize(self, text: str, **kwargs) -> str:
        if kwargs:
            config = NormalizerConfig(**{**self.config.__dict__, **kwargs})
            return Normalizer(**config.__dict__).normalize(text)
        return self._engine.normalize(text)

    def normalize_list(self, texts: list[str], **kwargs) -> list[str]:
        return [self.normalize(text, **kwargs) for text in texts]


def preload(languages=None, operators=None) -> None:
    languages = languages or ["zh"]
    operators = operators or ["tn", "itn"]
    for operator in operators:
        supported = ITN_LANGUAGES if operator == "itn" else TN_LANGUAGES
        for lang in languages:
            route_lang = "zh" if lang == "auto" else lang
            if route_lang in supported:
                Normalizer(lang=route_lang, operator=operator)
