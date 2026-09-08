# RQ1：AIDev 中的重复 PR 候选

## 一句话说明

我们从 AIDev v5 的 pop 子集里寻找“一个 PR 明确提到同仓库另一个 PR”的关系，再用 MSR2018-DupPR 的规则做第一轮筛选。最终得到两层候选，供两位同学独立阅读和标注。

这两层都不是已经确认的重复 PR。只有完成双人标注和分歧裁决后，才能形成最终重复数据集。

## 数据范围

- AIDev v5 pop 子集，固定 revision：`37bbe1533e26cc1e1374917dba1186d1c8a4dc81`
- 361,296 个 PR
- 944,499 条讨论证据：普通评论、Review 正文、行内 Review 评论
- 本仓库没有上传原始 AIDev 数据，避免提交大文件和无关数据

## A 层：论文规则候选

A 层移植并适配论文代码中的三条重复语义规则，例如 duplicate、replaced、fixed by 等表达。它是自动筛选阶段，不是完整复现了人工标注流程。

- 932 对规则候选总账
- 124 对主人工复核候选
- 87 对更严格子集：进一步排除了快照中提到早期 PR 的情况

124 对不是 124 条已确认重复关系。932 对中有不少因为同一作者、提交前知情或快照引用而需要人工判断。

## B 层：高召回扩展候选

B 层不要求评论一定出现 duplicate 词，而是收集所有可解析的同仓库 PR 引用，再按证据数量、是否出现 A 层重复语义、作者和时间信息排序。B 层已经排除了 A 层的 124 对。

- B 全池：7,297 对
- B 优先复核队列：1,500 对
- 1,500 只是人工工作量上限，不是随机样本，也不能用来估计重复率
- 这 1,500 对中有 1,309 对属于同一 GitHub 账号提交，只有 191 对不是同账号；因此 B 层主要是扩大召回的检索池，不是高置信结果。
- 进一步看，B 优先队列中只有 115 对同时没有提交前评论知情标记，75 对再没有快照引用标记；这些是风险筛查数字，不是自动确认结果。

B 层预期会有更多误报；具体准确率尚未标注验证。很多引用可能只是“参考”“相关”“修复依据”，不一定是重复关系。全池 7,297 对中仅 849 对不同账号，同时没有提交前评论标记的为 580 对。此前“排除同作者仍远超千对”的估计不成立。

B 中 `tier` 是排序信号代码，不是新的研究层：`A_explicit_duplicate_cue` 只表示命中过论文规则（这 808 对因风险过滤未进入研究 A 层）；`B_repeated_or_cross_evidence_reference` 表示重复或多来源引用；`C_single_same_repository_reference` 表示单次引用。全体 B 都是补充候选池，不改变原论文的重复定义。

B 层与 A 层不重复。B 层全池保留在 `all_candidates.csv`，优先复核队列保留在 `candidates.csv`。证据可在 `reference_evidence.csv` 和 `comment_evidence_*.parquet` 分片中按 `evidence_id` 回查。

## 同学怎么标注

1. 先看对应层的候选 CSV，查看两个 PR 的标题、作者、时间和链接。
2. 根据 `evidence_ids`，在对应的评论证据文件中阅读原始评论。
3. 两位同学分别填写自己的标签：`confirmed_duplicate`、`not_duplicate` 或 `unclear`。
4. 如果确认重复，填写哪个是 master PR、哪个是 duplicate PR，以及理由。
5. 两人意见不一致时讨论或请第三人裁决，在独立的 `adjudication.csv` 中填写最终 `label` 和理由；一致的记录也要完成最终核验。

更方便的查阅入口：

- [A 层核查索引](a_layer/REVIEW_INDEX.md)
- [B 层核查索引](b_layer/REVIEW_INDEX.md)
- [统一人工标注说明](ANNOTATION_GUIDE.md)
- 每层的 `reviewer_1.csv`、`reviewer_2.csv` 为独立填写文件，`adjudication.csv` 为最后裁决表。

需要特别检查：

- 两个 PR 是否确实处理同一个问题；
- 是否只是普通引用、依赖关系或后续修复；
- 两个 PR 是否由同一 GitHub 账号提交；
- 后一个 PR 提交前，作者是否已经知道前一个 PR；
- 引用来自采集时快照，不能单独证明提交时已经知情。

## 目录

- `a_layer/`：A 层候选和证据
- `b_layer/`：B 层候选和证据
- `code/`：复现脚本和测试
- `research/`：方法说明和规则来源

## 复现

使用 Python 3.12，在仓库根目录执行。输入目录与结果目录彼此分开，原始数据不纳入 Git。

```text
python -m pip install pandas==2.2.3 pyarrow==23.0.1 fsspec==2025.3.0 requests==2.32.5
python code/download_aidev76_pop.py --data-dir inputs/aidev-7.6m
python code/build_aidev76_duppr.py --data-root inputs/aidev-7.6m --output-dir results/aidev76_duppr
python code/build_aidev76_broad_candidates.py --data-root inputs/aidev-7.6m --output-dir results/aidev76_broad_final --max-candidates 1500 --rule-matches-path results/aidev76_duppr/rule_matches.csv --exclude-pairs-path results/aidev76_duppr/duplicate_candidates.csv
python code/prepare_rq1_release.py --a-source results/aidev76_duppr --b-source results/aidev76_broad_final --release-root .
python code/test_build_aidev76_duppr.py
```

种子抽样 26 个仓库、1,994 条跨 PR 评论已在自动处理中生成，但还未进行双人审读和本数据集规则校准。两层候选不能直接得出 AIDev 总体重复率。数据仅覆盖所选 pop 中的 AI PR 对，指向 pop 外的 PR 尚未补齐。

提交内容不包含 AIDev 原始 parquet、完整原始评论表或本地临时文件。若要重新运行，需要按 `code/download_aidev76_pop.py` 下载并校验 pop 数据。

论文来源：`msr2018.pdf`（不上传原 PDF）。规则参考：[MSR2018-DupPR code](https://github.com/Yuyue/MSR2018-DupPR/tree/master/code)。
