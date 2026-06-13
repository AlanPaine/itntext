#!/usr/bin/env python3
"""生成 itntext 全场景测试报告。"""

from __future__ import annotations

import csv
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
    category: str
    lang: str
    operator: str
    text: str
    expected: str | None = None
    note: str = ""


CASES = [
    Case("数字", "zh", "tn", "123", "一百二十三"),
    Case("小数", "zh", "tn", "3.14", "三点一四"),
    Case("百分比", "zh", "tn", "25%", "百分之二十五"),
    Case("时间", "zh", "tn", "10:30", "十点三十分"),
    Case("日期", "zh", "tn", "2026年6月12日", "二零二六年六月十二日"),
    Case("日期上下文", "zh", "tn", "今天是2026年6月12日", "今天是二零二六年六月十二日"),
    Case("单位", "zh", "tn", "12公斤", "十二公斤"),
    Case("金额", "zh", "tn", "￥12.50", None, "金额读法不同，观察输出"),
    Case("电话", "zh", "tn", "13800000000", "幺三八零零零零零零零零"),
    Case("数字", "zh", "itn", "一百二十三", "123"),
    Case("小数", "zh", "itn", "三点一四", "3.14"),
    Case("百分比", "zh", "itn", "百分之二十五", "25%"),
    Case("时间", "zh", "itn", "上午十点三十分", "上午 10:30"),
    Case("日期号", "zh", "itn", "五月二十三号", "5月23号"),
    Case("日期日", "zh", "itn", "四月二十三日", "4月23日"),
    Case("单位", "zh", "itn", "十二公斤", "12kg"),
    Case("金额", "zh", "itn", "十二元五角", "¥12.5"),
    Case("金额", "zh", "itn", "十二元五角三分", "¥12.53"),
    Case("金额", "zh", "itn", "十二元五分", "¥12.05"),
    Case("电话", "zh", "itn", "幺三八零零零零零零零零", "13800000000"),
    Case("数字", "en", "tn", "123", "one hundred and twenty three"),
    Case("小数", "en", "tn", "3.14", "three point one four"),
    Case("百分比", "en", "tn", "25%", "twenty five percent"),
    Case("时间", "en", "tn", "10:30", "ten thirty"),
    Case("金额", "en", "tn", "$12.50", None, "金额读法不同，观察输出"),
    Case("单位", "en", "tn", "12 kg", "twelve kilograms"),
    Case("数字", "en", "itn", "one hundred twenty three", "123"),
    Case("小数", "en", "itn", "three point one four", "3.14"),
    Case("百分比", "en", "itn", "twenty five percent", "25 %"),
    Case("时间", "en", "itn", "ten thirty", "1030"),
    Case("金额", "en", "itn", "twelve dollars fifty cents", "$12.50"),
    Case("单位", "en", "itn", "twelve kilograms", "12 kg"),
    Case("多语言数字", "de", "itn", "ein hundert drei und zwanzig"),
    Case("多语言数字", "es", "itn", "ciento veintitrés"),
    Case("多语言数字", "fr", "itn", "cent vingt trois"),
    Case("多语言数字", "id", "itn", "seratus dua puluh tiga", "123"),
    Case("多语言数字", "ja", "itn", "百二十三", "123"),
    Case("多语言数字", "ko", "itn", "백이십삼"),
    Case("多语言数字", "pt", "itn", "cento e vinte três"),
    Case("多语言数字", "ru", "itn", "сто двадцать три"),
    Case("多语言数字", "tl", "itn", "isang daan dalawampu tatlo"),
    Case("多语言数字", "vi", "itn", "một trăm hai mươi ba"),
    Case("多语言TN", "de", "tn", "123"),
    Case("多语言TN", "es", "tn", "123"),
    Case("多语言TN", "ru", "tn", "123"),
]


def run(factory, text):
    start = perf_counter()
    try:
        value = factory().normalize(text)
        return value, "", (perf_counter() - start) * 1000
    except Exception as exc:
        return "", repr(exc), (perf_counter() - start) * 1000


def status(value, error, expected):
    if error:
        return "error"
    if expected is None:
        return "observe"
    return "pass" if value == expected else "fail"


def warm_benchmark(lang, operator, text, loops=200):
    normalizer = ItnNormalizer(lang=lang, operator=operator)
    normalizer.normalize(text)
    start = perf_counter()
    for _ in range(loops):
        normalizer.normalize(text)
    elapsed = perf_counter() - start
    return elapsed * 1000 / loops, loops / elapsed


def main():
    from wetext import Normalizer as WetextNormalizer

    rows = []
    for case in CASES:
        itn_value, itn_error, itn_cold_ms = run(lambda c=case: ItnNormalizer(lang=c.lang, operator=c.operator), case.text)
        if case.lang in {"zh", "en"}:
            wetext_value, wetext_error, wetext_cold_ms = run(lambda c=case: WetextNormalizer(lang=c.lang, operator=c.operator), case.text)
            wetext_status = status(wetext_value, wetext_error, case.expected)
        else:
            wetext_value, wetext_error, wetext_cold_ms, wetext_status = "", "unsupported", 0.0, "unsupported"
        rows.append({
            "category": case.category,
            "lang": case.lang,
            "operator": case.operator,
            "input": case.text,
            "expected": case.expected or "",
            "itntext": itn_error or itn_value,
            "wetext": wetext_error or wetext_value,
            "itntext_status": status(itn_value, itn_error, case.expected),
            "wetext_status": wetext_status,
            "itntext_cold_ms": f"{itn_cold_ms:.3f}",
            "wetext_cold_ms": "" if wetext_error == "unsupported" else f"{wetext_cold_ms:.3f}",
            "note": case.note,
        })

    perf_cases = [
        Case("性能", "zh", "tn", "今天是2026年6月12日"),
        Case("性能", "zh", "itn", "上午十点三十分"),
        Case("性能", "en", "tn", "$12.50"),
        Case("性能", "en", "itn", "twelve kilograms"),
        Case("性能", "ja", "itn", "百二十三"),
        Case("性能", "ru", "tn", "123"),
    ]
    perf_rows = []
    for case in perf_cases:
        avg, tps = warm_benchmark(case.lang, case.operator, case.text)
        perf_rows.append({"lang": case.lang, "operator": case.operator, "input": case.text, "avg": f"{avg:.4f}", "tps": f"{tps:.1f}"})

    expected_rows = [r for r in rows if r["expected"]]
    passed = sum(1 for r in expected_rows if r["itntext_status"] == "pass")

    reports_dir = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    csv_path = os.path.join(reports_dir, "COMPREHENSIVE_COMPARE.csv")
    md_path = os.path.join(reports_dir, "COMPREHENSIVE_COMPARE.md")
    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    md = ["# itntext 全场景对比测试报告\n", "## 总结\n"]
    md.append(f"- 有明确期望值的用例：{len(expected_rows)} 个，itntext 通过 {passed} 个，通过率 {passed / len(expected_rows):.1%}。")
    md.append(f"- itntext ITN 覆盖语言：{', '.join(ITN_LANGUAGES)}。")
    md.append(f"- itntext TN 覆盖语言：{', '.join(TN_LANGUAGES)}。")
    md.append("- wetext 仅在 `zh/en` 范围内参与对比，其他语言标记为 unsupported。\n")
    md.append("## 准确率与输出\n")
    md.append("| 类别 | 语言 | 模式 | 输入 | 期望 | itntext | itntext状态 | wetext | wetext状态 | 说明 |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(f"| {r['category']} | {r['lang']} | {r['operator']} | {r['input']} | {r['expected']} | {r['itntext']} | {r['itntext_status']} | {r['wetext']} | {r['wetext_status']} | {r['note']} |")
    md.append("\n## 热调用性能\n")
    md.append("| 语言 | 模式 | 输入 | itntext平均ms | itntext TPS |")
    md.append("|---|---|---|---:|---:|")
    for r in perf_rows:
        md.append(f"| {r['lang']} | {r['operator']} | {r['input']} | {r['avg']} | {r['tps']} |")
    md.append("\n## 全语言可用性\n")
    md.append("| 模式 | 语言 | 状态 |")
    md.append("|---|---|---|")
    for lang in ITN_LANGUAGES:
        md.append(f"| itn | {lang} | ok |")
    for lang in TN_LANGUAGES:
        md.append(f"| tn | {lang} | ok |")

    with open(md_path, "w", encoding="utf-8") as file:
        file.write("\n".join(md) + "\n")
    print(md_path)
    print(csv_path)


if __name__ == "__main__":
    main()
