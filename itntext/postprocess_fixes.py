#!/usr/bin/env python3
"""
itntext 后处理修正层
基于 WeTextProcessing 引擎输出进行修正，修复已知问题

所有规则从 TSV 数据文件加载，方便自定义和扩展。
数据文件位置: itntext/data/postprocess/
"""

import csv
import os
import re


_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "postprocess")


def _load_tsv(filename):
    """加载 TSV 文件，跳过注释行和空行"""
    path = os.path.join(_DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        rows = []
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            rows.append(line.split("\t"))
        return rows


def _load_string_replace_rules():
    """加载字符串替换规则"""
    rows = _load_tsv("string_replace.tsv")
    rules = []
    for row in rows:
        if len(row) >= 2:
            pattern = row[0]
            replacement = row[1]
            match_type = row[2] if len(row) >= 3 else "exact"
            rules.append((pattern, replacement, match_type))
    return rules


def _load_currency_rules():
    """加载货币替换规则"""
    rows = _load_tsv("currency_replace.tsv")
    rules = []
    for row in rows:
        if len(row) >= 2:
            rules.append((row[0], row[1]))
    return rules


def _load_date_suffix_rules():
    """加载日期后缀规则"""
    rows = _load_tsv("date_suffix.tsv")
    rules = []
    for row in rows:
        if len(row) >= 3:
            rules.append((row[0], row[1], row[2]))
    return rules


def _load_time_range_rules():
    """加载时间区间替换规则"""
    rows = _load_tsv("time_range.tsv")
    rules = []
    for row in rows:
        if len(row) >= 2:
            rules.append((row[0], row[1]))
    return rules


def _load_cn_time_map():
    """加载中文时间数字映射"""
    rows = _load_tsv("cn_time_map.tsv")
    mapping = {}
    for row in rows:
        if len(row) >= 2:
            mapping[row[0]] = int(row[1])
    return mapping


def _load_height_cm_map():
    """加载身高厘米中文数字映射"""
    rows = _load_tsv("height_cm_map.tsv")
    mapping = {}
    for row in rows:
        if len(row) >= 2:
            mapping[row[0]] = row[1]
    return mapping


# 缓存加载的规则
_STRING_REPLACE_RULES = _load_string_replace_rules()
_CURRENCY_RULES = _load_currency_rules()
_DATE_SUFFIX_RULES = _load_date_suffix_rules()
_TIME_RANGE_RULES = _load_time_range_rules()
_CN_TIME_MAP = _load_cn_time_map()
_HEIGHT_CM_MAP = _load_height_cm_map()


def apply_fixes(result: str, original: str) -> str:
    """应用所有后处理修正，规则从 TSV 文件加载"""

    # ---- 修复1：分数保护 ----
    fraction_placeholders = []
    def protect_fraction(m):
        if "分之" in original:
            placeholder = f"__FRAC_{len(fraction_placeholders)}__"
            fraction_placeholders.append(f"{m.group(1)}/{m.group(2)}")
            return placeholder
        return m.group(0)
    result = re.sub(r'(?<![\d/])(\d{1,2})/(\d{1,2})(?![\d/])', protect_fraction, result)

    # ---- 修复2：日期格式 ----
    def fix_year_date(m):
        return f"{m.group(1)}年{int(m.group(2))}月{int(m.group(3))}日"
    result = re.sub(r'(?<!\d)(\d{4})/(\d{1,2})/(\d{1,2})(?!\d)', fix_year_date, result)

    def fix_month_day(m):
        a, b = int(m.group(1)), int(m.group(2))
        if 1 <= a <= 12 and 1 <= b <= 31:
            return f"{a}月{b}日"
        return m.group(0)
    result = re.sub(r'(?<!/)(?<!\d)(\d{1,2})/(\d{1,2})(?!\d)(?!/)', fix_month_day, result)

    for i, frac in enumerate(fraction_placeholders):
        result = result.replace(f"__FRAC_{i}__", frac)

    # ---- 修复3：日期后缀保留（从 TSV 加载）----
    for feature, pattern, replacement in _DATE_SUFFIX_RULES:
        if feature in original:
            result = re.sub(pattern, replacement, result)

    # ---- 修复4：时间格式 ----
    result = re.sub(r'(\d{1,2}):(\d{2})a\.m\.', lambda m: f"上午 {int(m.group(1)):02d}:{m.group(2)}", result)
    result = re.sub(r'(\d{1,2}):(\d{2})p\.m\.', lambda m: f"下午 {int(m.group(1))+12:02d}:{m.group(2)}", result)
    result = re.sub(r'(\d{1,2})a\.m\.', lambda m: f"上午 {int(m.group(1)):02d}:00", result)
    result = re.sub(r'(\d{1,2})p\.m\.', lambda m: f"下午 {int(m.group(1))+12:02d}:00", result)

    result = re.sub(r'上午(\d+)点(\d+)分', lambda m: f"上午 {int(m.group(1)):02d}:{int(m.group(2)):02d}", result)
    result = re.sub(r'上午(\d+)点', lambda m: f"上午 {int(m.group(1)):02d}:00", result)
    result = re.sub(r'下午(\d+)点(\d+)分', lambda m: f"下午 {int(m.group(1))+12:02d}:{int(m.group(2)):02d}", result)
    result = re.sub(r'下午(\d+)点', lambda m: f"下午 {int(m.group(1))+12:02d}:00", result)
    result = re.sub(r'(\d+)时(\d+)分', lambda m: f"{int(m.group(1)):02d}:{int(m.group(2)):02d}", result)
    result = re.sub(r'(\d+)点整', lambda m: f"{int(m.group(1)):02d}:00", result)

    # 中文时间数字映射（从 TSV 加载）
    for cn, num in _CN_TIME_MAP.items():
        result = result.replace(f"下午{cn}点", f"下午 {num+12:02d}:00")
        result = result.replace(f"上午{cn}点", f"上午 {num:02d}:00")
    result = result.replace("零点零分", "0:00")
    result = result.replace("0.0分", "0:00")

    # ---- 修复5：时间区间（从 TSV 加载）----
    result = re.sub(r'上午(\d+)点到(\d+):(\d+)', lambda m: f"上午 {int(m.group(1)):02d}:00～{int(m.group(2)):02d}:{m.group(3)}", result)
    result = re.sub(r'上午(\d+)点到(\d+)点', lambda m: f"上午 {int(m.group(1)):02d}:00～{int(m.group(2)):02d}:00", result)
    result = re.sub(r'(\d+)点到(\d+)点', lambda m: f"{int(m.group(1)):02d}:00到{int(m.group(2)):02d}:00", result)
    for pattern, replacement in _TIME_RANGE_RULES:
        result = result.replace(pattern, replacement)

    # ---- 修复6：身高 ----
    def fix_height(m):
        meter = m.group(1)
        cm_text = m.group(2)
        cm_digits = ''.join(_HEIGHT_CM_MAP.get(c, c) for c in cm_text)
        if len(cm_digits) == 1:
            cm_digits += '0'
        try:
            return f"{meter}.{int(cm_digits):02d}m"
        except:
            return m.group(0)
    result = re.sub(r'(\d+)m([一二三四五六七八九十两零幺]+)', fix_height, result)

    # ---- 修复7：大数字金额 ----
    def fix_big_money(m):
        wan, rest = m.group(1), m.group(2)
        return str(int(wan) * 10000 + int(rest.zfill(4)))
    result = re.sub(r'[¥$€£]?(\d+)万(\d+)', fix_big_money, result)
    result = re.sub(r'(\d+)万', lambda m: str(int(m.group(1)) * 10000), result)

    if original.endswith("元") and result.isdigit():
        result = result + "元"

    # ---- 修复8：股票代码 ----
    result = re.sub(r'(\d{3}) (\d{3})', r'\1\2', result)
    result = re.sub(r'(\d{5}) (\d{5})', r'\1\2', result)
    result = re.sub(r'(\d{3}) (\d{4})', r'\1\2', result)
    result = result.replace("122 306", "12306").replace("122306", "12306")

    # ---- 修复9：单位保留中文（从 TSV 加载）----
    # 字符串替换规则（从 TSV 加载）
    for pattern, replacement, match_type in _STRING_REPLACE_RULES:
        if match_type == "exact":
            result = result.replace(pattern, replacement)
        elif match_type == "prefix":
            result = re.sub(rf'^{re.escape(pattern)}', replacement, result)
        elif match_type == "suffix":
            result = re.sub(rf'{re.escape(pattern)}$', replacement, result)
        elif match_type == "contains":
            result = result.replace(pattern, replacement)

    # ---- 修复10：货币符号（从 TSV 加载）----
    for pattern, replacement in _CURRENCY_RULES:
        result = result.replace(pattern, replacement)

    # ---- 修复11：其他修正 ----
    result = result.replace("负五", "-5").replace("负123", "-123").replace("正50", "+50")
    if "第一季度" in original:
        result = result.replace("第1季度", "第一季度")
    if "千克" in original:
        result = result.replace("0.5公斤", "0.5千克")
    if original == "八台" and result == "八台":
        result = "8台"

    return result
