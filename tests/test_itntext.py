#!/usr/bin/env python3
"""
itntext 单元测试
"""

import pytest
from itntext import Normalizer


itn = Normalizer(lang="zh", operator="itn")


class TestDate:
    def test_date_ri(self):
        assert itn.normalize("四月二十三日") == "4月23日"

    def test_date_hao(self):
        assert itn.normalize("五月二十三号") == "5月23号"

    def test_date_year(self):
        assert itn.normalize("二零二四年四月二十三日") == "2024年4月23日"

    def test_date_march_hao(self):
        assert itn.normalize("三月十五号") == "3月15号"

    def test_date_oct_hao(self):
        assert itn.normalize("十月一号") == "10月1号"


class TestTime:
    def test_time_am(self):
        assert itn.normalize("上午十点三十分") == "上午 10:30"

    def test_time_pm(self):
        assert itn.normalize("下午两点") == "下午 14:00"

    def test_time_24h(self):
        assert itn.normalize("二十三时五十九分") == "23:59"

    def test_time_range(self):
        assert itn.normalize("上午九点到十一点半") == "上午 09:00～11:30"


class TestNumber:
    def test_fraction(self):
        assert itn.normalize("四分之三") == "3/4"

    def test_height(self):
        assert itn.normalize("身高一米七五") == "身高是1.75m"

    def test_range(self):
        assert itn.normalize("一两个") == "1～2个"

    def test_big_money(self):
        assert itn.normalize("一百二十三万四千五百六十七元") == "1234567元"

    def test_wan(self):
        assert itn.normalize("五百万") == "5000000"


class TestStock:
    def test_stock_code(self):
        assert itn.normalize("六零零五百一十九") == "600519"


class TestUnit:
    def test_kg(self):
        assert itn.normalize("体重六十公斤") == "体重60公斤"

    def test_km(self):
        assert itn.normalize("一百公里") == "100公里"

    def test_ml(self):
        assert itn.normalize("五百毫升") == "500毫升"


class TestPhone:
    def test_phone(self):
        assert itn.normalize("幺三八零零零零零零零零") == "13800000000"

    def test_12306(self):
        assert itn.normalize("幺二二三零六") == "12306"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
