#!/usr/bin/env python3
"""Generate comprehensive test report comparing itntext vs wetext."""

import json
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import wetext


def benchmark(normalizer, texts, rounds=5):
    times = []
    for _ in range(rounds):
        start = time.perf_counter()
        for t in texts:
            normalizer.normalize(t)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    return min(times), sum(times) / len(times), max(times)


def main():
    print("=" * 60)
    print("itntext vs wetext Comprehensive Test Report")
    print("=" * 60)

    # Document wetext known issues
    wetext_norm = wetext.Normalizer(lang="zh", operator="itn")

    bug_cases = [
        ("四月二十三日", "4月23日"),
        ("五月二十三号", "5月23号"),
        ("二零二四年四月二十三日", "2024年4月23日"),
        ("二零二五年一月一日", "2025年1月1日"),
        ("我们约在四月二十三日见面", "我们约在4月23日见面"),
        ("活动时间是五月二十三号到六月一日", "活动时间是5月23号到6月1日"),
        ("身高是一米七五", "身高是1.75m"),
        ("我的密码是零一二三四五六", "我的密码是0123456"),
    ]

    print("\n## 1. Known WeText Issues (Documented)")
    print("-" * 40)
    for inp, expected in bug_cases:
        actual = wetext_norm.normalize(inp)
        status = "PASS" if actual == expected else "FAIL"
        print(f"[{status}] {inp!r}")
        print(f"       wetext:  {actual!r}")
        print(f"       expected: {expected!r}")
        print()

    # Performance benchmark
    bench_texts = [
        "四月二十三日",
        "二零二四年四月二十三日",
        "身高是一米七五",
        "我的密码是零一二三四五六",
        "一百美元",
        "上午十点三十分",
    ] * 100

    print("\n## 2. Performance Benchmark")
    print("-" * 40)
    wetext_min, wetext_avg, wetext_max = benchmark(wetext_norm, bench_texts)
    print(f"WeText:  min={wetext_min:.3f}s avg={wetext_avg:.3f}s max={wetext_max:.3f}s ({len(bench_texts)} sentences)")

    # Additional test cases
    print("\n## 3. Additional Test Cases")
    print("-" * 40)
    additional = [
        ("一千零五", "1005"),
        ("百分之二十五", "25%"),
        ("三点一四", "3.14"),
        ("四分之三", "3/4"),
        ("BTC价格三万美金", "BTC价格30000美金"),
    ]
    for inp, expected in additional:
        actual = wetext_norm.normalize(inp)
        status = "PASS" if actual == expected else "FAIL"
        print(f"[{status}] {inp!r} -> {actual!r} (expected: {expected!r})")

    print("\n" + "=" * 60)
    print("Report generation complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
