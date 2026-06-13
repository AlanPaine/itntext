# itntext 与 wetext 对比报告

## API 对比

- itntext 构造签名：`(**kwargs)`
- wetext 构造签名：`(**kwargs)`
- itntext 调用方式保持 wetext 风格：`Normalizer(lang='zh', operator='tn').normalize(text)`
- itntext ITN 支持语言：`de, en, es, fr, id, ja, ko, pt, ru, tl, vi, zh`
- itntext TN 支持语言：`de, en, es, ru, zh`

## 输出对比

| lang | operator | input | itntext | wetext | same |
|---|---|---|---|---|---|
| zh | tn | 123 | 一百二十三 | 一百二十三 | yes |
| zh | tn | 今天是2026年6月12日 | 今天是二零二六年六月十二日 | 今天是二零二六年六月十二日 | yes |
| zh | tn | 13800000000 | 幺三八零零零零零零零零 | 幺三八零零零零零零零零 | yes |
| zh | itn | 五月二十三号 | 5月23号 | 05/23 | no |
| zh | itn | 上午十点三十分 | 上午 10:30 | 10:30a.m. | no |
| zh | itn | 十二元五角三分 | ¥12.53 | ¥12.53 | yes |
| en | tn | 123 | one hundred and twenty three | one hundred and twenty three | yes |
| en | tn | $12.50 | twelve dollars fifty cents | twelve point five dollars | no |
| en | itn | one hundred twenty three | 123 | 123 | yes |
| en | itn | twelve kilograms | 12 kg | 12 kg | yes |

## 首次调用耗时

| lang | operator | input | itntext_ms | wetext_ms |
|---|---|---|---:|---:|
| zh | tn | 123 | 11.088 | 1.340 |
| zh | tn | 今天是2026年6月12日 | 2.102 | 3.081 |
| zh | tn | 13800000000 | 1.925 | 3.115 |
| zh | itn | 五月二十三号 | 11.842 | 1.041 |
| zh | itn | 上午十点三十分 | 0.522 | 1.197 |
| zh | itn | 十二元五角三分 | 0.658 | 1.125 |
| en | tn | 123 | 182.643 | 4.549 |
| en | tn | $12.50 | 2.935 | 5.633 |
| en | itn | one hundred twenty three | 23.478 | 1.900 |
| en | itn | twelve kilograms | 1.109 | 0.974 |
