import os

from pynini import Fst

_FST_DIR = os.path.join(os.path.dirname(__file__), "fsts")


def _load_fst(path: str) -> callable:
    fst = Fst.read(path)

    def apply(text: str) -> str:
        from pynini import escape, shortestpath
        lattice = escape(text) @ fst
        return shortestpath(lattice, nshortest=1, unique=True).string()

    return apply


FSTS = {
    "preprocess": {
        "traditional_to_simple": _load_fst(os.path.join(_FST_DIR, "traditional_to_simple.fst")),
    },
    "postprocess": {
        "full_to_half": _load_fst(os.path.join(_FST_DIR, "full_to_half.fst")),
        "remove_interjections": _load_fst(os.path.join(_FST_DIR, "remove_interjections.fst")),
        "remove_puncts": _load_fst(os.path.join(_FST_DIR, "remove_puncts.fst")),
        "tag_oov": _load_fst(os.path.join(_FST_DIR, "tag_oov.fst")),
    },
    "zh": {
        "tn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "zh", "tn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "zh", "tn", "verbalizer.fst")),
            "verbalizer_remove_erhua": _load_fst(os.path.join(_FST_DIR, "zh", "tn", "verbalizer_remove_erhua.fst")),
        },
        "itn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "zh", "itn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "zh", "itn", "verbalizer.fst")),
            "tagger_enable_0_to_9": _load_fst(os.path.join(_FST_DIR, "zh", "itn", "tagger_enable_0_to_9.fst")),
        },
    },
    "en": {
        "tn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "en", "tn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "en", "tn", "verbalizer.fst")),
        },
        "itn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "en", "itn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "en", "itn", "verbalizer.fst")),
        },
    },
    "ja": {
        "tn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "ja", "tn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "ja", "tn", "verbalizer.fst")),
        },
        "itn": {
            "tagger": _load_fst(os.path.join(_FST_DIR, "ja", "itn", "tagger.fst")),
            "verbalizer": _load_fst(os.path.join(_FST_DIR, "ja", "itn", "verbalizer.fst")),
            "tagger_enable_0_to_9": _load_fst(os.path.join(_FST_DIR, "ja", "itn", "tagger_enable_0_to_9.fst")),
        },
    },
}
