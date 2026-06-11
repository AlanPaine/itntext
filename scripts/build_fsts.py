#!/usr/bin/env python3
"""
itntext FST 编译脚本

编译中文 ITN 和 TN 的 FST 文件，生成 .fst 缓存。

用法:
    python scripts/build_fsts.py
    python scripts/build_fsts.py --overwrite  # 强制重新编译
"""

import argparse
import os
import sys

# 将项目根目录加入路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def build_itn(overwrite=False):
    """编译中文 ITN FST"""
    print("=" * 60)
    print("编译中文 ITN (Inverse Text Normalization)")
    print("=" * 60)
    from itntext.itn.chinese.inverse_normalizer import InverseNormalizer
    InverseNormalizer(overwrite_cache=overwrite)
    print("ITN FST 编译完成\n")


def build_tn(overwrite=False):
    """编译中文 TN FST"""
    print("=" * 60)
    print("编译中文 TN (Text Normalization)")
    print("=" * 60)
    from itntext.tn.chinese.normalizer import Normalizer
    Normalizer(overwrite_cache=overwrite)
    print("TN FST 编译完成\n")


def main():
    parser = argparse.ArgumentParser(description="编译 itntext FST 文件")
    parser.add_argument("--overwrite", action="store_true", help="强制重新编译，覆盖已有 FST")
    parser.add_argument("--itn-only", action="store_true", help="只编译 ITN")
    parser.add_argument("--tn-only", action="store_true", help="只编译 TN")
    args = parser.parse_args()

    if args.itn_only:
        build_itn(args.overwrite)
    elif args.tn_only:
        build_tn(args.overwrite)
    else:
        build_itn(args.overwrite)
        build_tn(args.overwrite)

    print("=" * 60)
    print("所有 FST 编译完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()
