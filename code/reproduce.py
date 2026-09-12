# coding: utf-8
"""Generate the 899 rule-based candidate PR pairs on AIDev.

This script keeps the MSR2018 regular-expression rules but does not apply the
original MSR2018 author/awareness prefilters. The research dataset is the full
set of unique same-repository PR pairs resolved from rule matches.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
import sys

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import rules

PULL_URL_RE = re.compile(r"github\.com/([^/\s]+/[^/\s]+?)/pull/(\d+)")


def to_text(value) -> str:
    if value is None:
        return ""
    try:
        if pd.isna(value):
            return ""
    except (TypeError, ValueError):
        pass
    return str(value)


def extract_numbers(body: str) -> list[int]:
    numbers = []
    for pattern in rules.rules:
        for number in re.findall(pattern, to_text(body).lower()):
            if number:
                numbers.append(int(number))
    return numbers


def repo_name(url: str) -> str:
    match = re.search(r"github\.com/([^/\s]+/[^/\s]+?)(?:\.git)?/?$", to_text(url))
    return match.group(1) if match else to_text(url)


def load_prs(root: Path) -> pd.DataFrame:
    prs = pd.read_parquet(root / "pull_request.parquet", columns=[
        "id", "number", "title", "body", "agent", "user", "state",
        "created_at", "closed_at", "merged_at", "repo_id", "repo_url", "html_url",
    ])
    for column in ["id", "number", "repo_id"]:
        prs[column] = prs[column].astype("int64")
    for column in ["title", "body", "agent", "user", "state", "html_url", "repo_url"]:
        prs[column] = prs[column].map(to_text)
    for column in ["created_at", "closed_at", "merged_at"]:
        prs[column] = pd.to_datetime(prs[column], utc=True, errors="coerce")
    prs["repo_full_name"] = prs["repo_url"].map(repo_name)
    return prs


def load_comments(root: Path) -> pd.DataFrame:
    comments = pd.read_parquet(root / "pr_comments.parquet",
                               columns=["id", "pr_id", "user", "user_type", "created_at", "body"])
    comments = comments.rename(columns={"id": "comment_id", "user": "author"})
    comments["pr_id"] = pd.to_numeric(comments["pr_id"], errors="coerce")
    comments = comments.dropna(subset=["pr_id"]).copy()
    comments["pr_id"] = comments["pr_id"].astype("int64")
    for column in ["author", "user_type", "body"]:
        comments[column] = comments[column].map(to_text)
    comments["created_at"] = pd.to_datetime(comments["created_at"], utc=True, errors="coerce")
    return comments


def build_pairs(prs: pd.DataFrame, comments: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    by_repo_number = {(int(row.repo_id), int(row.number)): int(row.id)
                      for row in prs.itertuples(index=False)}
    by_id = prs.set_index("id", drop=False)
    evidence = defaultdict(list)
    counts = defaultdict(int)

    for row in comments.itertuples(index=False):
        if int(row.pr_id) not in by_id.index:
            continue
        source = by_id.loc[int(row.pr_id)]
        for target_number in extract_numbers(row.body):
            counts["rule_mentions"] += 1
            target_id = by_repo_number.get((int(source.repo_id), target_number))
            if target_id is None:
                counts["unresolved_references"] += 1
                continue
            if target_id == int(source.id):
                counts["self_references"] += 1
                continue
            target = by_id.loc[target_id]
            earlier, later = sorted([source, target], key=lambda item: int(item["number"]))
            evidence[(int(earlier.id), int(later.id))].append({
                "comment_id": int(row.comment_id),
                "comment_created_at": row.created_at,
                "comment_body": to_text(row.body),
            })

    rows = []
    for (earlier_id, later_id), events in sorted(evidence.items()):
        events.sort(key=lambda item: (pd.isna(item["comment_created_at"]),
                                      item["comment_created_at"], item["comment_id"]))
        earlier = by_id.loc[earlier_id]
        later = by_id.loc[later_id]
        first = events[0]
        rows.append({
            "pair_id": f"{int(earlier.number)}-{int(later.number)}",
            "master_pr_id": earlier_id,
            "duplicate_pr_id": later_id,
            "repo_id": int(earlier.repo_id),
            "repo_full_name": earlier.repo_full_name,
            "master_pr_number": int(earlier.number),
            "duplicate_pr_number": int(later.number),
            "master_title": earlier.title,
            "duplicate_title": later.title,
            "master_author": earlier.user,
            "duplicate_author": later.user,
            "master_agent": earlier.agent,
            "duplicate_agent": later.agent,
            "master_created_at": earlier.created_at,
            "duplicate_created_at": later.created_at,
            "master_state": earlier.state,
            "duplicate_state": later.state,
            "master_merged_at": earlier.merged_at,
            "duplicate_merged_at": later.merged_at,
            "master_url": earlier.html_url,
            "duplicate_url": later.html_url,
            "same_author": earlier.user == later.user,
            "evidence_count": len(events),
            "first_comment_id": first["comment_id"],
            "first_comment_created_at": first["comment_created_at"],
            "first_comment_body": first["comment_body"],
            "evidence_comment_ids": ";".join(str(item["comment_id"]) for item in events),
        })

    counts["resolved_references"] = sum(len(events) for events in evidence.values())
    counts["unique_pairs"] = len(rows)
    return pd.DataFrame(rows), dict(counts)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, default=Path("data/aidev-7.6m"))
    parser.add_argument("--output-dir", type=Path, default=Path("results/reproduction"))
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    pairs, counts = build_pairs(load_prs(args.data_root), load_comments(args.data_root))
    output = args.output_dir / "candidate_duplicates_unfiltered.csv"
    pairs.to_csv(output, index=False, encoding="utf-8-sig")
    summary = {
        "method": "MSR2018 regular-expression rules applied to AIDev comments",
        "rules_source": str(HERE / "rules.py"),
        "pairs": len(pairs),
        "counts": counts,
        "filters": "none beyond unresolved/self references",
        "output": str(output),
    }
    (args.output_dir / "summary.json").write_text(
        json.dumps(summary, indent=2, default=str), encoding="utf-8"
    )
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()


