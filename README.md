# itntext

[![PyPI](https://img.shields.io/pypi/v/itntext)](https://pypi.org/project/itntext/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

`itntext` 是一个 wetext 风格的多语言文本规范化库，支持文本规范化（TN）和逆文本规范化（ITN）。项目内置多语言 grammar、TSV 资源、FST 编译脚本和基于 `kaldifst` 的运行时，既可以直接加载预编译 FST 使用，也可以在本地修改规则后重新编译。

```python
from itntext import Normalizer

normalizer = Normalizer(lang="zh", operator="itn")
print(normalizer.normalize("上午十点三十分"))
# 上午 10:30
```

## 特性

- wetext 风格 API：`Normalizer(lang="zh", operator="itn").normalize(text)`。
- 多语言覆盖：ITN 支持 12 种语言，TN 支持 5 种语言。
- 自主编译 FST：修改 `itntext/grammars` 后运行 `scripts/build_fsts.py` 生成新的 `.fst`。
- 规则层优化：中文数字、日期、时间、金额、单位、电话等核心场景在 grammar/TSV/FST 层处理。
- 服务端友好：支持全局 FST 缓存、`preload()` 预加载和 `normalize_list()` 批量处理。
- 可复现实验：内置与 wetext 的对比脚本、全场景测试报告和 CSV 明细。

## 支持语言

| 模式 | 支持语言 |
|---|---|
| ITN | `de`, `en`, `es`, `fr`, `id`, `ja`, `ko`, `pt`, `ru`, `tl`, `vi`, `zh` |
| TN | `de`, `en`, `es`, `ru`, `zh` |

`auto` 目前按 wetext 风格路由到 `zh`。

## 安装

从 PyPI 安装：

```bash
pip install itntext
```

从 GitHub 安装：

```bash
pip install git+https://github.com/alanpaine/itntext.git
```

从本地源码安装：

```bash
pip install -e .
```

从本地 wheel 安装：

```bash
pip install dist/itntext-0.1.6-py3-none-any.whl
```

安装包中的 wheel 会包含预编译 FST。普通用户安装后可以直接运行，不需要安装 `pynini`，只有修改 grammar 并重新编译 FST 时才需要额外安装：

```bash
pip install "pynini>=2.1.5"
```

运行测试和对比脚本：

```bash
pip install -e ".[test]"
```

## 快速使用

### 中文 TN

```python
from itntext import Normalizer

tn = Normalizer(lang="zh", operator="tn")

print(tn.normalize("123"))
# 一百二十三

print(tn.normalize("2026年6月12日"))
# 二零二六年六月十二日

print(tn.normalize("13800000000"))
# 幺三八零零零零零零零零
```

### 中文 ITN

```python
from itntext import Normalizer

itn = Normalizer(lang="zh", operator="itn")

print(itn.normalize("五月二十三号"))
# 5月23号

print(itn.normalize("上午十点三十分"))
# 上午 10:30

print(itn.normalize("十二元五角三分"))
# ¥12.53

print(itn.normalize("十二公斤"))
# 12kg
```

### 英文与多语言

```python
from itntext import Normalizer

print(Normalizer(lang="en", operator="tn").normalize("$12.50"))
# twelve dollars fifty cents

print(Normalizer(lang="ja", operator="itn").normalize("百二十三"))
# 123

print(Normalizer(lang="ru", operator="tn").normalize("123"))
# сто двадцать три
```

## 服务端用法

服务中不要每句话都创建新的 `Normalizer`。复用同一个实例可以避免重复加载 FST。

```python
from itntext import Normalizer, preload

preload(["zh", "en"], operators=["tn", "itn"])

normalizer = Normalizer(lang="zh", operator="itn")
results = normalizer.normalize_list([
    "五月二十三号",
    "上午十点三十分",
    "十二元五角",
])
```

## CLI

```bash
itntext --lang zh --operator tn "今天是2026年6月12日"
itntext --lang zh --operator itn "十二元五角三分"
itntext --lang en --operator itn "twelve dollars fifty cents"
```

## 编译 FST

源码包和 wheel 已包含预编译 FST。只有修改 `itntext/grammars` 下的 grammar 或 TSV 后，才需要重新编译。

```bash
python scripts/build_fsts.py --operator all --language all --overwrite
python scripts/build_fsts.py --operator tn --language zh --overwrite
python scripts/build_fsts.py --operator itn --language zh --overwrite
```

FST 输出目录：

```text
itntext/fst/itn/<lang>/<lang>_itn_tagger.fst
itntext/fst/itn/<lang>/<lang>_itn_verbalizer.fst
itntext/fst/tn/<lang>/<lang>_tn_tagger.fst
itntext/fst/tn/<lang>/<lang>_tn_verbalizer.fst
```

更完整的编译说明见 [`docs/BUILDING_FSTS.md`](docs/BUILDING_FSTS.md)。

## 测试与对比

```bash
python -m pytest tests -q
python scripts/full_scenario_compare.py
python scripts/compare_wetext.py
python scripts/comprehensive_compare.py
```

正式文档只有三个，位于 `docs/`：

- [`docs/USAGE.md`](docs/USAGE.md)
- [`docs/BUILDING_FSTS.md`](docs/BUILDING_FSTS.md)
- [`docs/DEVELOPMENT.md`](docs/DEVELOPMENT.md)

测试、对比和验收报告放在 `reports/`：

- [`reports/FULL_SCENARIO_COMPARE.md`](reports/FULL_SCENARIO_COMPARE.md)
- [`reports/FULL_SCENARIO_COMPARE.csv`](reports/FULL_SCENARIO_COMPARE.csv)
- [`reports/FULL_SCENARIO_PERFORMANCE.csv`](reports/FULL_SCENARIO_PERFORMANCE.csv)
- [`reports/COMPREHENSIVE_COMPARE.md`](reports/COMPREHENSIVE_COMPARE.md)
- [`reports/COMPREHENSIVE_COMPARE.csv`](reports/COMPREHENSIVE_COMPARE.csv)
- [`reports/WETEXT_COMPARE.md`](reports/WETEXT_COMPARE.md)
- [`reports/DELIVERY_VALIDATION.md`](reports/DELIVERY_VALIDATION.md)

## 项目结构

```text
itntext/
  normalizer.py
  fst_processor.py
  fst/
  grammars/
scripts/
tests/
docs/
reports/
```

## 规则开发原则

项目不在 `Normalizer.normalize()` 里用 `if/replace/regex` 修补结果。新增语言行为时，应修改 `itntext/grammars` 下的 grammar 或 TSV，再重新编译 FST。这样可以保持运行时简单、结果可复现，也更接近 wetext 的编译式使用方式。
