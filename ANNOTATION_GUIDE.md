# RQ1 人工标注说明

本轮成果是 **RQ1 候选构建阶段**，不是确认重复数据集。A 层有 124 对论文规则候选，其中 87 对为更严格子集；B 层有 7,297 对扩展候选，优先检查其中 1,500 对。A、B 互不重复，87 不能再与 124 相加。JSON summary 中的数字均为候选数；B 的 1,500 对按检索信号排序，不是随机样本，不能据此估算总体重复率。

## 判断标准

原论文式正例须同时满足：两个 PR 属于同仓库、账号不同、想完成同一项修改、后提交者在提交时不知情，并有明确的重复或等价处理决定。每项按证据填 `yes`、`no` 或 `unclear`；缺少证据不是证明“不知情”。

这里 `prior_awareness=yes` 表示后提交者已知情，`no` 表示有证据支持其不知情；只是没有查到先前评论，应填 `unclear`。`discussion_consensus=yes` 必须有明确、被认可的项目处理决定；单纯引用、相似标题、共享 Issue、替代或关联说法不自动等于重复。

B 层保留了大量同账号关系。对此填 `different_accounts=no`、`label=not_duplicate`，在 `evidence_notes` 写 `same_account`；它们不算原定义正例，不得为凑数量改变定义。确需研究同账号关系时，应另设研究定义和结果，不混入本批正例。

## 两人独立检查

1. 每对先点击 `evidence_page` 打开分批 Markdown 证据页，核对两份 PR 的目标、作者、时间与原始讨论。需要全文时查 Parquet 分片或 `pr_url_a`、`pr_url_b`。GitHub 当前网页可能已更新；必须区分网页现状与截至 **2026-03-31** 的数据快照，并在备注记录外部补查时间及链接。
2. 两位同学各自填写 `reviewer_1.csv`、`reviewer_2.csv`，不要先商量标签或覆盖对方记录。字段如下：

```text
pair_id,layer,pr_url_a,pr_url_b,evidence_page,same_intent,different_accounts,prior_awareness,discussion_consensus,label,master_pr_id,duplicate_pr_id,evidence_notes,reviewer_id,reviewed_at_utc
```

四个 criteria 字段统一填 `yes/no/unclear`。`label` 只填 `confirmed_duplicate/not_duplicate/unclear`。只有全部条件被证据支持（`prior_awareness=no`，其余三个为 `yes`）才填 `confirmed_duplicate`；证据明确否定必要条件时填 `not_duplicate`；引用含糊、讨论未形成决定或证据不足时填 `unclear`，不要猜测。确认时填写主 PR、重复 PR 的 ID，通常以前后提交时间定位，但时间相同或缺失时须人工核验。备注写清判断理由、引用原句及证据 ID；时间使用 UTC。

## 汇总与裁决

保留两人的原始文件，在 `adjudication.csv` 中另存最终同名 criteria、标签、PR ID 和理由。分歧由讨论或第三人裁决；即使两人标签一致，也必须审核最终 criteria 是否完整、是否支持该标签。裁决仍无法消除多义性时保留 `unclear`。只有完成这一步的正例才能计入最终确认重复数量；报告时同时保留负例和不明确项。
