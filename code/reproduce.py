# coding: utf-8
"""Generate lookup tables for rule-based candidate PR pairs on AIDev."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import rules


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
    url = to_text(url)

    match = re.search(
        r"github\.com/repos/([^/\s]+/[^/\s]+)",
        url,
    )

    if match:
        return match.group(1)

    match = re.search(
        r"github\.com/([^/\s]+/[^/\s]+)",
        url,
    )

    if match:
        return match.group(1)

    return url


def load_prs(root: Path) -> pd.DataFrame:
    columns = [
        "id",
        "number",
        "title",
        "user",
        "agent",
        "created_at",
        "repo_id",
        "repo_url",
        "html_url",
    ]

    prs = pd.read_parquet(
        root / "pull_request.parquet",
        columns=columns,
    )

    for column in ["id", "number", "repo_id"]:
        prs[column] = pd.to_numeric(
            prs[column],
            errors="coerce",
        )

    prs = prs.dropna(
        subset=["id", "number", "repo_id"]
    ).copy()

    for column in ["id", "number", "repo_id"]:
        prs[column] = prs[column].astype("int64")

    for column in [
        "title",
        "user",
        "agent",
        "repo_url",
        "html_url",
    ]:
        prs[column] = prs[column].map(to_text)

    prs["created_at"] = pd.to_datetime(
        prs["created_at"],
        utc=True,
        errors="coerce",
    )

    prs["repo_full_name"] = prs["repo_url"].map(repo_name)

    return prs


def load_evidence(root: Path) -> list[dict]:
    events = []

    # 1. 普通 PR 评论
    comments = pd.read_parquet(
        root / "pr_comments.parquet",
        columns=[
            "id",
            "pr_id",
            "user",
            "user_type",
            "created_at",
            "body",
        ],
    )

    for row in comments.itertuples(index=False):
        pr_id = pd.to_numeric(row.pr_id, errors="coerce")

        if pd.isna(pr_id):
            continue

        events.append(
            {
                "source": "pr_comments",
                "event_id": int(row.id),
                "source_pr_id": int(pr_id),
                "event_time": row.created_at,
                "author": to_text(row.user),
                "author_type": to_text(row.user_type),
                "body": to_text(row.body),
            }
        )

    # 2. 正式 PR Review
    reviews = pd.read_parquet(
        root / "pr_reviews.parquet",
        columns=[
            "id",
            "pr_id",
            "user",
            "user_type",
            "submitted_at",
            "body",
        ],
    )

    review_to_pr = {}

    for row in reviews.itertuples(index=False):
        review_id = int(row.id)
        pr_id = pd.to_numeric(row.pr_id, errors="coerce")

        if pd.isna(pr_id):
            continue

        review_to_pr[review_id] = int(pr_id)

        events.append(
            {
                "source": "pr_reviews",
                "event_id": review_id,
                "source_pr_id": int(pr_id),
                "event_time": row.submitted_at,
                "author": to_text(row.user),
                "author_type": to_text(row.user_type),
                "body": to_text(row.body),
            }
        )

    # 3. 代码行 Review 评论
    review_comments = pd.read_parquet(
        root / "pr_review_comments.parquet",
        columns=[
            "id",
            "pull_request_review_id",
            "user",
            "user_type",
            "created_at",
            "body",
            "pull_request_url",
        ],
    )

    for row in review_comments.itertuples(index=False):
        review_id = pd.to_numeric(
            row.pull_request_review_id,
            errors="coerce",
        )

        if pd.isna(review_id):
            continue

        review_id = int(review_id)

        if review_id not in review_to_pr:
            continue

        events.append(
            {
                "source": "pr_review_comments",
                "event_id": int(row.id),
                "source_pr_id": review_to_pr[review_id],
                "event_time": row.created_at,
                "author": to_text(row.user),
                "author_type": to_text(row.user_type),
                "body": to_text(row.body),
                "pull_request_url": to_text(row.pull_request_url),
            }
        )

    return events


def build_pairs(root: Path):
    prs = load_prs(root)

    by_id = {
        int(row.id): row
        for row in prs.itertuples(index=False)
    }

    by_repo_number = {
        (int(row.repo_id), int(row.number)): int(row.id)
        for row in prs.itertuples(index=False)
    }

    evidence = defaultdict(list)
    counts = defaultdict(int)

    for event in load_evidence(root):
        source_pr_id = event["source_pr_id"]

        if source_pr_id not in by_id:
            continue

        source_pr = by_id[source_pr_id]

        for target_number in extract_numbers(event["body"]):
            counts[f"{event['source']}_rule_mentions"] += 1

            target_id = by_repo_number.get(
                (
                    int(source_pr.repo_id),
                    target_number,
                )
            )

            if target_id is None:
                counts["unresolved_references"] += 1
                continue

            if target_id == source_pr_id:
                counts["self_references"] += 1
                continue

            target_pr = by_id[target_id]

            earlier, later = sorted(
                [source_pr, target_pr],
                key=lambda row: int(row.number),
            )

            pair_key = (
                int(earlier.id),
                int(later.id),
            )

            evidence[pair_key].append(event)

    pair_rows = []
    evidence_rows = []

    for (earlier_id, later_id), events in sorted(
        evidence.items()
    ):
        events.sort(
            key=lambda event: (
                pd.isna(event["event_time"]),
                event["event_time"],
                event["event_id"],
            )
        )

        earlier = by_id[earlier_id]
        later = by_id[later_id]

        pair_key = f"{earlier_id}_{later_id}"

        for event in events:
            evidence_pr = by_id[event["source_pr_id"]]

            if event["source"] == "pr_comments":
                evidence_url = (
                    f"{evidence_pr.html_url}"
                    f"#issuecomment-{event['event_id']}"
                )

            elif event["source"] == "pr_reviews":
                evidence_url = (
                    f"{evidence_pr.html_url}"
                    f"#pullrequestreview-{event['event_id']}"
                )

            else:
                evidence_url = (
                    f"{event.get('pull_request_url', evidence_pr.html_url)}"
                    f"#discussion_r{event['event_id']}"
                )

            evidence_rows.append(
                {
                    "pair_key": pair_key,
                    "evidence_source": event["source"],
                    "evidence_id": event["event_id"],
                    "evidence_pr_id": event["source_pr_id"],
                    "evidence_time": event["event_time"],
                    "evidence_url": evidence_url,
                    "evidence_author": event["author"],
                    "evidence_author_type": event["author_type"],
                    "evidence_body": event["body"],
                }
            )

        first = events[0]

        first_evidence_url = evidence_rows[-len(events)]["evidence_url"]

        pair_rows.append(
            {
                "key": pair_key,
                "repo": earlier.repo_full_name,
                "repo_id": int(earlier.repo_id),

                "earlier_id": earlier_id,
                "later_id": later_id,

                "earlier_number": int(earlier.number),
                "later_number": int(later.number),

                "earlier_title": earlier.title,
                "later_title": later.title,

                "earlier_url": earlier.html_url,
                "later_url": later.html_url,

                "earlier_user": earlier.user,
                "later_user": later.user,

                "earlier_agent": earlier.agent,
                "later_agent": later.agent,

                "earlier_created": earlier.created_at,
                "later_created": later.created_at,

                "first_relation_event": (
                    f"{first['source']}:{first['event_id']}"
                ),

                "first_relation_time": first["event_time"],

                "first_relation_url": first_evidence_url,

                "first_relation_actor_type": first["author_type"],

                "first_relation_actor_role": "evidence_author",

                "ordinary_evidence_comments": sum(
                    event["source"] == "pr_comments"
                    for event in events
                ),

                "all_source_evidence_comments": len(events),
            }
        )

    counts["resolved_references"] = sum(
        len(events)
        for events in evidence.values()
    )

    counts["unique_pairs"] = len(pair_rows)

    return (
        pd.DataFrame(pair_rows),
        pd.DataFrame(evidence_rows),
        dict(counts),
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--data-root",
        type=Path,
        default=Path("data/aidev-7.6m"),
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("results/reproduction_all_sources"),
    )

    args = parser.parse_args()

    args.output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    pairs, evidence, counts = build_pairs(
        args.data_root
    )

    pair_output = (
        args.output_dir
        / "candidate_duplicates_lookup.csv"
    )

    evidence_output = (
        args.output_dir
        / "evidence_lookup.csv"
    )

    pairs.to_csv(
        pair_output,
        index=False,
        encoding="utf-8-sig",
    )

    evidence.to_csv(
        evidence_output,
        index=False,
        encoding="utf-8-sig",
    )

    summary = {
        "method": (
            "rules.py applied to pr_comments, "
            "pr_reviews, and pr_review_comments"
        ),
        "pairs": len(pairs),
        "evidence_rows": len(evidence),
        "counts": counts,
        "filters": (
            "unresolved and self references only"
        ),
        "pair_output": str(pair_output),
        "evidence_output": str(evidence_output),
    }

    (args.output_dir / "summary.json").write_text(
        json.dumps(
            summary,
            indent=2,
            default=str,
        ),
        encoding="utf-8",
    )

    print(
        json.dumps(
            summary,
            indent=2,
            default=str,
        )
    )


if __name__ == "__main__":
    main()
