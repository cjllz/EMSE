# B 层：高召回扩展候选

这是与 A 层不重复的扩展人工复核池。它收集所有可解析的同仓库 PR 引用，不要求评论必须出现 duplicate 词。

- `all_candidates.csv`：7,297 对 B 层全池
- `candidates.csv`：按检索分数排序的前 1,500 对优先队列
- `reference_evidence.csv`：所有引用证据索引
- `comment_evidence_*.parquet`、`pr_evidence.parquet`：优先队列的完整可回查证据
- `summary.json`：输入和输出统计

B 层召回高、误报也高。优先队列不是随机样本，不能用来估计总体重复率。标注前必须检查同账号、提交前知情、快照引用以及“只是参考/相关/修复”的情况。

先打开 [核查索引](REVIEW_INDEX.md)，再复制 `reviewer_1.csv` / `reviewer_2.csv` 独立标注。详细标准见 [人工标注说明](../research/ANNOTATION_GUIDE.md)。
