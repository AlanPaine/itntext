# itntext 全场景与 wetext 对比报告

## 总览

- 总用例：58 个。
- 有明确期望的用例：41 个，itntext 通过 41 个，通过率 100.0%。
- wetext 可对比且有明确期望的用例：38 个，wetext 通过 34 个，通过率 89.5%。
- 观察类用例：17 个，主要用于金额/货币格式、多语言上游覆盖差异和歧义表达。
- itntext 失败/异常用例：0 个。
- ITN 语言：`de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh`。
- TN 语言：`de, en, es, ru, zh`。

## 场景输出

| 类别 | 语言 | 模式 | 输入 | 期望 | itntext | 状态 | wetext | wetext状态 | 说明 |
|---|---|---|---|---|---|---|---|---|---|
| 数字 | zh | tn | 0 | 零 | 零 | pass | 零 | pass |  |
| 数字 | zh | tn | 123 | 一百二十三 | 一百二十三 | pass | 一百二十三 | pass |  |
| 数字 | zh | tn | 1001 | 一千零一 | 一千零一 | pass | 一千零一 | pass |  |
| 长数字/电话 | zh | tn | 13800000000 | 幺三八零零零零零零零零 | 幺三八零零零零零零零零 | pass | 幺三八零零零零零零零零 | pass |  |
| 小数 | zh | tn | 3.14 | 三点一四 | 三点一四 | pass | 三点一四 | pass |  |
| 百分比 | zh | tn | 25% | 百分之二十五 | 百分之二十五 | pass | 百分之二十五 | pass |  |
| 时间 | zh | tn | 10:30 | 十点三十分 | 十点三十分 | pass | 十点三十分 | pass |  |
| 日期 | zh | tn | 2026年6月12日 | 二零二六年六月十二日 | 二零二六年六月十二日 | pass | 二零二六年六月十二日 | pass |  |
| 日期上下文 | zh | tn | 今天是2026年6月12日 | 今天是二零二六年六月十二日 | 今天是二零二六年六月十二日 | pass | 今天是二零二六年六月十二日 | pass |  |
| 单位 | zh | tn | 12公斤 | 十二公斤 | 十二公斤 | pass | 十二公斤 | pass |  |
| 金额/货币 | zh | tn | ￥12.50 |  | 十二点五零人民币 | observe | 十二点五零元 | observe | 中文 TN 金额读法不同，观察输出 |
| 金额/货币 | zh | tn | $12.50 |  | 十二点五零美元 | observe | 十二点五零美元 | observe | 货币名和符号读法不同，观察输出 |
| 数字 | zh | itn | 一百二十三 | 123 | 123 | pass | 123 | pass |  |
| 小数 | zh | itn | 三点一四 | 3.14 | 3.14 | pass | 3.14 | pass |  |
| 百分比 | zh | itn | 百分之二十五 | 25% | 25% | pass | 25% | pass |  |
| 分数 | zh | itn | 三分之一 | 1/3 | 1/3 | pass | 1/3 | pass |  |
| 时间 | zh | itn | 上午十点三十分 | 上午 10:30 | 上午 10:30 | pass | 10:30a.m. | fail |  |
| 时间 | zh | itn | 下午三点零五分 |  | 下午 03:05 | observe | 3:05p.m. | observe | 观察中文时间更复杂表达 |
| 日期 | zh | itn | 五月二十三号 | 5月23号 | 5月23号 | pass | 05/23 | fail |  |
| 日期 | zh | itn | 四月二十三日 | 4月23日 | 4月23日 | pass | 04/23 | fail |  |
| 单位 | zh | itn | 十二公斤 | 12kg | 12kg | pass | 12kg | pass |  |
| 单位 | zh | itn | 三公里 | 3km | 3km | pass | 3km | pass |  |
| 金额/货币 | zh | itn | 十二元五角 | ¥12.5 | ¥12.5 | pass | ¥12.5 | pass |  |
| 金额/货币 | zh | itn | 十二元五角三分 | ¥12.53 | ¥12.53 | pass | ¥12.53 | pass |  |
| 金额/货币 | zh | itn | 十二元五分 | ¥12.05 | ¥12.05 | pass | ¥125分 | fail |  |
| 金额/货币 | zh | itn | 十二美元 | $12 | $12 | pass | $12 | pass |  |
| 长数字/电话 | zh | itn | 幺三八零零零零零零零零 | 13800000000 | 13800000000 | pass | 13800000000 | pass |  |
| 电子类 | zh | itn | 一二三点四五 |  | 123.45 | observe | 123.45 | observe | 观察电子/小数边界 |
| 数字 | en | tn | 123 | one hundred and twenty three | one hundred and twenty three | pass | one hundred and twenty three | pass |  |
| 数字 | en | tn | 1001 | one thousand one | one thousand one | pass | one thousand one | pass |  |
| 小数 | en | tn | 3.14 | three point one four | three point one four | pass | three point one four | pass |  |
| 百分比 | en | tn | 25% | twenty five percent | twenty five percent | pass | twenty five percent | pass |  |
| 时间 | en | tn | 10:30 | ten thirty | ten thirty | pass | ten thirty | pass |  |
| 日期 | en | tn | 01/02/2026 |  | january second twenty twenty six | observe | the second of january twenty twenty six | observe | 英文日期歧义，观察输出 |
| 金额/货币 | en | tn | $12.50 |  | twelve dollars fifty cents | observe | twelve point five dollars | observe | wetext 和 itntext 货币读法不同 |
| 金额/货币 | en | tn | €12.50 |  | twelve euros fifty cents | observe | twelve point five euros | observe | 观察欧元读法 |
| 单位 | en | tn | 12 kg | twelve kilograms | twelve kilograms | pass | twelve kilograms | pass |  |
| 数字 | en | itn | one hundred twenty three | 123 | 123 | pass | 123 | pass |  |
| 小数 | en | itn | three point one four | 3.14 | 3.14 | pass | 3.14 | pass |  |
| 百分比 | en | itn | twenty five percent | 25 % | 25 % | pass | 25 % | pass |  |
| 时间 | en | itn | ten thirty | 1030 | 1030 | pass | 1030 | pass |  |
| 金额/货币 | en | itn | twelve dollars fifty cents | $12.50 | $12.50 | pass | $12.50 | pass |  |
| 金额/货币 | en | itn | twelve euros | €12 | €12 | pass | €12 | pass |  |
| 单位 | en | itn | twelve kilograms | 12 kg | 12 kg | pass | 12 kg | pass |  |
| 电话 | en | itn | one two three four | 1234 | 1234 | pass | 1234 | pass |  |
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
| 多语言TN | ru | tn | 123 | сто двадцать три | сто двадцать три | pass | unsupported | unsupported |  |

## 热调用性能

| 语言 | 模式 | 输入 | itntext平均ms | itntext中位ms | itntext TPS | wetext平均ms | wetext中位ms | wetext TPS |
|---|---|---|---:|---:|---:|---:|---:|---:|
| zh | tn | 今天是2026年6月12日 | 2.1460 | 2.0669 | 465.7 | 3.1153 | 3.0957 | 320.8 |
| zh | itn | 上午十点三十分 | 0.4902 | 0.4829 | 2036.8 | 1.1055 | 1.0781 | 903.7 |
| zh | itn | 十二元五角三分 | 0.6315 | 0.6224 | 1581.3 | 1.1030 | 1.0888 | 905.8 |
| en | tn | $12.50 | 2.8126 | 2.7804 | 355.4 | 5.5501 | 5.4956 | 180.1 |
| en | itn | twelve dollars fifty cents | 2.0451 | 2.0106 | 488.6 | 1.7617 | 1.7172 | 567.2 |
| ja | itn | 百二十三 | 1.3370 | 1.3244 | 747.3 |  |  |  |
| ru | tn | 123 | 38.6735 | 38.0509 | 25.9 |  |  |  |

## 结论

- 中文核心修复场景保持通过，包括数字、日期、时间、百分比、单位、元角分金额和长数字/电话。
- wetext 仅对 `zh/en` 参与对比；多语言部分以 itntext 的可用性和输出观察为主。
- 金额/货币在 TN 侧存在风格差异，报告保留为观察项，避免把有歧义的读法误判为失败。
- 性能部分覆盖中文、英文、日语和俄语；俄语 TN 仍是热调用最慢场景。
