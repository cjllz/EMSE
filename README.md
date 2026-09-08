# RQ1：AIDev 中的重复 PR 候选

## 先看结论

我们用 AIDev v5 的 pop 子集，寻找“一个 PR 的讨论提到同仓库另一个 PR”的关系，再参考 MSR2018-DupPR 的三条规则筛选。这里一行代表一对 PR，不是一条 PR。结果只是待人工核查的候选，不是已经确认的重复关系。

- **A 层**：932 对规则命中，保留 124 对主审核候选；其中 87 对是进一步排除快照引用后的严格子集（87 已包含在 124 内）。
- **B 层**：7,297 对放宽规则后的扩展池，按检索信号排序后优先审核 1,500 对；与 A 完全不重复。优先 1,500 对中 1,309 对为同一 GitHub 账号，只有 191 对不同账号，因此 B 主要用于扩大召回，不是高置信结果。

两层都必须由两位同学独立阅读、标注，再对分歧裁决，才能报告最终确认数量。

## 我们实际做了什么

数据来自 `hao-li/AIDev-7.6M` v5，固定 revision `37bbe1533e26cc1e1374917dba1186d1c8a4dc81`。pop 中有 361,296 个 PR 和 944,499 条普通评论、Review 正文及行内 Review 评论。A 层检查 duplicate、replaced、fixed by 等论文式表达；B 层不要求出现 duplicate 词，而是收集所有可解析的同仓库 PR 引用，再按引用数量、论文式信号、作者和时间排序。数据快照截止 2026-03-31；当前 GitHub 页面可能已经变化。

## 文件怎么读

下载后直接双击 `a_layer/review.html` 或 `b_layer/review.html`，按 `pair_id` 搜索即可看到两个 PR 的链接、标题、作者、时间和原始评论摘录；`evidence_page` 已指向本地 `review.html#pair-<id>`。两位同学分别填写各层的 `reviewer_1.csv`、`reviewer_2.csv`，最终在 `adjudication.csv` 保留裁决，不能覆盖原始标注。

候选 CSV 的主要字段：`pair_id`（PR 对编号）、`pr_id_a/pr_id_b`、`pr_number_a/pr_number_b`、`title_a/title_b`、`author_a/author_b`、`html_url_a/html_url_b`、创建时间、`earlier_pr_id/later_pr_id`、`evidence_ids`、`same_author`、`prior_comment_awareness`、`snapshot_reference_flag`。B 另有 `tier` 和 `retrieval_score`，只是排序信号。评论证据可按 `evidence_id` 在 `comment_evidence_*.parquet` 分片中回查；PR 信息在 `pr_evidence.parquet`。完整评论分片只为 A 的 124 对和 B 优先 1,500 对提供；B 全池 7,297 对只有候选表。

导入 Excel 前建议把 ID、`pair_id`、URL 和日期列设为“文本”，避免科学计数法、前导数字丢失或公式触发。不要把 `same_author` 标记直接当作重复结论。

## 复现

在本目录根部使用 Python 3.12：

```text
python -m pip install -r requirements.txt
python code/download_aidev76_pop.py --data-dir inputs/aidev-7.6m
python code/build_aidev76_duppr.py --data-root inputs/aidev-7.6m --output-dir results/aidev76_duppr
python code/build_aidev76_broad_candidates.py --data-root inputs/aidev-7.6m --output-dir results/aidev76_broad_final --max-candidates 1500 --rule-matches-path results/aidev76_duppr/rule_matches.csv --exclude-pairs-path results/aidev76_duppr/duplicate_candidates.csv
python code/prepare_rq1_release.py --a-source results/aidev76_duppr --b-source results/aidev76_broad_final --release-root .
python code/test_rq1_release.py
```

`code/` 中包含下载、A 层构建、B 层构建、发布整理和测试脚本。论文规则来源：[MSR2018-DupPR code](https://github.com/Yuyue/MSR2018-DupPR/tree/master/code)。本发布包不含原始 AIDev parquet；需先下载并校验 pop 数据。
