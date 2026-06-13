from __future__ import annotations

import itertools
import os
import string
from collections import OrderedDict
from math import factorial
from typing import Dict, Iterable, List, Sequence, Union

from kaldifst import TextNormalizer


PRESERVE_ORDER_KEY = "preserve_order"
EOS = "<EOS>"

ITN_LANGUAGES = ("de", "en", "es", "fr", "id", "ja", "ko", "pt", "ru", "tl", "vi", "zh")
TN_LANGUAGES = ("de", "en", "es", "ru", "zh")
ALL_LANGUAGES = tuple(sorted(set(ITN_LANGUAGES) | set(TN_LANGUAGES) | {"auto"}))


class TokenParser:
    """解析 grammar 输出的 token 字符串并生成候选重排。"""

    def __call__(self, text: str) -> None:
        self.text = text
        self.len_text = len(text)
        self.char = text[0] if text else EOS
        self.index = 0

    def parse(self) -> List[dict]:
        result = []
        while self.parse_ws():
            token = self.parse_token()
            if not token:
                break
            result.append(token)
        return result

    def parse_token(self) -> Dict[str, Union[str, dict, bool]]:
        result = OrderedDict()
        key = self.parse_string_key()
        if key is None:
            return {}
        self.parse_ws()
        if key == PRESERVE_ORDER_KEY:
            self.parse_char(":")
            self.parse_ws()
            self.parse_chars("true")
            value: Union[str, dict, bool] = True
        else:
            value = self.parse_token_value()
        result[key] = value
        return result

    def parse_token_value(self) -> Union[str, dict]:
        if self.char == ":":
            self.parse_char(":")
            self.parse_ws()
            self.parse_char('"')
            value = self.parse_string_value()
            self.parse_char('"')
            return value
        if self.char == "{":
            result = OrderedDict()
            self.parse_char("{")
            for token_dict in self.parse():
                for key, value in token_dict.items():
                    result[key] = value
            self.parse_char("}")
            return result
        raise ValueError(f"Unexpected token parser state at {self.index}: {self.char!r}")

    def parse_char(self, expected: str) -> bool:
        assert self.char == expected
        self.read()
        return True

    def parse_chars(self, expected: str) -> bool:
        matched = False
        for char in expected:
            matched |= self.parse_char(char)
        return matched

    def parse_string_key(self) -> str | None:
        assert self.char not in string.whitespace and self.char != EOS
        chars = []
        while self.char in string.ascii_letters + "_":
            chars.append(self.char)
            if not self.read():
                raise ValueError("Unexpected end of token key")
        return "".join(chars) if chars else None

    def parse_string_value(self) -> str | None:
        assert self.char != EOS
        chars = []
        while self.char != '"' or self.text[self.index + 1] != " ":
            chars.append(self.char)
            if not self.read():
                raise ValueError("Unexpected end of token value")
        return "".join(chars) if chars else None

    def parse_ws(self) -> bool:
        not_eos = self.char != EOS
        while not_eos and self.char == " ":
            not_eos = self.read()
        return not_eos

    def read(self) -> bool:
        if self.index < self.len_text - 1:
            self.index += 1
            self.char = self.text[self.index]
            return True
        self.char = EOS
        return False

    def estimate_permutations(self, token_group: Dict[str, Union[OrderedDict, str, bool]]) -> int:
        count = 1
        for value in token_group.values():
            if isinstance(value, dict):
                count *= self.estimate_permutations(value)
        return count * factorial(len(token_group))

    def split_tokens(self, tokens: Sequence[dict], max_permutations: int = 729) -> List[List[dict]]:
        splits = []
        start = 0
        current_count = 1
        for idx, token_group in enumerate(tokens):
            token_count = self.estimate_permutations(token_group)
            if token_count * current_count > max_permutations:
                splits.append(list(tokens[start:idx]))
                start = idx
                current_count = 1
            if token_count > max_permutations:
                raise ValueError(f"Token group has too many permutations: {token_count}")
            current_count *= token_count
        splits.append(list(tokens[start:]))
        return splits

    def permute(self, parsed: OrderedDict) -> List[str]:
        output = []
        permutations = [parsed.items()] if PRESERVE_ORDER_KEY in parsed else itertools.permutations(parsed.items())
        for permutation in permutations:
            fragments = [""]
            for key, value in permutation:
                if isinstance(value, str) or value is None:
                    fragments = ["".join(x) for x in itertools.product(fragments, [f'{key}: "{value}" '])]
                elif isinstance(value, OrderedDict):
                    nested = self.permute(value)
                    fragments = ["".join(x) for x in itertools.product(fragments, [f" {key} {{ "], nested, [f" }} "])]
                elif isinstance(value, bool):
                    fragments = ["".join(x) for x in itertools.product(fragments, [f"{key}: true "])]
                else:
                    raise ValueError(f"Unsupported token value type: {type(value)!r}")
            output.extend(fragments)
        return output

    def generate_permutations(self, tokens: Sequence[dict]) -> Iterable[str]:
        def helper(prefix: str, idx: int) -> Iterable[str]:
            if idx == len(tokens):
                yield prefix
                return
            for option in self.permute(tokens[idx]):
                yield from helper(prefix + option, idx + 1)

        yield from helper("", 0)


class FstProcessor:
    """加载并运行 itntext tagger/verbalizer FST。"""

    def __init__(self, lang: str, operator: str, fst_root: str | None = None):
        if operator not in {"tn", "itn"}:
            raise ValueError("operator must be 'tn' or 'itn'")
        supported = ITN_LANGUAGES if operator == "itn" else TN_LANGUAGES
        if lang not in supported:
            raise ValueError(f"Unsupported {operator.upper()} language: {lang}. Supported: {', '.join(supported)}")

        base_dir = os.path.dirname(os.path.abspath(__file__))
        fst_root = fst_root or os.path.join(base_dir, "fst")
        fst_dir = os.path.join(fst_root, operator, lang)
        prefix = f"{lang}_{operator}"
        tagger_path = os.path.join(fst_dir, f"{prefix}_tagger.fst")
        verbalizer_path = os.path.join(fst_dir, f"{prefix}_verbalizer.fst")
        missing = [p for p in (tagger_path, verbalizer_path) if not os.path.exists(p)]
        if missing:
            raise FileNotFoundError(
                "缺少预编译 FST: "
                + ", ".join(missing)
                + f"。请运行: python scripts/build_fsts.py --operator {operator} --language {lang}"
            )

        self.lang = lang
        self.operator = operator
        self.tagger = TextNormalizer(tagger_path)
        self.verbalizer = TextNormalizer(verbalizer_path)
        self.parser = TokenParser()

    def tag(self, text: str) -> str:
        return self.tagger(text).strip()

    def verbalize(self, tagged_text: str) -> str:
        return self.verbalizer(tagged_text).strip()

    def normalize(self, text: str) -> str:
        tagged = self.tag(text)
        if not tagged:
            return text
        self.parser(tagged)
        tokens = self.parser.parse()
        parts = []
        for token_group in self.parser.split_tokens(tokens):
            for candidate in self.parser.generate_permutations(token_group):
                output = self.verbalize(candidate)
                if output:
                    parts.append(output)
                    break
            else:
                return text
        return " ".join(part for part in parts if part).strip() or text
