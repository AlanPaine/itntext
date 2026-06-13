import os
from time import perf_counter
from argparse import ArgumentParser
from itntext.grammars.text_normalization.en.graph_utils import generator_main


def parse_args():
    parser = ArgumentParser()

    parser.add_argument(
        "--language",
        help="language",
        choices=["de", "en", "es", "fr", "id", "ja", "ko", "pt", "ru", "vi", "zh"],
        default="en",
        type=str,
    )
    parser.add_argument(
        "--export_dir",
        help="path to export directory. Default to current directory.",
        default="./",
        type=str,
    )
    return parser.parse_args()


def get_grammars(lang: str = "en"):
    if lang == "de":
        from itntext.grammars.inverse_text_normalization.de.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.de.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "en":
        from itntext.grammars.inverse_text_normalization.en.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.en.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "es":
        from itntext.grammars.inverse_text_normalization.es.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.es.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "fr":
        from itntext.grammars.inverse_text_normalization.fr.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.fr.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "id":
        from itntext.grammars.inverse_text_normalization.id.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.id.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "ja":
        from itntext.grammars.inverse_text_normalization.ja.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.ja.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "ko":
        from itntext.grammars.inverse_text_normalization.ko.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.ko.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "pt":
        from itntext.grammars.inverse_text_normalization.pt.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.pt.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "ru":
        from itntext.grammars.inverse_text_normalization.ru.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.ru.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "vi":
        from itntext.grammars.inverse_text_normalization.vi.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.vi.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    elif lang == "zh":
        from itntext.grammars.inverse_text_normalization.zh.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.zh.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )
    else:
        from itntext.grammars.inverse_text_normalization.en.taggers.tokenize_and_classify import (
            ClassifyFst,
        )
        from itntext.grammars.inverse_text_normalization.en.verbalizers.verbalize_final import (
            VerbalizeFinalFst,
        )

    return ClassifyFst().fst, VerbalizeFinalFst().fst


if __name__ == "__main__":
    args = parse_args()

    export_dir = args.export_dir
    os.makedirs(export_dir, exist_ok=True)
    tagger_far_file = os.path.join(export_dir, args.language + "_itn_tagger.far")
    verbalizer_far_file = os.path.join(export_dir, args.language + "_itn_verbalizer.far")

    start_time = perf_counter()
    tagger_fst, verbalizer_fst = get_grammars(args.language)
    generator_main(tagger_far_file, {"tokenize_and_classify": tagger_fst})
    generator_main(verbalizer_far_file, {"verbalize": verbalizer_fst})
    print(f"Time to generate graph: {round(perf_counter() - start_time, 2)} sec")
