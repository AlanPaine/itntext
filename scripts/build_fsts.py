#!/usr/bin/env python3
"""itntext 多语言 FST 编译脚本。"""

import argparse
import os
import sys
from time import perf_counter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from itntext.fst_processor import ITN_LANGUAGES, TN_LANGUAGES


def _write_fst(graph, path: str, overwrite: bool) -> bool:
    if os.path.exists(path) and not overwrite:
        print(f"跳过已存在: {path}")
        return False
    os.makedirs(os.path.dirname(path), exist_ok=True)
    graph.optimize().write(path)
    print(f"写入: {path}")
    return True


def _get_itn_grammars(lang: str):
    if lang == "tl":
        from itntext.grammars.inverse_text_normalization.tl.taggers.tokenize_and_classify import ClassifyFst
        from itntext.grammars.inverse_text_normalization.tl.verbalizers.verbalize_final import VerbalizeFinalFst

        return ClassifyFst().fst, VerbalizeFinalFst().fst

    from itntext.grammars.inverse_text_normalization.export_models import get_grammars

    return get_grammars(lang)


def _get_tn_grammars(lang: str, input_case: str):
    from itntext.grammars.text_normalization.export_models import get_grammars

    return get_grammars(lang, input_case)


def build_language(operator: str, lang: str, overwrite: bool = False, input_case: str = "cased") -> None:
    if operator == "itn":
        tagger_fst, verbalizer_fst = _get_itn_grammars(lang)
    elif operator == "tn":
        tagger_fst, verbalizer_fst = _get_tn_grammars(lang, input_case)
    else:
        raise ValueError(f"Unsupported operator: {operator}")

    out_dir = os.path.join(PROJECT_ROOT, "itntext", "fst", operator, lang)
    prefix = f"{lang}_{operator}"
    _write_fst(tagger_fst, os.path.join(out_dir, f"{prefix}_tagger.fst"), overwrite)
    _write_fst(verbalizer_fst, os.path.join(out_dir, f"{prefix}_verbalizer.fst"), overwrite)


def build_many(operator: str, languages, overwrite: bool = False, input_case: str = "cased"):
    for lang in languages:
        print("=" * 60)
        print(f"编译 {lang} {operator.upper()} FST")
        print("=" * 60)
        start = perf_counter()
        build_language(operator, lang, overwrite=overwrite, input_case=input_case)
        print(f"{lang} {operator.upper()} 编译完成，用时 {perf_counter() - start:.2f}s\n")


def main():
    parser = argparse.ArgumentParser(description="编译 itntext 多语言 FST 文件")
    parser.add_argument("--overwrite", action="store_true", help="强制重新编译，覆盖已有 FST")
    parser.add_argument("--operator", choices=["all", "itn", "tn"], default="all", help="编译范围")
    parser.add_argument("--language", default="all", help="语言代码，默认 all")
    parser.add_argument("--input-case", choices=["lower_cased", "cased"], default="cased", help="TN 输入大小写模式")
    args = parser.parse_args()

    operators = ["itn", "tn"] if args.operator == "all" else [args.operator]
    for operator in operators:
        supported = ITN_LANGUAGES if operator == "itn" else TN_LANGUAGES
        languages = supported if args.language == "all" else [args.language]
        invalid = [lang for lang in languages if lang not in supported]
        if invalid:
            raise ValueError(f"{operator.upper()} 不支持语言: {', '.join(invalid)}。支持语言: {', '.join(supported)}")
        build_many(operator, languages, overwrite=args.overwrite, input_case=args.input_case)

    print("=" * 60)
    print("请求的 FST 编译完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
