# 开发指南

本文面向需要维护 `itntext` grammar、FST 编译流程和测试集的开发者。

## 设计原则

`itntext` 保持 wetext 风格的使用方式，同时把多语言规则收敛到项目自己的 grammar/TSV 体系中。运行时只负责加载 FST 和执行 tagger/verbalizer，不负责修补结果。

规则开发遵循三点：

- 语言行为写在 `itntext/grammars`。
- 修改规则后重新编译 FST。
- 通过测试和对比报告确认输出。

## 运行时链路

```text
Normalizer.normalize(text)
  ↓
FstProcessor.tag(text)
  ↓
tagger.fst 输出 token
  ↓
TokenParser 生成候选 token 顺序
  ↓
FstProcessor.verbalize(token)
  ↓
verbalizer.fst 输出最终文本
```

## 中文已优化场景

| 场景 | 输入 | 输出 |
|---|---|---|
| TN 数字 | `123` | `一百二十三` |
| TN 日期 | `2026年6月12日` | `二零二六年六月十二日` |
| TN 电话 | `13800000000` | `幺三八零零零零零零零零` |
| ITN 日期号 | `五月二十三号` | `5月23号` |
| ITN 日期日 | `四月二十三日` | `4月23日` |
| ITN 时间 | `上午十点三十分` | `上午 10:30` |
| ITN 百分比 | `百分之二十五` | `25%` |
| ITN 单位 | `十二公斤` | `12kg` |
| ITN 金额 | `十二元五角三分` | `¥12.53` |

这些规则都编译进 FST，不是 `normalize()` 里的后处理补丁。

## 测试

```bash
python scripts/full_scenario_compare.py
python scripts/comprehensive_compare.py
python scripts/compare_wetext.py
python -m pytest tests -q
python -m compileall -q itntext scripts tests
```

## GitHub 仓库结构

开源仓库建议保留以下内容：

```text
README.md
pyproject.toml
itntext/
docs/
reports/
scripts/
tests/
dist/
```

`docs/` 只放正式使用文档，`reports/` 放测试报告、wetext 对比和交付验收记录。`dist/` 可以作为构建产物随交付包保留；如果推送到 GitHub，也可以只保留源码，把构建产物放到 Release 页面。

## 性能建议

服务启动时预加载：

```python
from itntext import preload

preload(["zh", "en"], operators=["tn", "itn"])
```

批量文本复用实例：

```python
from itntext import Normalizer

normalizer = Normalizer(lang="zh", operator="itn")
results = normalizer.normalize_list(texts)
```
