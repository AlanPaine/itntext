#!/usr/bin/env python3
"""生成 itntext 与 wetext 的基础对比报告。"""

from __future__ import annotations

import inspect
import os
import sys
from dataclasses import dataclass
from time import perf_counter

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from itntext import Normalizer as ItnNormalizer
from itntext.fst_processor import ITN_LANGUAGES, TN_LANGUAGES


@dataclass
class Case:
    lang: str
    operator: str
    text: str


CASES = [
    Case("zh", "tn", "123"),
    Case("zh", "tn", "今天是2026年6月12日"),
    Case("zh", "tn", "13800000000"),
    Case("zh", "itn", "五月二十三号"),
    Case("zh", "itn", "上午十点三十分"),
    Case("zh", "itn", "十二元五角三分"),
    Case("en", "tn", "123"),
    Case("en", "tn", "$12.50"),
    Case("en", "itn", "one hundred twenty three"),
    Case("en", "itn", "twelve kilograms"),
]


def safe_call(factory, text: str):
    start = perf_counter()
    try:
        normalizer = factory()
        result = normalizer.normalize(text)
        return result, None, perf_counter() - start
    except Exception as exc:
        return "", repr(exc), perf_counter() - start


def main():
    from wetext import Normalizer as WetextNormalizer

    rows = []
    for case in CASES:
        itn_result, itn_error, itn_time = safe_call(
            lambda c=case: ItnNormalizer(lang=c.lang, operator=c.operator), case.text
        )
        wetext_result, wetext_error, wetext_time = safe_call(
            lambda c=case: WetextNormalizer(lang=c.lang, operator=c.operator), case.text
        )
        rows.append((case, itn_result, itn_error, itn_time, wetext_result, wetext_error, wetext_time))

    report = ["# itntext 与 wetext 对比报告\n", "## API 对比\n"]
    report.append(f"- itntext 构造签名：`{inspect.signature(ItnNormalizer)}`")
    report.append(f"- wetext 构造签名：`{inspect.signature(WetextNormalizer)}`")
    report.append("- itntext 调用方式保持 wetext 风格：`Normalizer(lang='zh', operator='tn').normalize(text)`")
    report.append(f"- itntext ITN 支持语言：`{', '.join(ITN_LANGUAGES)}`")
    report.append(f"- itntext TN 支持语言：`{', '.join(TN_LANGUAGES)}`\n")
    report.append("## 输出对比\n")
    report.append("| lang | operator | input | itntext | wetext | same |")
    report.append("|---|---|---|---|---|---|")
    for case, itn_result, itn_error, _, wetext_result, wetext_error, _ in rows:
        left = itn_error or itn_result
        right = wetext_error or wetext_result
        same = "yes" if left == right else "no"
        report.append(f"| {case.lang} | {case.operator} | {case.text} | {left} | {right} | {same} |")
    report.append("\n## 首次调用耗时\n")
    report.append("| lang | operator | input | itntext_ms | wetext_ms |")
    report.append("|---|---|---|---:|---:|")
    for case, _, _, itn_time, _, _, wetext_time in rows:
        report.append(f"| {case.lang} | {case.operator} | {case.text} | {itn_time * 1000:.3f} | {wetext_time * 1000:.3f} |")

    out_path = os.path.join(PROJECT_ROOT, "reports", "WETEXT_COMPARE.md")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as file:
        file.write("\n".join(report) + "\n")
    print(out_path)


if __name__ == "__main__":
    main()
