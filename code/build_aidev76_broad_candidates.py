"""Build a high-recall, same-repository PR-reference candidate queue.

This is intentionally separate from the MSR2018-style high-precision output.
It uses every resolvable same-repository PR reference in discussion evidence
(general comments, review bodies, and inline review comments), keeps all
evidence and diagnostic flags, and never infers a duplicate label.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_aidev76_duppr as base


def main() -> dict:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-root", default=base.DEFAULT_DATA_ROOT)
    ap.add_argument("--output-dir", default="results/aidev76_broad")
    ap.add_argument("--rule-matches-path", type=Path, default=None,
                    help="CSV emitted by the strict MSR2018 pass; used only to rank explicit cues.")
    ap.add_argument("--exclude-pairs-path", type=Path, default=Path("results/aidev76_duppr/duplicate_candidates.csv"),
                    help="A-layer candidate CSV; those pairs are excluded from B.")
    ap.add_argument("--max-candidates", type=int, default=1200,
                    help="Maximum number of high-recall candidates to export; use 0 for all.")
    args = ap.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    prs = base.load_table(args.data_root, "pull_request")
    for c in ["created_at", "closed_at", "merged_at"]:
        prs[c] = pd.to_datetime(prs[c], utc=True, errors="coerce")
    prs["title"] = prs.title.map(base.text_or_empty)
    prs["body"] = prs.body.map(base.text_or_empty)
    comments, diag = base.build_discussion_table(prs, args.data_root)

    local_num = prs.set_index(["repo_id", "number"])["id"].to_dict()
    repo_num = {
        (base.repository_key(r.repo_url), int(r.number)): int(r.id)
        for r in prs.itertuples(index=False)
        if base.repository_key(r.repo_url)
    }
    by_id = prs.set_index("id", drop=False)
    excluded_pairs = set()
    if args.exclude_pairs_path.exists():
        excluded_pairs = set(pd.read_csv(args.exclude_pairs_path, usecols=["pair_id"]).pair_id.astype(str))
    evidence = []
    grouped = defaultdict(list)

    for r in comments.itertuples(index=False):
        source_repo = base.repository_key(r.repo_url)
        for m in base.ANY_REF.finditer(r.body_text):
            token = m.group(0)
            number_match = base.re.search(r"(\d+)\s*$", token)
            if not number_match:
                continue
            number = int(number_match.group(1))
            fu = base.FULL_URL.fullmatch(token)
            qu = base.QUALIFIED.fullmatch(token)
            if fu or qu:
                ref_repo = (fu.group(1) if fu else qu.group(1)).casefold()
                target = repo_num.get((ref_repo, number)) if ref_repo == source_repo else None
                reference_kind = "url" if fu else "qualified"
                rejection = "cross_repository_or_unknown" if target is None else ""
            else:
                target = local_num.get((int(r.repo_id), number))
                reference_kind = "local_hash"
                rejection = "target_pr_missing_or_issue" if target is None else ""
            if target is None or int(target) == int(r.pr_id):
                continue
            pair = tuple(sorted((int(r.pr_id), int(target))))
            rec = {
                "pair_id": f"{pair[0]}_{pair[1]}",
                "pr_id_source": int(r.pr_id),
                "pr_id_target": int(target),
                "repo_id": int(r.repo_id),
                "evidence_id": str(r.evidence_id),
                "comment_id": int(r.comment_id),
                "comment_type": str(r.comment_type),
                "evidence_created_at": r.created_at,
                "evidence_user": base.text_or_empty(r.user),
                "reference_kind": reference_kind,
                "reference_number": number,
                "reference_token": token,
                "matched_text": r.body_text[max(0, m.start() - 120): min(len(r.body_text), m.end() + 120)],
                "rejection_reason": rejection,
            }
            evidence.append(rec)
            grouped[pair].append(rec)

    evidence_df = pd.DataFrame(evidence)
    if evidence_df.empty:
        evidence_df = pd.DataFrame(columns=["pair_id"])
    evidence_df.to_csv(out / "broad_reference_evidence.csv", index=False)

    # Existing rule matches provide the exact high-precision MSR cue signal.
    rule_keys = set()
    rule_path = args.rule_matches_path or Path("results/aidev76_duppr/rule_matches.csv")
    if rule_path.exists():
        rm = pd.read_csv(rule_path, usecols=["evidence_id", "target_pr_id", "resolved", "rule_id"])
        for x in rm[rm.resolved.astype(bool)].itertuples(index=False):
            rule_keys.add((str(x.evidence_id), int(x.target_pr_id), str(x.rule_id)))

    first_id, first_login = base._awareness_maps(comments)
    rows = []
    for pair, hits in sorted(grouped.items()):
        x, y = pair
        a, b = by_id.loc[x], by_id.loc[y]
        if pd.notna(a.created_at) and pd.notna(b.created_at) and a.created_at < b.created_at:
            early, later = x, y
        elif pd.notna(a.created_at) and pd.notna(b.created_at) and b.created_at < a.created_at:
            early, later = y, x
        else:
            early = later = pd.NA
        early_row = by_id.loc[int(early)] if pd.notna(early) else None
        later_row = by_id.loc[int(later)] if pd.notna(later) else None
        same = ((pd.notna(a.user_id) and pd.notna(b.user_id) and int(a.user_id) == int(b.user_id)) or
                (base.norm_login(a.user) and base.norm_login(a.user) == base.norm_login(b.user)))
        prior = False
        if later_row is not None and early_row is not None:
            t = first_id.get((int(early_row.id), int(later_row.user_id))) if pd.notna(later_row.user_id) else None
            if t is None:
                t = first_login.get((int(early_row.id), base.norm_login(later_row.user)))
            prior = bool(t is not None and pd.notna(later_row.created_at) and t < later_row.created_at)
        explicit = [h for h in hits if any((h["evidence_id"], int(h["pr_id_target"]), rid) in rule_keys for rid in ["MSR2018-R1", "MSR2018-R2", "MSR2018-R3"])]
        types = sorted({h["comment_type"] for h in hits})
        if explicit:
            tier = "A_explicit_duplicate_cue"
        elif len(hits) >= 2 or len(types) >= 2:
            tier = "B_repeated_or_cross_evidence_reference"
        else:
            tier = "C_single_same_repository_reference"
        title_key_a, title_key_b = base.title_key(a.title), base.title_key(b.title)
        same_title_key = bool(title_key_a and title_key_a == title_key_b)
        snapshot_flag = False
        if early_row is not None and later_row is not None:
            snapshot_flag = int(early_row.id) in base._snapshot_targets(f"{later_row.title}\n{later_row.body}", later_row, local_num, repo_num)
        rank_score = (100 if explicit else 0) + (20 if len(hits) >= 2 else 0) + (10 if len(types) >= 2 else 0) + (8 if not same else 0) + (5 if not prior else 0) + (4 if same_title_key else 0)
        rows.append({
            "pair_id": f"{x}_{y}", "pr_id_a": x, "pr_id_b": y, "repo_id": int(a.repo_id),
            "pr_number_a": int(a.number), "pr_number_b": int(b.number),
            "title_a": a.title, "title_b": b.title, "author_a": base.text_or_empty(a.user),
            "author_b": base.text_or_empty(b.user), "author_user_id_a": a.user_id, "author_user_id_b": b.user_id,
            "html_url_a": base.text_or_empty(a.html_url), "html_url_b": base.text_or_empty(b.html_url),
            "created_at_a": a.created_at, "created_at_b": b.created_at,
            "earlier_pr_id": early, "later_pr_id": later, "temporal_order": "ordered" if pd.notna(early) else "tie_or_missing",
            "evidence_count": len(hits), "evidence_ids": ";".join(sorted({h["evidence_id"] for h in hits})),
            "evidence_types": ";".join(types), "reference_kinds": ";".join(sorted({h["reference_kind"] for h in hits})),
            "explicit_msr_cue_evidence_count": len(explicit), "tier": tier,
            "same_author": bool(same), "prior_comment_awareness": bool(prior),
            "snapshot_reference_flag": bool(snapshot_flag),
            "same_title_key": same_title_key, "retrieval_score": rank_score,
            "review_label": pd.NA, "rater_1_label": pd.NA, "rater_2_label": pd.NA,
            "adjudicated_label": pd.NA, "adjudication_rationale": pd.NA,
        })
    all_candidates = pd.DataFrame(rows)
    if not all_candidates.empty and excluded_pairs:
        all_candidates = all_candidates[~all_candidates.pair_id.astype(str).isin(excluded_pairs)].copy()
    all_candidates = all_candidates.sort_values(
        ["retrieval_score", "evidence_count", "pair_id"], ascending=[False, False, True], kind="stable"
    ).reset_index(drop=True)
    all_candidates.insert(0, "retrieval_rank", range(1, len(all_candidates) + 1))
    selected = all_candidates if args.max_candidates == 0 else all_candidates.head(args.max_candidates).copy()
    all_candidates.to_csv(out / "broad_reference_candidates_all.csv", index=False)
    selected.to_csv(out / "broad_reference_candidates.csv", index=False)
    if not selected.empty:
        packet_ids = set(selected.pr_id_a.astype("int64")).union(set(selected.pr_id_b.astype("int64")))
        selected_prs = prs[prs.id.isin(packet_ids)].copy()
        selected_comments = comments[comments.pr_id.isin(packet_ids)].copy()
        selected_prs.to_parquet(out / "broad_candidate_pr_packet.parquet", index=False)
        selected_comments.to_parquet(out / "broad_candidate_comment_packet.parquet", index=False)
        selected_prs.to_csv(out / "broad_candidate_pr_packet.csv", index=False)
        selected_comments.to_csv(out / "broad_candidate_comment_packet.csv", index=False)
    counts = selected["tier"].value_counts().to_dict() if not selected.empty else {}
    summary = {"input_prs": len(prs), "input_discussion_rows": len(comments), "resolved_same_repository_mentions": len(evidence_df), "excluded_a_pairs": len(excluded_pairs), "candidate_pairs_all_b": len(all_candidates), "candidate_pairs_exported": len(selected), "tier_counts_exported": counts, "max_candidates": args.max_candidates, "rule_matches_path": str(rule_path) if rule_path.exists() else None, **diag, "interpretation": "B-layer high-recall references for manual review; A-layer pairs excluded; no duplicate label inferred"}
    (out / "broad_reference_summary.json").write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
    print(json.dumps(summary, indent=2, default=str))
    return summary


if __name__ == "__main__":
    main()
