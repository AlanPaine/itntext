# FST 编译说明

`itntext` 的运行时只加载预编译 `.fst` 文件。修改 grammar 或 TSV 后，需要重新编译对应语言和模式的 tagger/verbalizer FST。

## 安装包中的 FST

wheel 和源码包会携带已编译 FST。用户执行：

```bash
pip install itntext
```

即可直接调用 `Normalizer`，不需要安装 `pynini`，也不需要本地编译 FST。

FST 通过 `pyproject.toml` 中的 package data 配置打包：

```toml
[tool.setuptools.package-data]
"itntext" = ["fst/**/*.fst"]
"itntext.grammars" = ["**/*.tsv", "**/*.far", "**/*.fst", "**/*.txt", "**/*.md"]
```

构建后可以检查 wheel 是否包含 FST：

```bash
python - <<'PY'
import zipfile
from pathlib import Path

wheel = next(Path("dist").glob("*.whl"))
with zipfile.ZipFile(wheel) as zf:
    print("fst count:", sum(1 for name in zf.namelist() if name.endswith(".fst")))
PY
```

## 编译依赖

只有需要重新编译 FST 时才安装：

```bash
pip install "pynini>=2.1.5"
```

## 编译命令

```bash
python scripts/build_fsts.py --operator all --language all --overwrite
python scripts/build_fsts.py --operator tn --language zh --overwrite
python scripts/build_fsts.py --operator itn --language zh --overwrite
```

## 参数

| 参数 | 可选值 | 默认值 | 说明 |
|---|---|---|---|
| `--operator` | `all`, `tn`, `itn` | `all` | 编译 TN、ITN 或两者 |
| `--language` | 语言代码或 `all` | `all` | 编译指定语言或全部语言 |
| `--overwrite` | flag | `False` | 覆盖已有 FST |
| `--input-case` | `cased`, `lower_cased` | `cased` | TN 输入大小写模式 |

## 输出目录

```text
itntext/fst/itn/<lang>/<lang>_itn_tagger.fst
itntext/fst/itn/<lang>/<lang>_itn_verbalizer.fst
itntext/fst/tn/<lang>/<lang>_tn_tagger.fst
itntext/fst/tn/<lang>/<lang>_tn_verbalizer.fst
```

## 修改规则后的流程

1. 修改 `itntext/grammars` 下对应语言的 grammar 或 TSV。
2. 重新编译对应语言。
3. 运行目标用例。
4. 运行 `python -m pytest tests -q`。
5. 运行 `python scripts/comprehensive_compare.py` 更新报告。

项目约定不在 `Normalizer.normalize()` 里用运行时补丁修输出，新增行为应写进 grammar 或 TSV，再编译成 FST。
