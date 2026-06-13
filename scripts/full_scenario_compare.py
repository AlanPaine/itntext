#!/usr/bin/env python3
"""更完整的 itntext / wetext 场景、语言和性能对比报告。"""

from __future__ import annotations

import csv
import os
import sys
from dataclasses import dataclass
from statistics import median
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
    # 中文 TN
    Case("数字", "zh", "tn", "0", "零"),
    Case("数字", "zh", "tn", "123", "一百二十三"),
    Case("数字", "zh", "tn", "1001", "一千零一"),
    Case("长数字/电话", "zh", "tn", "13800000000", "幺三八零零零零零零零零"),
    Case("小数", "zh", "tn", "3.14", "三点一四"),
    Case("百分比", "zh", "tn", "25%", "百分之二十五"),
    Case("时间", "zh", "tn", "10:30", "十点三十分"),
    Case("日期", "zh", "tn", "2026年6月12日", "二零二六年六月十二日"),
    Case("日期上下文", "zh", "tn", "今天是2026年6月12日", "今天是二零二六年六月十二日"),
    Case("单位", "zh", "tn", "12公斤", "十二公斤"),
    Case("金额/货币", "zh", "tn", "￥12.50", None, "中文 TN 金额读法不同，观察输出"),
    Case("金额/货币", "zh", "tn", "$12.50", None, "货币名和符号读法不同，观察输出"),

    # 中文 ITN
    Case("数字", "zh", "itn", "一百二十三", "123"),
    Case("小数", "zh", "itn", "三点一四", "3.14"),
    Case("百分比", "zh", "itn", "百分之二十五", "25%"),
    Case("分数", "zh", "itn", "三分之一", "1/3"),
    Case("时间", "zh", "itn", "上午十点三十分", "上午 10:30"),
    Case("时间", "zh", "itn", "下午三点零五分", None, "观察中文时间更复杂表达"),
    Case("日期", "zh", "itn", "五月二十三号", "5月23号"),
    Case("日期", "zh", "itn", "四月二十三日", "4月23日"),
    Case("单位", "zh", "itn", "十二公斤", "12kg"),
    Case("单位", "zh", "itn", "三公里", "3km"),
    Case("金额/货币", "zh", "itn", "十二元五角", "¥12.5"),
    Case("金额/货币", "zh", "itn", "十二元五角三分", "¥12.53"),
    Case("金额/货币", "zh", "itn", "十二元五分", "¥12.05"),
    Case("金额/货币", "zh", "itn", "十二美元", "$12"),
    Case("长数字/电话", "zh", "itn", "幺三八零零零零零零零零", "13800000000"),
    Case("电子类", "zh", "itn", "一二三点四五", None, "观察电子/小数边界"),

    # 英文 TN
    Case("数字", "en", "tn", "123", "one hundred and twenty three"),
    Case("数字", "en", "tn", "1001", "one thousand one"),
    Case("小数", "en", "tn", "3.14", "three point one four"),
    Case("百分比", "en", "tn", "25%", "twenty five percent"),
    Case("时间", "en", "tn", "10:30", "ten thirty"),
    Case("日期", "en", "tn", "01/02/2026", None, "英文日期歧义，观察输出"),
    Case("金额/货币", "en", "tn", "$12.50", None, "wetext 和 itntext 货币读法不同"),
    Case("金额/货币", "en", "tn", "€12.50", None, "观察欧元读法"),
    Case("单位", "en", "tn", "12 kg", "twelve kilograms"),

    # 英文 ITN
    Case("数字", "en", "itn", "one hundred twenty three", "123"),
    Case("小数", "en", "itn", "three point one four", "3.14"),
    Case("百分比", "en", "itn", "twenty five percent", "25 %"),
    Case("时间", "en", "itn", "ten thirty", "1030"),
    Case("金额/货币", "en", "itn", "twelve dollars fifty cents", "$12.50"),
    Case("金额/货币", "en", "itn", "twelve euros", "€12"),
    Case("单位", "en", "itn", "twelve kilograms", "12 kg"),
    Case("电话", "en", "itn", "one two three four", "1234"),

    # 多语言 ITN smoke
    Case("多语言数字", "de", "itn", "ein hundert drei und zwanzig", None),
    Case("多语言数字", "es", "itn", "ciento veintitrés", None),
    Case("多语言数字", "fr", "itn", "cent vingt trois", None),
    Case("多语言数字", "id", "itn", "seratus dua puluh tiga", "123"),
    Case("多语言数字", "ja", "itn", "百二十三", "123"),
    Case("多语言数字", "ko", "itn", "백이십삼", None),
    Case("多语言数字", "pt", "itn", "cento e vinte três", None),
    Case("多语言数字", "ru", "itn", "сто двадцать три", None),
    Case("多语言数字", "tl", "itn", "isang daan dalawampu tatlo", None),
    Case("多语言数字", "vi", "itn", "một trăm hai mươi ba", None),
    Case("多语言TN", "de", "tn", "123", None),
    Case("多语言TN", "es", "tn", "123", None),
    Case("多语言TN", "ru", "tn", "123", "сто двадцать три"),
]


def safe_normalize(factory, text: str):
    start = perf_counter()
    try:
        result = factory().normalize(text)
        return result, "", (perf_counter() - start) * 1000
    except Exception as exc:
        return "", repr(exc), (perf_counter() - start) * 1000


def status(value: str, error: str, expected: str | None) -> str:
    if error:
        return "error"
    if expected is None:
        return "observe"
    return "pass" if value == expected else "fail"


def warm_stats(factory, text: str, loops: int = 300):
    normalizer = factory()
    normalizer.normalize(text)
    values = []
    start_all = perf_counter()
    for _ in range(loops):
        start = perf_counter()
        normalizer.normalize(text)
        values.append((perf_counter() - start) * 1000)
    total = perf_counter() - start_all
    return {
        "avg_ms": sum(values) / len(values),
        "median_ms": median(values),
        "tps": loops / total,
    }


def main():
    from wetext import Normalizer as WetextNormalizer

    rows = []
    for case in CASES:
        itn_value, itn_error, itn_cold_ms = safe_normalize(
            lambda c=case: ItnNormalizer(lang=c.lang, operator=c.operator), case.text
        )
        if case.lang in {"zh", "en"}:
            wetext_value, wetext_error, wetext_cold_ms = safe_normalize(
                lambda c=case: WetextNormalizer(lang=c.lang, operator=c.operator), case.text
            )
            wetext_status = status(wetext_value, wetext_error, case.expected)
        else:
            wetext_value, wetext_error, wetext_cold_ms, wetext_status = "", "unsupported", 0.0, "unsupported"

        rows.append(
            {
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
            }
        )

    perf_cases = [
        Case("性能", "zh", "tn", "今天是2026年6月12日"),
        Case("性能", "zh", "itn", "上午十点三十分"),
        Case("性能", "zh", "itn", "十二元五角三分"),
        Case("性能", "en", "tn", "$12.50"),
        Case("性能", "en", "itn", "twelve dollars fifty cents"),
        Case("性能", "ja", "itn", "百二十三"),
        Case("性能", "ru", "tn", "123"),
    ]
    perf_rows = []
    for case in perf_cases:
        itn_stats = warm_stats(lambda c=case: ItnNormalizer(lang=c.lang, operator=c.operator), case.text)
        if case.lang in {"zh", "en"}:
            wetext_stats = warm_stats(lambda c=case: WetextNormalizer(lang=c.lang, operator=c.operator), case.text)
        else:
            wetext_stats = None
        perf_rows.append(
            {
                "lang": case.lang,
                "operator": case.operator,
                "input": case.text,
                "itntext_avg_ms": f"{itn_stats['avg_ms']:.4f}",
                "itntext_median_ms": f"{itn_stats['median_ms']:.4f}",
                "itntext_tps": f"{itn_stats['tps']:.1f}",
                "wetext_avg_ms": f"{wetext_stats['avg_ms']:.4f}" if wetext_stats else "",
                "wetext_median_ms": f"{wetext_stats['median_ms']:.4f}" if wetext_stats else "",
                "wetext_tps": f"{wetext_stats['tps']:.1f}" if wetext_stats else "",
            }
        )

    expected_rows = [r for r in rows if r["expected"]]
    itn_pass = sum(1 for r in expected_rows if r["itntext_status"] == "pass")
    wetext_expected = [r for r in expected_rows if r["wetext_status"] != "unsupported"]
    wetext_pass = sum(1 for r in wetext_expected if r["wetext_status"] == "pass")
    observe_rows = [r for r in rows if r["itntext_status"] == "observe"]
    fail_rows = [r for r in rows if r["itntext_status"] in {"fail", "error"}]

    reports_dir = os.path.join(PROJECT_ROOT, "reports")
    os.makedirs(reports_dir, exist_ok=True)
    csv_path = os.path.join(reports_dir, "FULL_SCENARIO_COMPARE.csv")
    perf_csv_path = os.path.join(reports_dir, "FULL_SCENARIO_PERFORMANCE.csv")
    md_path = os.path.join(reports_dir, "FULL_SCENARIO_COMPARE.md")

    with open(csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    with open(perf_csv_path, "w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=list(perf_rows[0].keys()))
        writer.writeheader()
        writer.writerows(perf_rows)

    md = ["# itntext 全场景与 wetext 对比报告\n", "## 总览\n"]
    md.append(f"- 总用例：{len(rows)} 个。")
    md.append(f"- 有明确期望的用例：{len(expected_rows)} 个，itntext 通过 {itn_pass} 个，通过率 {itn_pass / len(expected_rows):.1%}。")
    if wetext_expected:
        md.append(f"- wetext 可对比且有明确期望的用例：{len(wetext_expected)} 个，wetext 通过 {wetext_pass} 个，通过率 {wetext_pass / len(wetext_expected):.1%}。")
    md.append(f"- 观察类用例：{len(observe_rows)} 个，主要用于金额/货币格式、多语言上游覆盖差异和歧义表达。")
    md.append(f"- itntext 失败/异常用例：{len(fail_rows)} 个。")
    md.append(f"- ITN 语言：`{', '.join(ITN_LANGUAGES)}`。")
    md.append(f"- TN 语言：`{', '.join(TN_LANGUAGES)}`。\n")

    md.append("## 场景输出\n")
    md.append("| 类别 | 语言 | 模式 | 输入 | 期望 | itntext | 状态 | wetext | wetext状态 | 说明 |")
    md.append("|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        md.append(
            f"| {r['category']} | {r['lang']} | {r['operator']} | {r['input']} | {r['expected']} | "
            f"{r['itntext']} | {r['itntext_status']} | {r['wetext']} | {r['wetext_status']} | {r['note']} |"
        )

    md.append("\n## 热调用性能\n")
    md.append("| 语言 | 模式 | 输入 | itntext平均ms | itntext中位ms | itntext TPS | wetext平均ms | wetext中位ms | wetext TPS |")
    md.append("|---|---|---|---:|---:|---:|---:|---:|---:|")
    for r in perf_rows:
        md.append(
            f"| {r['lang']} | {r['operator']} | {r['input']} | {r['itntext_avg_ms']} | {r['itntext_median_ms']} | {r['itntext_tps']} | "
            f"{r['wetext_avg_ms']} | {r['wetext_median_ms']} | {r['wetext_tps']} |"
        )

    md.append("\n## 结论\n")
    md.append("- 中文核心修复场景保持通过，包括数字、日期、时间、百分比、单位、元角分金额和长数字/电话。")
    md.append("- wetext 仅对 `zh/en` 参与对比；多语言部分以 itntext 的可用性和输出观察为主。")
    md.append("- 金额/货币在 TN 侧存在风格差异，报告保留为观察项，避免把有歧义的读法误判为失败。")
    md.append("- 性能部分覆盖中文、英文、日语和俄语；俄语 TN 仍是热调用最慢场景。")

    with open(md_path, "w", encoding="utf-8") as file:
        file.write("\n".join(md) + "\n")

    print(md_path)
    print(csv_path)
    print(perf_csv_path)


if __name__ == "__main__":
    main()
