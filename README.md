# itntext

[![PyPI](https://img.shields.io/pypi/v/itntext)](https://pypi.org/project/itntext/)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-Apache%202.0-green.svg)](LICENSE)

**itntext** 是一个改进版的文本规范化（TN）与逆文本规范化（ITN）库，API 完全兼容 [`wetext`](https://github.com/pengzhendong/wetext)，可零成本切换。

在 wetext 的基础上，itntext 修复了大量中文场景下的已知问题，包括日期格式、时间格式、单位转换、金额表达等，**准确率达到 94.4%**（wetext 为 47.2%），会议转录场景准确率达到 **100%**。

## Features

- Text Normalization (TN) for Chinese
- Inverse Text Normalization (ITN) for Chinese
- 日期后缀保留（号/日）
- 时间格式修复（上午 10:30 / 下午 14:00）
- 分数保护（3/4 不误转为 3月4日）
- 身高转换（1.75m）
- 大数字金额修复（1234567元）
- 股票代码不拆分（600519）
- 单位保留中文（公斤/公里/毫升）
- Traditional to Simplified Chinese conversion
- Full-width to Half-width character conversion
- Interjection removal
- Punctuation removal
- Out-of-vocabulary (OOV) word tagging
- Erhua removal (for Chinese)
- 0-to-9 conversion (for Chinese ITN)

## Installation

```bash
pip install itntext
```

### 依赖

- Python >= 3.8
- kaldifst >= 1.0

### 从源码安装

```bash
git clone https://github.com/alanpaine/itntext.git
cd itntext
pip install -e .
```

### 编译 FST（可选）

itntext 已内置预编译的 FST 文件，安装即可使用。如需自定义规则并重新编译：

```bash
# 安装开发依赖（包含 pynini，用于编译 FST）
pip install -e ".[dev]"

# 编译 FST
python scripts/build_fsts.py
```

## Usage

### Python API

#### Text Normalization (TN)

```python
from itntext import Normalizer

# Chinese TN with erhua removal
normalizer = Normalizer(lang="zh", operator="tn", remove_erhua=True)
result = normalizer.normalize("你好 WeTextProcessing 1.0，全新版本儿，简直666")
print(result)
# => 你好 WeTextProcessing 一点零，全新版本，简直六六六
```

#### Inverse Text Normalization (ITN)

```python
from itntext import Normalizer

# Chinese ITN
normalizer = Normalizer(lang="zh", operator="itn", enable_0_to_9=False)
result = normalizer.normalize("五月二十三号")
print(result)
# => 5月23号

result = normalizer.normalize("上午十点三十分")
print(result)
# => 上午 10:30

result = normalizer.normalize("身高一米七五")
print(result)
# => 身高是1.75m

result = normalizer.normalize("一百二十三万四千五百六十七元")
print(result)
# => 1234567元
```

### Command Line Interface

```bash
# Basic usage
itntext "你好 WeTextProcessing 1.0，全新版本儿，简直666"

# With options
itntext --lang zh --operator tn --remove-erhua "你好 WeTextProcessing 1.0，全新版本儿，简直666"

# Convert traditional to simplified Chinese
itntext --traditional-to-simple "你好，這是測試。"

# Remove punctuations
itntext --remove-puncts "你好，這是測試。"

# ITN mode
itntext --lang zh --operator itn "五月二十三号"
```

## API Reference

### Normalizer Class

```python
Normalizer(
    lang: Literal["auto", "en", "zh", "ja"] = "auto",
    operator: Literal["tn", "itn"] = "tn",
    traditional_to_simple: bool = False,
    full_to_half: bool = False,
    remove_interjections: bool = False,
    remove_puncts: bool = False,
    tag_oov: bool = False,
    enable_0_to_9: bool = False,
    remove_erhua: bool = False,
)
```

#### Parameters

- `lang`: The language of the text. Can be "auto", "en", "zh" or "ja". Default is "auto".
- `operator`: The operator to use. Can be "tn" (text normalization) or "itn" (inverse text normalization). Default is "tn".
- `traditional_to_simple`: Whether to convert traditional Chinese to simplified Chinese. Default is False.
- `full_to_half`: Whether to convert full-width characters to half-width characters. Default is False.
- `remove_interjections`: Whether to remove interjections. Default is False.
- `remove_puncts`: Whether to remove punctuation. Default is False.
- `tag_oov`: Whether to tag out-of-vocabulary words. Default is False.
- `enable_0_to_9`: Whether to enable 0-to-9 conversion for ITN. Default is False.
- `remove_erhua`: Whether to remove erhua for TN. Default is False.

#### Methods

- `normalize(text: str, **kwargs) -> str`: Normalize the text.

## CLI Options

- `--lang, -l`: Set the language. Choices are "auto", "en", "zh", "ja". Default is "auto".
- `--operator, -o`: Set the operator. Choices are "tn", "itn". Default is "tn".
- `--traditional-to-simple`: Convert traditional Chinese to simplified Chinese.
- `--full-to-half`: Convert full-width characters to half-width characters.
- `--remove-interjections`: Remove interjections.
- `--remove-puncts`: Remove punctuation.
- `--tag-oov`: Tag out-of-vocabulary words.
- `--enable-0-to-9`: Enable 0-to-9 conversion.
- `--remove-erhua`: Remove erhua.

## 与 wetext 对比

| 输入 | wetext | **itntext** |
|------|--------|-------------|
| 五月二十三**号** | 05/23 | **5月23号** |
| 四月二十三**日** | 04/23 | **4月23日** |
| 四分之三 | 3/4 | **3/4** |
| 上午十点三十分 | 10:30a.m. | **上午 10:30** |
| 下午两点 | 下午两点 | **下午 14:00** |
| 身高一米七五 | 身高1m七五 | **身高是1.75m** |
| 一两个 | 一2个 | **1～2个** |
| 一百二十三万四千五百六十七元 | ¥123万4567 | **1234567元** |
| 六零零五百一十九 | 600 519 | **600519** |
| 上午九点到十一点半 | 上午九点到11:30 | **上午 09:00～11:30** |

完整对比报告见 [docs/BENCHMARK.md](docs/BENCHMARK.md)。

## 架构

```
输入文本
   │
   ▼
┌─────────────────┐
│  kaldifst FST    │  ← 预编译的 FST 文件（.fst）
│  tagger          │     运行时加载，无需 pynini
│  verbalizer      │
└─────────────────┘
   │
   ▼
┌─────────────────┐
│  itntext 后处理层 │  ← 修复 WeText 已知问题
│  - 日期格式修正   │     规则从 TSV 数据文件加载
│  - 时间格式修正   │
│  - 单位中文保留   │
│  - 股票代码合并   │
│  - 金额格式修正   │
│  - 分数保护      │
│  - 身高转换      │
└─────────────────┘
   │
   ▼
输出文本
```

## 项目结构

```
itntext/
├── itntext/
│   ├── __init__.py              # 包入口
│   ├── normalizer.py            # 核心 Normalizer 类
│   ├── postprocess_fixes.py     # 后处理修正层（规则从 TSV 加载）
│   ├── processor.py             # kaldifst FST 运行时
│   ├── token_parser.py          # Token 解析与重排序
│   ├── config.py                # 配置类
│   ├── utils.py                 # 工具函数
│   ├── data/postprocess/        # TSV 规则数据文件
│   ├── itn/chinese/             # ITN 中文规则 + 预编译 FST
│   │   ├── rules/               # Python 规则类（pynini 编译用）
│   │   ├── data/                # TSV 数据文件
│   │   ├── zh_itn_tagger.fst    # 预编译 FST
│   │   └── zh_itn_verbalizer.fst
│   └── tn/chinese/              # TN 中文规则 + 预编译 FST
│       ├── rules/               # Python 规则类（pynini 编译用）
│       ├── data/                # TSV 数据文件
│       ├── zh_tn_tagger.fst     # 预编译 FST
│       └── zh_tn_verbalizer.fst
├── tests/                       # 测试用例
├── scripts/
│   └── build_fsts.py            # FST 编译脚本（需要 pynini）
├── docs/
│   └── BENCHMARK.md             # 完整对比测试报告
├── README.md                    # 本文档
├── LICENSE                      # Apache 2.0
└── pyproject.toml               # PyPI 打包配置
```

## 性能

| 指标 | wetext | itntext | 差异 |
|------|--------|---------|------|
| 单句平均延迟 | 0.813 ms | 0.932 ms | +15% |
| 批量 TPS (短文本) | 1225 | 1040 | -15% |
| 批量 TPS (长文本) | 84 | 77 | -8% |
| 峰值内存 | 5.0 KB | 4.2 KB | **-16%** |
| 初始化时间 | 0.012 ms | 0.007 ms | **-41%** |

itntext 与 wetext 使用相同的 kaldifst 运行时引擎，性能差距主要来自后处理修正层（约 15% 延迟开销）。

## 已知限制

以下场景与 wetext 表现一致，均为底层 WeTextProcessing 的已知限制：

- 英文数字转换（如 `one hundred` → `123`）
- 邮箱格式还原（如 `test at example dot com` → `test@example.com`）
- 单字数字（如 `零` → `0`）

## 开源协议

Apache License 2.0，详见 [LICENSE](LICENSE)。

## 致谢

本项目基于以下优秀开源项目构建，在此深表感谢：

- **[WeTextProcessing](https://github.com/wenet-e2e/WeTextProcessing)** - 由 WeNet 社区维护的文本规范化与逆文本规范化工具库。itntext 内嵌了 WeTextProcessing 的核心 runtime（processor.py、token_parser.py、utils.py）以及完整的中文 ITN/TN 规则体系（FST 规则类、TSV 数据文件），并在此基础上进行了改进和扩展。
- **[wetext](https://pypi.org/project/wetext/)** - WeTextProcessing 的 PyPI 封装，使用 kaldifst 作为运行时引擎。itntext 在 API 设计上完全兼容 wetext，运行时同样使用 kaldifst 加载预编译 FST。
- **[OpenFST](https://www.openfst.org/)** - 底层有限状态转换器引擎，为文本规则编译和运行提供核心能力。

特别感谢 WeNet 社区和 WeTextProcessing 项目的所有贡献者，他们的工作为中文语音处理领域奠定了坚实的基础。
