#!/usr/bin/env python3
"""
itntext 全面测试：覆盖各种边缘场景，与 wetext 对比
"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from itntext import Normalizer
import wetext

PASS = 0
FAIL = 0
ERRORS = []


def check(name, inp, expected_itn, actual_itn, expected_wt=None, actual_wt=None):
    global PASS, FAIL, ERRORS
    ok = actual_itn == expected_itn
    if expected_wt is not None:
        ok = ok and (actual_wt == expected_wt)
    if ok:
        PASS += 1
    else:
        FAIL += 1
        ERRORS.append({"name": name, "input": inp, "expected": expected_itn, "actual": actual_itn, "wt": actual_wt})
        print(f"  [FAIL] {name}: {inp!r}")
        if actual_itn != expected_itn:
            print(f"         itntext 期望: {expected_itn!r}")
            print(f"         itntext 实际: {actual_itn!r}")
        if expected_wt is not None and actual_wt != expected_wt:
            print(f"         wetext  期望: {expected_wt!r}")
            print(f"         wetext  实际: {actual_wt!r}")


# ============================================================
print("=" * 70)
print("1. ITN 基础场景")
print("=" * 70)
# ============================================================
itn = Normalizer(lang="zh", operator="itn")
wt_itn = wetext.Normalizer(lang="zh", operator="itn")

itn_cases = [
    # 日期
    ("日期_号", "五月二十三号", "5月23号"),
    ("日期_日", "四月二十三日", "4月23日"),
    ("日期_年", "二零二四年四月二十三日", "2024年4月23日"),
    ("日期_一月", "一月一号", "1月1号"),
    ("日期_十二月", "十二月三十一号", "12月31号"),
    ("日期_零月", "二零二三年零一月零一日", "2023年1月1日"),
    # 时间
    ("时间_上午", "上午十点三十分", "上午 10:30"),
    ("时间_下午", "下午两点", "下午 14:00"),
    ("时间_24h", "二十三时五十九分", "23:59"),
    ("时间_零点", "零点零分", "0:00"),
    ("时间_区间", "上午九点到十一点半", "上午 09:00～11:30"),
    ("时间_下午区间", "下午两点到五点", "下午 14:00～17:00"),
    # 数字
    ("基数", "一百二十三", "123"),
    ("小数", "三点一四", "3.14"),
    ("百分比", "百分之二十五", "25%"),
    ("分数", "四分之三", "3/4"),
    ("负数", "负五", "-5"),
    ("零", "零", "0"),
    ("大数", "一亿", "100000000"),
    ("大金额", "一百二十三万四千五百六十七元", "1234567元"),
    # 电话/股票
    ("电话", "幺三八零零零零零零零零", "13800000000"),
    ("股票", "六零零五百一十九", "600519"),
    ("12306", "一二二三百零六", "12306"),
    # 单位
    ("kg", "体重六十公斤", "体重60公斤"),
    ("km", "一百公里", "100公里"),
    ("ml", "五百毫升", "500毫升"),
    # 其他
    ("身高", "身高一米七五", "身高是1.75m"),
    ("范围", "一两个", "1～2个"),
    ("序号", "第二章", "第2章"),
    ("密码", "我的密码是零一二三四五六", "我的密码是0123456"),
]

for name, inp, expected in itn_cases:
    actual = itn.normalize(inp)
    wt = wt_itn.normalize(inp)
    check(name, inp, expected, actual)

# ============================================================
print("\n" + "=" * 70)
print("2. TN 基础场景")
print("=" * 70)
# ============================================================
tn = Normalizer(lang="zh", operator="tn")
wt_tn = wetext.Normalizer(lang="zh", operator="tn")

tn_cases = [
    ("数字", "123", "一百二十三"),
    ("日期", "2024年4月23日", "二零二四年四月二十三日"),
    ("小数", "3.14", "三点一四"),
    ("百分比", "25%", "百分之二十五"),
    ("版本号", "1.0", "一点零"),
    ("英文数字", "WeTextProcessing 2.0", "WeTextProcessing 二点零"),
    ("666", "简直666", "简直六百六十六"),
    ("带标点", "你好，世界！", "你好，世界！"),
    ("全角数字", "１２３", "一百二十三"),
]

for name, inp, expected in tn_cases:
    actual = tn.normalize(inp)
    wt = wt_tn.normalize(inp)
    check(name, inp, expected, actual, expected, wt)

# ============================================================
print("\n" + "=" * 70)
print("3. TN 参数组合")
print("=" * 70)
# ============================================================

# remove_erhua
tn_erhua = Normalizer(lang="zh", operator="tn", remove_erhua=True)
wt_erhua = wetext.Normalizer(lang="zh", operator="tn", remove_erhua=True)
for inp, exp in [("花儿", "花"), ("这儿", "这"), ("那儿", "那")]:
    actual = tn_erhua.normalize(inp)
    wt = wt_erhua.normalize(inp)
    check(f"去儿化_{inp}", inp, exp, actual, exp, wt)

# remove_puncts
tn_nopunct = Normalizer(lang="zh", operator="tn", remove_puncts=True)
wt_nopunct = wetext.Normalizer(lang="zh", operator="tn", remove_puncts=True)
for inp, exp in [("你好，世界！", "你好世界"), ("价格是3.14元。", "价格是314元")]:
    actual = tn_nopunct.normalize(inp)
    wt = wt_nopunct.normalize(inp)
    check(f"去标点_{inp}", inp, exp, actual, exp, wt)

# full_to_half
tn_f2h = Normalizer(lang="zh", operator="tn", full_to_half=True)
wt_f2h = wetext.Normalizer(lang="zh", operator="tn", full_to_half=True)
for inp, exp in [("ＡＢＣ１２３", "ABC123"), ("版本２.０", "版本2.0")]:
    actual = tn_f2h.normalize(inp)
    wt = wt_f2h.normalize(inp)
    check(f"全角半角_{inp}", inp, exp, actual, exp, wt)

# traditional_to_simple
tn_t2s = Normalizer(lang="zh", operator="tn", traditional_to_simple=True)
wt_t2s = wetext.Normalizer(lang="zh", operator="tn", traditional_to_simple=True)
for inp, exp in [("這是測試", "这是测试"), ("你好", "你好")]:
    actual = tn_t2s.normalize(inp)
    wt = wt_t2s.normalize(inp)
    check(f"繁简_{inp}", inp, exp, actual, exp, wt)

# remove_interjections
tn_nointerj = Normalizer(lang="zh", operator="tn", remove_interjections=True)
wt_nointerj = wetext.Normalizer(lang="zh", operator="tn", remove_interjections=True)
for inp, exp in [("嗯一百二十三", "一百二十三"), ("啊你好", "你好")]:
    actual = tn_nointerj.normalize(inp)
    wt = wt_nointerj.normalize(inp)
    check(f"去语气词_{inp}", inp, exp, actual, exp, wt)

# 组合参数
tn_combo = Normalizer(lang="zh", operator="tn", remove_erhua=True, full_to_half=True)
wt_combo = wetext.Normalizer(lang="zh", operator="tn", remove_erhua=True, full_to_half=True)
for inp, exp in [("ＡＢＣ花儿", "ABC花")]:
    actual = tn_combo.normalize(inp)
    wt = wt_combo.normalize(inp)
    check(f"组合_{inp}", inp, exp, actual, exp, wt)

# ============================================================
print("\n" + "=" * 70)
print("4. ITN 参数组合")
print("=" * 70)
# ============================================================

# enable_0_to_9
itn_09 = Normalizer(lang="zh", operator="itn", enable_0_to_9=True)
wt_09 = wetext.Normalizer(lang="zh", operator="itn", enable_0_to_9=True)
for inp, exp in [("零一二三", "0123"), ("五", "5")]:
    actual = itn_09.normalize(inp)
    wt = wt_09.normalize(inp)
    check(f"0-9_{inp}", inp, exp, actual, exp, wt)

# remove_interjections
itn_nointerj = Normalizer(lang="zh", operator="itn", remove_interjections=True)
wt_nointerj = wetext.Normalizer(lang="zh", operator="itn", remove_interjections=True)
for inp, exp in [("嗯一百二十三", "123"), ("啊你好", "你好")]:
    actual = itn_nointerj.normalize(inp)
    wt = wt_nointerj.normalize(inp)
    check(f"ITN去语气词_{inp}", inp, exp, actual, exp, wt)

# ============================================================
print("\n" + "=" * 70)
print("5. 边缘场景")
print("=" * 70)
# ============================================================

edge_cases = [
    # 空字符串
    ("空字符串", "", ""),
    # 纯英文
    ("纯英文", "hello world", "hello world"),
    # 纯数字
    ("纯数字", "12345", "12345"),
    # 混合文本
    ("混合", "hello 世界 123", "hello 世界 123"),
    # 特殊字符
    ("特殊字符", "@#$%", "@#$%"),
    # 长文本
    ("长文本", "二零二四年五月二十三号上午十点三十分", "2024年5月23号上午 10:30"),
    # 重复数字
    ("重复数字", "六六六", "666"),
    # 连续日期
    ("连续日期", "五月二十三号到六月一号", "5月23号到6月1号"),
    # 带单位数字
    ("带单位", "一百公里每小时", "100公里每小时"),
    # 小数金额
    ("小数金额", "三点五元", "3.5元"),
    # 零金额
    ("零金额", "零元", "0元"),
    # 超大数字
    ("超大数", "一亿二千三百四十五万六千七百八十九", "123456789"),
    # 电话号码
    ("电话", "幺零零八六", "10086"),
    # 身份证号
    ("身份证", "三二零一零二一九九零零一零一零一零一", "320102199001010101"),
    # 车牌
    ("车牌", "京A一二三四五", "京A12345"),
    # 温度
    ("温度", "二十五摄氏度", "25摄氏度"),
    # 面积
    ("面积", "一百平方米", "100平方米"),
    # 体积
    ("体积", "五百毫升", "500毫升"),
]

for name, inp, expected in edge_cases:
    actual = itn.normalize(inp)
    check(name, inp, expected, actual)

# ============================================================
print("\n" + "=" * 70)
print("6. 已知问题验证（itntext 改进项）")
print("=" * 70)
# ============================================================

improvements = [
    ("日期_号保留", "五月二十三号", "5月23号", "05/23"),
    ("日期_日保留", "四月二十三日", "4月23日", "04/23"),
    ("时间_上午格式", "上午十点三十分", "上午 10:30", "10:30a.m."),
    ("时间_下午格式", "下午两点", "下午 14:00", "下午两点"),
    ("身高", "身高一米七五", "身高是1.75m", "身高1m七五"),
    ("范围", "一两个", "1～2个", "一2个"),
    ("大金额", "一百二十三万四千五百六十七元", "1234567元", "¥123万4567"),
    ("股票", "六零零五百一十九", "600519", "600 519"),
    ("时间区间", "上午九点到十一点半", "上午 09:00～11:30", "上午九点到11:30"),
]

for name, inp, itn_expected, wt_expected in improvements:
    actual = itn.normalize(inp)
    wt = wt_itn.normalize(inp)
    ok = actual == itn_expected
    if ok:
        PASS += 1
        print(f"  [OK] {name}: itntext={actual!r} (wetext={wt!r})")
    else:
        FAIL += 1
        ERRORS.append({"name": name, "input": inp, "expected": itn_expected, "actual": actual})
        print(f"  [FAIL] {name}: {inp!r}")
        print(f"         itntext 期望: {itn_expected!r}")
        print(f"         itntext 实际: {actual!r}")
        print(f"         wetext  实际: {wt!r}")

# ============================================================
print("\n" + "=" * 70)
print(f"测试结果: {PASS} 通过, {FAIL} 失败, 共 {PASS+FAIL} 个")
print("=" * 70)

if ERRORS:
    print("\n失败用例:")
    for e in ERRORS:
        print(f"  [{e['name']}] {e['input']!r}")
        print(f"    期望: {e['expected']!r}")
        print(f"    实际: {e['actual']!r}")

sys.exit(0 if FAIL == 0 else 1)
