from itntext import Normalizer, preload
from itntext.fst_processor import ITN_LANGUAGES, TN_LANGUAGES


def test_all_compiled_itn_languages_load():
    for lang in ITN_LANGUAGES:
        normalizer = Normalizer(lang=lang, operator="itn")
        assert isinstance(normalizer.normalize("one two three"), str)


def test_all_compiled_tn_languages_load():
    for lang in TN_LANGUAGES:
        normalizer = Normalizer(lang=lang, operator="tn")
        assert isinstance(normalizer.normalize("123"), str)


def test_wetext_style_api_examples():
    assert Normalizer(lang="en", operator="itn").normalize("one hundred twenty three") == "123"
    assert Normalizer(lang="en", operator="tn").normalize("123") == "one hundred and twenty three"
    assert Normalizer(lang="ja", operator="itn").normalize("百二十三") == "123"


def test_zh_grammar_fixes():
    assert Normalizer(lang="zh", operator="tn").normalize("123") == "一百二十三"
    assert Normalizer(lang="zh", operator="tn").normalize("2026年6月12日") == "二零二六年六月十二日"
    assert Normalizer(lang="zh", operator="tn").normalize("13800000000") == "幺三八零零零零零零零零"
    assert Normalizer(lang="zh", operator="itn").normalize("五月二十三号") == "5月23号"
    assert Normalizer(lang="zh", operator="itn").normalize("四月二十三日") == "4月23日"
    assert Normalizer(lang="zh", operator="itn").normalize("上午十点三十分") == "上午 10:30"
    assert Normalizer(lang="zh", operator="itn").normalize("百分之二十五") == "25%"
    assert Normalizer(lang="zh", operator="itn").normalize("十二公斤") == "12kg"
    assert Normalizer(lang="zh", operator="itn").normalize("十二元五角") == "¥12.5"
    assert Normalizer(lang="zh", operator="itn").normalize("十二元五角三分") == "¥12.53"
    assert Normalizer(lang="zh", operator="itn").normalize("十二元五分") == "¥12.05"


def test_batch_and_preload_api():
    preload(["zh"], operators=["tn", "itn"])
    normalizer = Normalizer(lang="zh", operator="itn")
    assert normalizer.normalize_list(["五月二十三号", "十二公斤"]) == ["5月23号", "12kg"]
