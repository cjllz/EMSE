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

A 层严格模仿论文中的三条重复语义规则，例如 duplicate、replaced、fixed by 等表达。

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

B 层的误报会明显高于 A 层。很多引用可能只是“参考”“相关”“修复依据”，不一定是重复关系。

B 层与 A 层不重复。B 层全池保留在 `all_candidates.csv`，优先复核队列保留在 `candidates.csv`。证据可在 `reference_evidence.csv` 和 `comment_evidence.parquet` 中按 `evidence_id` 回查。

## 同学怎么标注

1. 先看对应层的候选 CSV，查看两个 PR 的标题、作者、时间和链接。
2. 根据 `evidence_ids`，在对应的评论证据文件中阅读原始评论。
3. 两位同学分别填写自己的标签：`confirmed_duplicate`、`not_duplicate` 或 `unclear`。
4. 如果确认重复，填写哪个是 master PR、哪个是 duplicate PR，以及理由。
5. 两人意见不一致时，再填写 `adjudicated_label` 和裁决理由。

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

提交内容不包含 AIDev 原始 parquet、完整原始评论表或本地临时文件。若要重新运行，需要按 `code/download_aidev76_pop.py` 下载并校验 pop 数据。

论文来源：`msr2018.pdf`（不上传原 PDF）。规则参考：[MSR2018-DupPR code](https://github.com/Yuyue/MSR2018-DupPR/tree/master/code)。
