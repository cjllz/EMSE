"""Prepare the readable, verified RQ1 sharing package; never assign labels."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import shutil
from pathlib import Path

import pandas as pd


def safe_text(value):
    return "" if pd.isna(value) else str(value)


def md(value):
    return html.escape(safe_text(value)).replace("|", "&#124;").replace("\r", "").replace("\n", "<br>")


def write_csv(frame, path):
    # Literal strings in the CSV stay untouched for reproducibility; import as
    # text when using spreadsheet software (see annotation guide).
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def prepare_layer(source, dest, layer):
    dest.mkdir(parents=True, exist_ok=True)
    for name in ["reviewer_1.csv", "reviewer_2.csv", "adjudication.csv"]:
        existing = dest / name
        if existing.exists() and pd.read_csv(existing).label.notna().any():
            raise ValueError(f"Refusing to overwrite completed annotations: {existing}")
    prefix = "duplicate" if layer == "A" else "broad_reference"
    candidates = pd.read_csv(source / f"{prefix}_candidates.csv")
    shutil.copyfile(source / f"{prefix}_candidates.csv", dest / "candidates.csv")
    if layer == "A":
        for old, new in [("duplicate_msr_compatible_candidates.csv", "strict_candidates.csv"), ("duplicate_annotations_template.csv", "annotations_template.csv"), ("candidate_summary.json", "summary.json")]:
            shutil.copyfile(source / old, dest / new)
    else:
        for old, new in [("broad_reference_candidates_all.csv", "all_candidates.csv"), ("broad_reference_evidence.csv", "reference_evidence.csv"), ("broad_reference_summary.json", "summary.json")]:
            shutil.copyfile(source / old, dest / new)
    pr_path = "candidate_pr_packet.parquet" if layer == "A" else "broad_candidate_pr_packet.parquet"
    comment_path = "candidate_comment_packet.parquet" if layer == "A" else "broad_candidate_comment_packet.parquet"
    prs = pd.read_parquet(source / pr_path)
    comments = pd.read_parquet(source / comment_path)
    ids = set(candidates.pr_id_a.astype("int64")) | set(candidates.pr_id_b.astype("int64"))
    prs = prs[prs.id.isin(ids)].copy()
    comments = comments[comments.pr_id.isin(ids)].copy()
    by_evidence = comments.drop_duplicates("evidence_id").set_index("evidence_id")
    needed = set(";".join(candidates.evidence_ids).split(";"))
    assert not needed - set(by_evidence.index), "Missing discussion evidence"
    assert len(candidates) == candidates.pair_id.nunique()
    prs.to_parquet(dest / "pr_evidence.parquet", index=False)
    shards = []
    for i, start in enumerate(range(0, len(comments), 5000), 1):
        name = f"comment_evidence_{i:02}.parquet"
        comments.iloc[start:start + 5000].to_parquet(dest / name, index=False)
        assert (dest / name).stat().st_size < 24_000_000, "Reduce shard size"
        shards.append(name)
    pages = []
    index = [f"# {layer} 层人工核查索引", "", "所有标签为空。每对需要两位同学独立阅读，标准见 [人工标注指南](../ANNOTATION_GUIDE.md)。", "", "| 序号 | PR 对 | 仓库 | 同账号 | 提交前评论 | 快照引用 |", "| --- | --- | --- | --- | --- | --- |"]
    entries = []
    for i, row in candidates.iterrows():
        page = f"review_{i // 40 + 1:03}.md"
        anchor = f"pair-{row.pair_id}"
        evidence_page = f"https://github.com/cjllz/EMSE/blob/cjllz-rq1/{dest.name}/{page}#{anchor}"
        if page not in pages:
            pages.append(page)
            (dest / page).write_text(f"# {layer} 层核查：第 {i // 40 + 1} 批\n\n[返回索引](REVIEW_INDEX.md) · [标注指南](../ANNOTATION_GUIDE.md)\n\n以下是候选线索，**不是人工结论**。摘录上限 4,000 字符，全文在本层评论 parquet 分片中；PR 链接显示的是当前 GitHub 状态。\n\n", encoding="utf-8")
        pair_link = f"[{row.pair_id}]({page}#{anchor})"
        repo = "/".join(str(row.html_url_a).split("/")[3:5])
        index.append(f"| {i+1} | {pair_link} | {md(repo)} | {row.same_author} | {row.prior_comment_awareness} | {row.snapshot_reference_flag} |")
        block = [f"## {anchor}", "", f"[{repo} PR #{row.pr_number_a}]({row.html_url_a}) 与 [PR #{row.pr_number_b}]({row.html_url_b})", "", f"- 标题 A：{md(row.title_a)}", f"- 标题 B：{md(row.title_b)}", f"- 作者：{md(row.author_a)} / {md(row.author_b)}", f"- 创建时间 UTC：{row.created_at_a} / {row.created_at_b}", f"- 风险标记：同账号={row.same_author}；提交前评论={row.prior_comment_awareness}；快照引用={row.snapshot_reference_flag}", ""]
        for eid in dict.fromkeys(row.evidence_ids.split(";")):
            e = by_evidence.loc[eid]
            body = safe_text(e.body)
            block += [f"### 证据 {eid}", "", f"类型：{e.comment_type}；来源 PR ID：{int(e.pr_id)}；时间：{e.created_at}；评论者：{md(e.user)}", "", "<pre>" + html.escape(body[:4000]) + "</pre>", ""]
            if len(body) > 4000:
                block += [f"（摘录，原文 {len(body):,} 字符。完整内容请按 evidence_id 在评论分片中读取。）", ""]
        with (dest / page).open("a", encoding="utf-8") as fh:
            fh.write("\n".join(block) + "\n")
        entries.append({"pair_id": row.pair_id, "layer": layer, "pr_url_a": row.html_url_a, "pr_url_b": row.html_url_b, "evidence_page": evidence_page, "same_intent": "", "different_accounts": "", "prior_awareness": "", "discussion_consensus": "", "label": "", "master_pr_id": "", "duplicate_pr_id": "", "evidence_notes": "", "reviewer_id": "", "reviewed_at_utc": ""})
    (dest / "REVIEW_INDEX.md").write_text("\n".join(index) + "\n", encoding="utf-8")
    template = pd.DataFrame(entries)
    for name in ["reviewer_1.csv", "reviewer_2.csv", "adjudication.csv"]:
        write_csv(template, dest / name)
    stats = {"layer": layer, "candidate_pairs": len(candidates), "unique_prs": len(prs), "repositories": int(candidates.repo_id.nunique()), "discussion_rows": len(comments), "required_evidence_ids": len(needed), "missing_evidence_ids": 0, "comment_shards": shards, "review_pages": len(pages), "same_author_pairs": int(candidates.same_author.sum()), "prior_comment_awareness_pairs": int(candidates.prior_comment_awareness.sum()), "snapshot_reference_pairs": int(candidates.snapshot_reference_flag.sum()), "manual_labels_filled": 0}
    (dest / "review_summary.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a-source", type=Path, required=True)
    parser.add_argument("--b-source", type=Path, required=True)
    parser.add_argument("--release-root", type=Path, default=Path("."))
    args = parser.parse_args()
    a = prepare_layer(args.a_source, args.release_root / "a_layer", "A")
    b = prepare_layer(args.b_source, args.release_root / "b_layer", "B")
    ac = pd.read_csv(args.a_source / "duplicate_candidates.csv")
    bc = pd.read_csv(args.b_source / "broad_reference_candidates_all.csv")
    assert not set(ac.pair_id) & set(bc.pair_id), "A and B overlap"
    result = {"A": a, "B_priority": b, "B_pool_pairs": len(bc), "A_B_pair_overlap": 0, "interpretation": "RQ1 candidate construction stage; annotation incomplete; no confirmed count or prevalence estimate."}
    (args.release_root / "verification.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
