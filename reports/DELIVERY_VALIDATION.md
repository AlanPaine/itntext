# 交付验收记录

本文记录 `itntext-0.1.6` 完整产物包的交付验收结果。

## 包结构

产物包：

```text
itntext-0.1.6-complete.zip
```

包内包含：

- 完整源码
- 多语言 grammar 和 TSV
- 已编译运行时 FST
- README 和 docs 文档
- 测试代码
- 对比脚本
- wetext 对比报告
- 全场景测试报告
- PyPI 构建产物

## 版本

```text
pyproject.toml version = 0.1.6
itntext.__version__ = 0.1.6
```

## 已编译产物

运行时 FST 数量：

```text
34
```

对应：

- ITN：12 种语言，每种语言包含 tagger/verbalizer 两个 FST
- TN：5 种语言，每种语言包含 tagger/verbalizer 两个 FST

包内全部 `.fst` 数量为 `35`，其中额外 1 个来自 grammar 资源目录。

## 核心识别测试

| 模式 | 输入 | 输出 |
|---|---|---|
| zh TN | `123` | `一百二十三` |
| zh TN | `3.14` | `三点一四` |
| zh TN | `25%` | `百分之二十五` |
| zh TN | `10:30` | `十点三十分` |
| zh TN | `2026年6月12日` | `二零二六年六月十二日` |
| zh TN | `今天是2026年6月12日` | `今天是二零二六年六月十二日` |
| zh TN | `13800000000` | `幺三八零零零零零零零零` |
| zh ITN | `五月二十三号` | `5月23号` |
| zh ITN | `四月二十三日` | `4月23日` |
| zh ITN | `上午十点三十分` | `上午 10:30` |
| zh ITN | `百分之二十五` | `25%` |
| zh ITN | `十二公斤` | `12kg` |
| zh ITN | `十二元五角` | `¥12.5` |
| zh ITN | `十二元五角三分` | `¥12.53` |
| zh ITN | `十二元五分` | `¥12.05` |
| zh ITN | `幺三八零零零零零零零零` | `13800000000` |
| en ITN | `twelve kilograms` | `12 kg` |
| ja ITN | `百二十三` | `123` |
| id ITN | `seratus dua puluh tiga` | `123` |
| ru TN | `123` | `сто двадцать три` |

## 测试命令

```bash
python scripts/full_scenario_compare.py
python scripts/comprehensive_compare.py
python scripts/compare_wetext.py
python -m pytest tests -q
python -m compileall -q itntext scripts tests
```

结果：

```text
6 passed
```

## 全场景测试

新增全量场景报告：

```text
reports/FULL_SCENARIO_COMPARE.md
reports/FULL_SCENARIO_COMPARE.csv
reports/FULL_SCENARIO_PERFORMANCE.csv
```

结果：

```text
总用例：58
itntext 明确期望用例：41/41，通过率 100.0%
wetext 可比明确期望用例：34/38，通过率 89.5%
itntext 失败/异常用例：0
```

覆盖类别包括数字、小数、百分比、分数、时间、日期、金额/货币、单位、长数字/电话、电子类、多语言和热调用性能。

## wheel 安装验证

从完整 zip 解压后，安装包内 wheel：

```bash
pip install dist/itntext-0.1.6-py3-none-any.whl
```

验证结果：

```text
version 0.1.6
runtime_fst 34
zh itn 十二元五角三分 => ¥12.53
zh tn 13800000000 => 幺三八零零零零零零零零
en itn twelve kilograms => 12 kg
ja itn 百二十三 => 123
```

## PyPI 构建检查

```bash
twine check dist/*
```

结果：

```text
itntext-0.1.6-py3-none-any.whl: PASSED
itntext-0.1.6.tar.gz: PASSED
```

## 命名检查

源码、文档和包内路径未发现历史项目命名残留。

## 结论

该产物满足此前确定的交付要求：项目名为 `itntext`，版本号为 `0.1.6`，包含完整源码、文档、测试、对比报告、已编译 FST 和 PyPI 构建产物；中文核心 TN/ITN 场景、英文基础场景和多语言 smoke 场景均已验证。
