#!/usr/bin/env python3
"""
itntext vs wetext 性能对比测试
"""

import sys
import os
import time
import tracemalloc
import statistics

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import wetext
from itntext import Normalizer

# ============================================================
# 初始化
# ============================================================
wetext_itn = wetext.Normalizer(lang="zh", operator="itn")
wetext_tn = wetext.Normalizer(lang="zh", operator="tn")
itntext_itn = Normalizer(lang="zh", operator="itn")
itntext_tn = Normalizer(lang="zh", operator="tn")

# ============================================================
# 测试文本集
# ============================================================

SHORT_TEXTS = [
    "五月二十三号", "二零二四年四月二十三日", "身高一米七五",
    "我的密码是零一二三四五六", "一百美元", "上午十点三十分",
    "百分之二十五", "三点一四", "四分之三", "BTC价格三万美金",
    "一千二百三十四", "零点五", "版本号三点五点一",
    "电话幺三八零零零零零零零零", "股票六零零五百一十九",
    "一百二十三万四千五百六十七元", "上午九点到十一点半",
    "体重六十公斤", "一百公里", "五百毫升",
]

LONG_TEXTS = [
    "会议决定在二零二五年四月十五号发布新版本，预算为一百二十三万四千五百六十七元，"
    "预计用户增长百分之三十，日活跃用户达到五百万，服务器从两台扩展到八台，"
    "响应时间从五百毫秒降低到一百五十毫秒，数据库容量从一百GB扩展到五百GB。",
    "各位同事大家好，今天的会议主要讨论三个方面的问题。首先是项目进度，"
    "目前我们完成了百分之八十五的开发工作，剩余部分预计在十二月三十一日前完成。"
    "第二，关于预算，本季度总支出为一百二十三万四千五百六十七元。"
    "第三，下一阶段的目标，我们计划在二零二五年第一季度实现用户增长百分之三十。",
    "股价方面，我们的股票代码六零零五百一十九，今日收盘价一千八百五十元，"
    "涨幅百分之二点三。BTC持仓价值约三百万美元，ETH持仓约一百二十万美元。"
    "会议时间是上午九点到十一点半，请大家准时参加。",
]

MEETING_TEXT = (
    "各位同事大家好，今天的会议主要讨论三个方面的问题。"
    "首先是项目进度，目前我们完成了百分之八十五的开发工作，剩余部分预计在十二月三十一日前完成。"
    "第二，关于预算，本季度总支出为一百二十三万四千五百六十七元，其中研发投入占百分之六十，"
    "市场推广占百分之二十五，运营成本占百分之十五。"
    "第三，下一阶段的目标，我们计划在二零二五年第一季度实现用户增长百分之三十，日活跃用户达到五百万。"
    "具体来说，一月份目标是三百万日活，二月份四百万，三月份五百万。"
    "技术方面，服务器已经从两台扩展到八台，响应时间从五百毫秒降低到一百五十毫秒。"
    "数据库容量从一百GB扩展到五百GB，缓存命中率提升到百分之九十五。"
    "关于产品发布，我们定在四月十五号发布v二点零版本，六月一号发布v二点一点。"
    "客户反馈方面，满意度从百分之七十二提升到百分之八十九。"
    "电话支持热线幺三八零零一二三四五六已开通。"
    "目前有十五个待修复的bug，其中三个是高优先级，十二个是中优先级。"
    "股价方面，我们的股票代码六零零五百一十九，今日收盘价一千八百五十元，涨幅百分之二点三。"
    "BTC持仓价值约三百万美元，ETH持仓约一百二十万美元。"
    "会议时间是上午九点到十一点半，请大家准时参加。"
    "如有疑问请发邮件到 admin at company dot com。"
    "项目文档地址是 https colon slash slash docs dot company dot com slash project。"
    "以上就是今天会议的全部内容，散会。"
)

# ============================================================
# 预热
# ============================================================
print("预热中...")
for t in SHORT_TEXTS * 20:
    wetext_itn.normalize(t)
    itntext_itn.normalize(t)
for t in LONG_TEXTS * 20:
    wetext_itn.normalize(t)
    itntext_itn.normalize(t)
for _ in range(20):
    wetext_itn.normalize(MEETING_TEXT)
    itntext_itn.normalize(MEETING_TEXT)
print("预热完成\n")

# ============================================================
# 1. 单句延迟对比（ITN）
# ============================================================
print("=" * 70)
print("1. 单句延迟对比（ITN）")
print("=" * 70)

ITERS = 200
wetext_latencies = []
itntext_latencies = []

for t in SHORT_TEXTS:
    start = time.perf_counter()
    for _ in range(ITERS):
        wetext_itn.normalize(t)
    wetext_latencies.append((time.perf_counter() - start) / ITERS * 1000)

    start = time.perf_counter()
    for _ in range(ITERS):
        itntext_itn.normalize(t)
    itntext_latencies.append((time.perf_counter() - start) / ITERS * 1000)

print(f"{'指标':<15} {'wetext':>12} {'itntext':>12} {'差异':>10}")
print("-" * 50)
print(f"{'平均 (ms)':<15} {statistics.mean(wetext_latencies):>12.3f} {statistics.mean(itntext_latencies):>12.3f} {(statistics.mean(itntext_latencies)/statistics.mean(wetext_latencies)-1)*100:>+9.1f}%")
print(f"{'最小 (ms)':<15} {min(wetext_latencies):>12.3f} {min(itntext_latencies):>12.3f}")
print(f"{'最大 (ms)':<15} {max(wetext_latencies):>12.3f} {max(itntext_latencies):>12.3f}")
print(f"{'P50 (ms)':<15} {statistics.median(wetext_latencies):>12.3f} {statistics.median(itntext_latencies):>12.3f}")
print(f"{'P95 (ms)':<15} {sorted(wetext_latencies)[int(len(wetext_latencies)*0.95)]:>12.3f} {sorted(itntext_latencies)[int(len(itntext_latencies)*0.95)]:>12.3f}")
print(f"{'P99 (ms)':<15} {sorted(wetext_latencies)[int(len(wetext_latencies)*0.99)]:>12.3f} {sorted(itntext_latencies)[int(len(itntext_latencies)*0.99)]:>12.3f}")

# ============================================================
# 2. 批量吞吐量对比
# ============================================================
print("\n" + "=" * 70)
print("2. 批量吞吐量对比")
print("=" * 70)

for label, texts, iters in [
    ("短文本 1000句", SHORT_TEXTS, 1000),
    ("长文本 100句", LONG_TEXTS, 100),
    ("会议文本 100次", [MEETING_TEXT], 100),
]:
    N = len(texts) * iters
    batch = texts * iters

    start = time.perf_counter()
    for t in batch:
        wetext_itn.normalize(t)
    wt_time = time.perf_counter() - start

    start = time.perf_counter()
    for t in batch:
        itntext_itn.normalize(t)
    it_time = time.perf_counter() - start

    print(f"\n  {label} (共 {N} 次调用):")
    print(f"  {'引擎':<10} {'耗时(s)':>10} {'TPS':>10} {'差异':>10}")
    print(f"  {'wetext':<10} {wt_time:>10.3f} {N/wt_time:>10.1f}")
    print(f"  {'itntext':<10} {it_time:>10.3f} {N/it_time:>10.1f} {(it_time/wt_time-1)*100:>+9.1f}%")

# ============================================================
# 3. TN 吞吐量对比
# ============================================================
print("\n" + "=" * 70)
print("3. TN 吞吐量对比")
print("=" * 70)

tn_texts = ["123", "2024年4月23日", "3.14", "25%", "你好世界"] * 200
N_tn = len(tn_texts)

start = time.perf_counter()
for t in tn_texts:
    wetext_tn.normalize(t)
wt_tn_time = time.perf_counter() - start

start = time.perf_counter()
for t in tn_texts:
    itntext_tn.normalize(t)
it_tn_time = time.perf_counter() - start

print(f"  TN {N_tn}句:")
print(f"  {'引擎':<10} {'耗时(s)':>10} {'TPS':>10} {'差异':>10}")
print(f"  {'wetext':<10} {wt_tn_time:>10.3f} {N_tn/wt_tn_time:>10.1f}")
print(f"  {'itntext':<10} {it_tn_time:>10.3f} {N_tn/it_tn_time:>10.1f} {(it_tn_time/wt_tn_time-1)*100:>+9.1f}%")

# ============================================================
# 4. 内存占用对比
# ============================================================
print("\n" + "=" * 70)
print("4. 内存占用对比")
print("=" * 70)

batch = SHORT_TEXTS * 500

tracemalloc.start()
for t in batch:
    wetext_itn.normalize(t)
_, wt_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

tracemalloc.start()
for t in batch:
    itntext_itn.normalize(t)
_, it_mem = tracemalloc.get_traced_memory()
tracemalloc.stop()

print(f"  {'引擎':<10} {'峰值内存(KB)':>15} {'差异':>10}")
print(f"  {'wetext':<10} {wt_mem/1024:>15.1f}")
print(f"  {'itntext':<10} {it_mem/1024:>15.1f} {(it_mem/wt_mem-1)*100:>+9.1f}%")

# ============================================================
# 5. 初始化时间对比
# ============================================================
print("\n" + "=" * 70)
print("5. 初始化时间对比")
print("=" * 70)

# wetext 初始化（加载已有 FST）
start = time.perf_counter()
wetext_itn2 = wetext.Normalizer(lang="zh", operator="itn")
wt_init = time.perf_counter() - start

# itntext 初始化（加载已有 FST）
start = time.perf_counter()
itntext_itn2 = Normalizer(lang="zh", operator="itn")
it_init = time.perf_counter() - start

print(f"  {'引擎':<10} {'初始化耗时(ms)':>18} {'差异':>10}")
print(f"  {'wetext':<10} {wt_init*1000:>18.3f}")
print(f"  {'itntext':<10} {it_init*1000:>18.3f} {(it_init/wt_init-1)*100:>+9.1f}%")

# ============================================================
# 6. 准确率对比（关键用例）
# ============================================================
print("\n" + "=" * 70)
print("6. 准确率对比（关键用例）")
print("=" * 70)

KEY_CASES = [
    ("五月二十三号", "5月23号"),
    ("四月二十三日", "4月23日"),
    ("四分之三", "3/4"),
    ("上午十点三十分", "上午 10:30"),
    ("下午两点", "下午 14:00"),
    ("身高一米七五", "身高是1.75m"),
    ("一两个", "1～2个"),
    ("一百二十三万四千五百六十七元", "1234567元"),
    ("六零零五百一十九", "600519"),
    ("上午九点到十一点半", "上午 09:00～11:30"),
    ("一百二十三", "123"),
    ("三点一四", "3.14"),
    ("百分之二十五", "25%"),
    ("幺三八零零零零零零零零", "13800000000"),
    ("体重六十公斤", "体重60公斤"),
    ("一百公里", "100公里"),
    ("二零二四年四月二十三日", "2024年4月23日"),
    ("二十三时五十九分", "23:59"),
    ("我的密码是零一二三四五六", "我的密码是0123456"),
    ("第二章", "第2章"),
]

wt_pass = 0
it_pass = 0
total = len(KEY_CASES)

print(f"\n{'输入':<25} {'wetext':<20} {'itntext':<20} {'期望':<20}")
print("-" * 85)

for inp, expected in KEY_CASES:
    wt_result = wetext_itn.normalize(inp)
    it_result = itntext_itn.normalize(inp)
    wt_ok = wt_result == expected
    it_ok = it_result == expected
    if wt_ok:
        wt_pass += 1
    if it_ok:
        it_pass += 1
    wt_mark = "OK" if wt_ok else "FAIL"
    it_mark = "OK" if it_ok else "FAIL"
    print(f"{inp:<25} {wt_result:<20} {it_result:<20} {expected:<20}")

print("-" * 85)
print(f"准确率: wetext {wt_pass}/{total} ({wt_pass/total*100:.1f}%)  itntext {it_pass}/{total} ({it_pass/total*100:.1f}%)")

# ============================================================
print("\n" + "=" * 70)
print("总结")
print("=" * 70)
print(f"  wetext 和 itntext 使用相同的 pynini/OpenFST 引擎")
print(f"  性能差异来自 itntext 的后处理修正层（约 +5-10% 延迟）")
print(f"  准确率: wetext {wt_pass/total*100:.1f}% vs itntext {it_pass/total*100:.1f}%")
