# AIDev-DupPR v1 Protocol

## Scope

This protocol constructs a duplicate pull-request dataset from the user-selected
Hugging Face dataset `hao-li/AIDev-7.6M`, AIDev v5, revision
`37bbe1533e26cc1e1374917dba1186d1c8a4dc81` (cutoff: 2026-03-31).

The source has 7,685,281 AI-agent-authored pull requests. Confirmable duplicate
relations are restricted to the AIDev-pop subset (`pull_request.parquet`) because
the review-discussion tables needed to find and verify a relation are supplied
only for that subset. The full census can be used for descriptive follow-up work,
but it must not be represented as having complete duplicate-relation coverage.

The project uses this v5 population as its only analysis source.

## Operational Definition

A confirmed duplicate is a pair of pull requests in the same repository for
which all of the following hold:

1. The two PRs address the same intended change.
2. They were submitted by different GitHub contributors (`user_id` differs).
3. The later contributor was not demonstrably aware of the earlier PR at
   submission time. If evidence is unavailable, label this criterion `unclear`.
4. The PR discussion contains an explicit, affirmed duplicate decision, or an
   adjudicator can establish an equivalent project decision from the AIDev
   source records.

`agent` equality is retained as an analytic attribute, not used as a proxy for
same contributor. The contributor exclusion uses `user_id`, following the
source paper's rationale for excluding intentional self-duplicates.

## Collection Process

1. Select the 26 AIDev-pop repositories with the highest number of distinct PRs
   whose discussion has a resolvable same-repository PR reference (ties: eligible
   discussion count, repository ID). In each, randomly sample up to 200 comments that resolve
   to a different PR in the same repository.
2. Two raters label sampled comments as indicative or non-indicative. Indicative
   comments explicitly state a duplicate, replacement, closure in favour of,
   or prior implementation relation.
3. Update the versioned regular-expression rules from those labels. The shipped
   `aidev76_duplicate_rules_msr2018_adapted_v1.json` ports the three published
   MSR2018 rules and is a starting rule set, not a gold rule set.
4. Apply rules to all AIDev-pop ordinary comments, top-level reviews, and inline
   review comments. PR title/body text and title/issue similarity do not nominate
   candidates in this baseline.
5. Keep the resolved rule candidates in a full ledger. The main review queue
   excludes same-account pairs and positive evidence that the later contributor
   commented on the earlier PR before submission. Invalid/non-local references
   remain in the rule-match audit rather than becoming candidate pairs.
6. Independently annotate every candidate selected for the released dataset.
   Resolve disagreements through adjudication. Only `confirmed_duplicate` rows
   with a completed adjudication are final dataset rows.

## Evidence and Limits

The source exposes PR records, ordinary comments, inline review comments,
reviews, and structured related-issue links for the AIDev-pop subset. It does
not itself expose a duplicate-PR label. The baseline uses discussion rules only;
neither title nor issue similarity establishes duplication.

The protocol records direct evidence IDs, source type, timestamps, and snippets, but does not infer
that a review comment caused a code change, was resolved, or was useful. The
dataset will have unknown recall because unlinked or differently worded duplicate
decisions can be missed.

The v1 rule implementation is adapted directly from the original
[MSR2018-DupPR rules.py](https://github.com/Yuyue/MSR2018-DupPR/blob/master/code/rules.py).
It implements the original `AutoIdent.pre_filter` intent: validate PR references,
identify same-account pairs, and inspect prior comments and later-PR references.
The source provides current title/body snapshots rather than their submission-time
versions, so a title/body reference is an audit flag, not proof of prior awareness.
Different bot-generated contributions may share one GitHub account; same-account
exclusion follows the original rule but may remove distinct underlying requests.

## Output Status

输出均为候选、证据或人工工作表，当前没有自动确认的重复标签：

| 文件 | 保留范围 |
| --- | --- |
| `duplicate_candidate_ledger.csv` | 所有成功解析到本地、非自身 PR 对的规则候选，包括过滤命中。 |
| `duplicate_candidates.csv` | 排除 `same_author` 和 `prior_comment_awareness` 的主审查队列。 |
| `duplicate_prefilter_excluded.csv` | 命中同账号、提交前评论或 `snapshot_reference_flag` 至少一项的审计行。 |
| `duplicate_msr_compatible_candidates.csv` | 主队列进一步排除 `snapshot_reference_flag` 的严格兼容子集。 |

主队列保留快照引用行，因此它与过滤审计文件可能有交集。快照引用标记只说明
采集时标题/正文提到了较早 PR；人工必须核验该引用何时加入。缺少先前评论也
不能自动证明提交时不知情。时间相同或缺失的 PR 对不自动指定 master/duplicate。

`duplicate_annotations_template.csv` 的独立标注和裁决字段初始为空，
`candidate_pr_packet` 与 `candidate_comment_packet` 提供 PR 快照及完整讨论供核验。
只有完成独立标注、争议裁决，且标签为 `confirmed_duplicate` 的行才能进入最终
确认重复数据集。运行自动脚本本身不完成这些人工步骤。
