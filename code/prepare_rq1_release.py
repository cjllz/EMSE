"""Prepare the readable, verified RQ1 sharing package; never assign labels."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_review_html import build as build_review_html


def safe_text(value):
    return "" if pd.isna(value) else str(value)


def write_csv(frame, path):
    # Literal strings in the CSV stay untouched for reproducibility; import as
    # text when using spreadsheet software (see annotation guide).
    frame.to_csv(path, index=False, encoding="utf-8-sig")


def prepare_layer(source, dest, layer):
    dest.mkdir(parents=True, exist_ok=True)
    annotation_fields = ["same_intent", "different_accounts", "prior_awareness", "discussion_consensus", "label", "master_pr_id", "duplicate_pr_id", "evidence_notes", "reviewer_id", "reviewed_at_utc"]
    for name in ["reviewer_1.csv", "reviewer_2.csv", "adjudication.csv"]:
        existing = dest / name
        if existing.exists():
            old = pd.read_csv(existing, dtype=str, keep_default_na=False)
            present = [field for field in annotation_fields if field in old.columns]
            if present and old[present].apply(lambda col: col.str.strip()).ne("").any().any():
                raise ValueError(f"Refusing to overwrite completed annotations: {existing}")
    prefix = "duplicate" if layer == "A" else "broad_reference"
    candidates = pd.read_csv(source / f"{prefix}_candidates.csv")
    shutil.copyfile(source / f"{prefix}_candidates.csv", dest / "candidates.csv")
    if layer == "A":
        for old, new in [("duplicate_msr_compatible_candidates.csv", "strict_candidates.csv"), ("candidate_summary.json", "summary.json")]:
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
    entries = []
    for _, row in candidates.iterrows():
        entries.append({"pair_id": row.pair_id, "layer": layer, "pr_url_a": row.html_url_a, "pr_url_b": row.html_url_b, "evidence_page": f"review.html#pair-{row.pair_id}", "same_intent": "", "different_accounts": "", "prior_awareness": "", "discussion_consensus": "", "label": "", "master_pr_id": "", "duplicate_pr_id": "", "evidence_notes": "", "reviewer_id": "", "reviewed_at_utc": ""})
    template = pd.DataFrame(entries)
    for name in ["reviewer_1.csv", "reviewer_2.csv", "adjudication.csv"]:
        write_csv(template, dest / name)
    build_review_html(dest)
    stats = {"layer": layer, "candidate_pairs": len(candidates), "unique_prs": len(prs), "repositories": int(candidates.repo_id.nunique()), "discussion_rows": len(comments), "required_evidence_ids": len(needed), "missing_evidence_ids": 0, "comment_shards": shards, "review_pages": 1, "same_author_pairs": int(candidates.same_author.sum()), "prior_comment_awareness_pairs": int(candidates.prior_comment_awareness.sum()), "snapshot_reference_pairs": int(candidates.snapshot_reference_flag.sum()), "manual_labels_filled": 0}
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
