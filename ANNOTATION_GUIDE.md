# 人工标注怎么做

这批数据是 RQ1 候选构建阶段。先从每层 `review.html` 阅读证据，必要时查评论 Parquet 全文；点 GitHub 链接补查时，把日期和链接记入备注，因为当前网页可能不同于 2026-03-31 的数据快照。

两位同学分别填写 `reviewer_1.csv`、`reviewer_2.csv`，不要先商量标签。`pair_id`、`layer`、两条 URL 和 `evidence_page` 不改；后者指向本地 `review.html#pair-<id>`。主要判断项统一填 `yes/no/unclear`：

- `same_intent`：两份 PR 是否想完成同一项修改。
- `different_accounts`：是否不同 GitHub 账号。同账号填 `no`，备注写 `same_account`，不算原定义正例，不能为凑数量改定义。
- `prior_awareness`：后提交者提交时是否已知情。没有查到先前评论不等于不知情，应填 `unclear`。
- `discussion_consensus`：讨论是否明确认可重复或等价处理决定。普通引用、依赖、后续修复和相似标题不自动算重复。

只有同仓库、前三项分别为 `yes/yes/no`，且决定为 `yes`，才能填 `label=confirmed_duplicate`；明确否定必要条件填 `not_duplicate`，证据不足或含糊填 `unclear`。确认后补 `master_pr_id`、`duplicate_pr_id`；在 `evidence_notes` 写理由、证据 ID 和原句，再填 `reviewer_id`、UTC 时间 `reviewed_at_utc`。

保留两份原记录，在 `adjudication.csv` 填最终同名判断项、标签和理由。分歧请讨论或第三人裁决；两人一致也要审核条件是否完整。summary 的数量不是确认数；B 的 1,500 对是排序后的工作量预算，不是随机样本，不能估算总体重复率。
