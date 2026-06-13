# itntext 全场景对比测试报告

## 总结

- 有明确期望值的用例：32 个，itntext 通过 32 个，通过率 100.0%。
- itntext ITN 覆盖语言：de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh。
- itntext TN 覆盖语言：de, en, es, ru, zh。
- wetext 仅在 `zh/en` 范围内参与对比，其他语言标记为 unsupported。

## 准确率与输出

| 类别 | 语言 | 模式 | 输入 | 期望 | itntext | itntext状态 | wetext | wetext状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 数字 | zh | tn | 123 | 一百二十三 | 一百二十三 | pass | 一百二十三 | pass |  |
| 小数 | zh | tn | 3.14 | 三点一四 | 三点一四 | pass | 三点一四 | pass |  |
| 百分比 | zh | tn | 25% | 百分之二十五 | 百分之二十五 | pass | 百分之二十五 | pass |  |
| 时间 | zh | tn | 10:30 | 十点三十分 | 十点三十分 | pass | 十点三十分 | pass |  |
| 日期 | zh | tn | 2026年6月12日 | 二零二六年六月十二日 | 二零二六年六月十二日 | pass | 二零二六年六月十二日 | pass |  |
| 日期上下文 | zh | tn | 今天是2026年6月12日 | 今天是二零二六年六月十二日 | 今天是二零二六年六月十二日 | pass | 今天是二零二六年六月十二日 | pass |  |
| 单位 | zh | tn | 12公斤 | 十二公斤 | 十二公斤 | pass | 十二公斤 | pass |  |
| 金额 | zh | tn | ￥12.50 |  | 十二点五零人民币 | observe | 十二点五零元 | observe | 金额读法不同，观察输出 |
| 电话 | zh | tn | 13800000000 | 幺三八零零零零零零零零 | 幺三八零零零零零零零零 | pass | 幺三八零零零零零零零零 | pass |  |
| 数字 | zh | itn | 一百二十三 | 123 | 123 | pass | 123 | pass |  |
| 小数 | zh | itn | 三点一四 | 3.14 | 3.14 | pass | 3.14 | pass |  |
| 百分比 | zh | itn | 百分之二十五 | 25% | 25% | pass | 25% | pass |  |
| 时间 | zh | itn | 上午十点三十分 | 上午 10:30 | 上午 10:30 | pass | 10:30a.m. | fail |  |
| 日期号 | zh | itn | 五月二十三号 | 5月23号 | 5月23号 | pass | 05/23 | fail |  |
| 日期日 | zh | itn | 四月二十三日 | 4月23日 | 4月23日 | pass | 04/23 | fail |  |
| 单位 | zh | itn | 十二公斤 | 12kg | 12kg | pass | 12kg | pass |  |
| 金额 | zh | itn | 十二元五角 | ¥12.5 | ¥12.5 | pass | ¥12.5 | pass |  |
| 金额 | zh | itn | 十二元五角三分 | ¥12.53 | ¥12.53 | pass | ¥12.53 | pass |  |
| 金额 | zh | itn | 十二元五分 | ¥12.05 | ¥12.05 | pass | ¥125分 | fail |  |
| 电话 | zh | itn | 幺三八零零零零零零零零 | 13800000000 | 13800000000 | pass | 13800000000 | pass |  |
| 数字 | en | tn | 123 | one hundred and twenty three | one hundred and twenty three | pass | one hundred and twenty three | pass |  |
| 小数 | en | tn | 3.14 | three point one four | three point one four | pass | three point one four | pass |  |
| 百分比 | en | tn | 25% | twenty five percent | twenty five percent | pass | twenty five percent | pass |  |
| 时间 | en | tn | 10:30 | ten thirty | ten thirty | pass | ten thirty | pass |  |
| 金额 | en | tn | $12.50 |  | twelve dollars fifty cents | observe | twelve point five dollars | observe | 金额读法不同，观察输出 |
| 单位 | en | tn | 12 kg | twelve kilograms | twelve kilograms | pass | twelve kilograms | pass |  |
| 数字 | en | itn | one hundred twenty three | 123 | 123 | pass | 123 | pass |  |
| 小数 | en | itn | three point one four | 3.14 | 3.14 | pass | 3.14 | pass |  |
| 百分比 | en | itn | twenty five percent | 25 % | 25 % | pass | 25 % | pass |  |
| 时间 | en | itn | ten thirty | 1030 | 1030 | pass | 1030 | pass |  |
| 金额 | en | itn | twelve dollars fifty cents | $12.50 | $12.50 | pass | $12.50 | pass |  |
| 单位 | en | itn | twelve kilograms | 12 kg | 12 kg | pass | 12 kg | pass |  |
| 多语言数字 | de | itn | ein hundert drei und zwanzig |  | 123 | observe | unsupported | unsupported |  |
| 多语言数字 | es | itn | ciento veintitrés |  | 123 | observe | unsupported | unsupported |  |
| 多语言数字 | fr | itn | cent vingt trois |  | 120 trois | observe | unsupported | unsupported |  |
| 多语言数字 | id | itn | seratus dua puluh tiga | 123 | 123 | pass | unsupported | unsupported |  |
| 多语言数字 | ja | itn | 百二十三 | 123 | 123 | pass | unsupported | unsupported |  |
| 多语言数字 | ko | itn | 백이십삼 |  | 백이십삼 | observe | unsupported | unsupported |  |
| 多语言数字 | pt | itn | cento e vinte três |  | 123 | observe | unsupported | unsupported |  |
| 多语言数字 | ru | itn | сто двадцать три |  | 123 | observe | unsupported | unsupported |  |
| 多语言数字 | tl | itn | isang daan dalawampu tatlo |  | 100 20 3 | observe | unsupported | unsupported |  |
| 多语言数字 | vi | itn | một trăm hai mươi ba |  | 123 | observe | unsupported | unsupported |  |
| 多语言TN | de | tn | 123 |  | ein hundert drei und zwanzig | observe | unsupported | unsupported |  |
| 多语言TN | es | tn | 123 |  | ciento veintitrés | observe | unsupported | unsupported |  |
| 多语言TN | ru | tn | 123 |  | сто двадцать три | observe | unsupported | unsupported |  |

## 热调用性能

| 语言 | 模式 | 输入 | itntext平均ms | itntext TPS |
|---|---|---|---:|---:|
| zh | tn | 今天是2026年6月12日 | 2.1729 | 460.2 |
| zh | itn | 上午十点三十分 | 0.4928 | 2029.0 |
| en | tn | $12.50 | 2.8957 | 345.3 |
| en | itn | twelve kilograms | 1.1024 | 907.1 |
| ja | itn | 百二十三 | 1.3586 | 736.0 |
| ru | tn | 123 | 40.0882 | 24.9 |

## 全语言可用性

| 模式 | 语言 | 状态 |
|---|---|---|
| itn | de | ok |
| itn | en | ok |
| itn | es | ok |
| itn | fr | ok |
| itn | id | ok |
| itn | ja | ok |
| itn | ko | ok |
| itn | pt | ok |
| itn | ru | ok |
| itn | tl | ok |
| itn | vi | ok |
| itn | zh | ok |
| tn | de | ok |
| tn | en | ok |
| tn | es | ok |
| tn | ru | ok |
| tn | zh | ok |
