# 使用指南

`itntext` 的核心入口是 `Normalizer`。TN 用于把书面文本转成适合朗读的形式，ITN 用于把 ASR 识别出的口语文本转成规范写法。

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

wheel 已包含预编译 FST，普通使用不需要安装 `pynini`。只有修改 grammar 或 TSV 并重新编译 FST 时，才需要额外安装 `pynini`。

## Python API

```python
from itntext import Normalizer

normalizer = Normalizer(lang="zh", operator="itn")
print(normalizer.normalize("上午十点三十分"))
# 上午 10:30
```

| 参数 | 类型 | 默认值 | 说明 |
|---|---|---|---|
| `lang` | `str` | `auto` | 语言代码，`auto` 当前路由到 `zh` |
| `operator` | `str` | `tn` | `tn` 或 `itn` |
| `traditional_to_simple` | `bool` | `False` | 兼容 wetext 参数 |
| `full_to_half` | `bool` | `False` | 兼容 wetext 参数 |
| `remove_interjections` | `bool` | `False` | 兼容 wetext 参数 |
| `remove_puncts` | `bool` | `False` | 兼容 wetext 参数 |
| `tag_oov` | `bool` | `False` | 兼容 wetext 参数 |
| `enable_0_to_9` | `bool` | `False` | 兼容 wetext 参数 |
| `remove_erhua` | `bool` | `False` | 兼容 wetext 参数 |

## 中文示例

```python
from itntext import Normalizer

tn = Normalizer(lang="zh", operator="tn")
assert tn.normalize("123") == "一百二十三"
assert tn.normalize("2026年6月12日") == "二零二六年六月十二日"
assert tn.normalize("13800000000") == "幺三八零零零零零零零零"

itn = Normalizer(lang="zh", operator="itn")
assert itn.normalize("五月二十三号") == "5月23号"
assert itn.normalize("上午十点三十分") == "上午 10:30"
assert itn.normalize("十二公斤") == "12kg"
assert itn.normalize("十二元五角三分") == "¥12.53"
```

## 批量处理

```python
from itntext import Normalizer

normalizer = Normalizer(lang="zh", operator="itn")
results = normalizer.normalize_list(["五月二十三号", "十二公斤"])
```

## 预加载

```python
from itntext import preload

preload(["zh", "en"], operators=["tn", "itn"])
```

## CLI

```bash
itntext --lang zh --operator tn "今天是2026年6月12日"
itntext --lang zh --operator itn "十二元五角三分"
itntext --lang zh --operator itn --file input.txt
```
