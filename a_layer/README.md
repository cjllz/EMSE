# A 层：论文规则候选

这是按 MSR2018-DupPR 三条重复语义规则筛出的主人工复核队列。

- `candidates.csv`：124 对主复核候选
- `strict_candidates.csv`：87 对严格子集
- `annotations_template.csv`：可直接复制后填写的人工标注表
- `comment_evidence_*.parquet`、`pr_evidence.parquet`：候选对应的完整评论和 PR 证据
- `summary.json`：输入和输出统计

标签只能由人工填写。推荐标签：`confirmed_duplicate`、`not_duplicate`、`unclear`。

先打开 [核查索引](REVIEW_INDEX.md)，再复制 `reviewer_1.csv` / `reviewer_2.csv` 独立标注。详细标准见 [人工标注说明](../ANNOTATION_GUIDE.md)。旧 `annotations_template.csv` 是原管线格式；共同标注优先使用独立 reviewer 表，避免覆盖。
