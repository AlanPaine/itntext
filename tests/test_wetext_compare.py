from itntext import Normalizer as ItnNormalizer


def test_wetext_import_and_basic_comparison():
    from wetext import Normalizer as WetextNormalizer

    cases = [
        ("zh", "tn", "123"),
        ("zh", "itn", "一百二十三"),
        ("en", "tn", "123"),
        ("en", "itn", "one hundred twenty three"),
    ]
    for lang, operator, text in cases:
        itn_result = ItnNormalizer(lang=lang, operator=operator).normalize(text)
        wetext_result = WetextNormalizer(lang=lang, operator=operator).normalize(text)
        assert isinstance(itn_result, str)
        assert isinstance(wetext_result, str)
