"""RQ1 descriptive analysis for the 899 candidate PR pairs.

Run from this directory:
    python rq1_analysis.py

The script prints the main RQ1 statistics and writes compact CSV summaries.
"""
from pathlib import Path
import sys
import pandas as pd

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).resolve().parent
DF = pd.read_csv(HERE / "rq1_dataset.csv")
DF["same_account"] = DF["same_account"].astype(str).str.lower().eq("true")
DF["title_exact"] = DF["earlier_title"].fillna("").str.strip().str.lower().eq(DF["later_title"].fillna("").str.strip().str.lower())
DF["title_jaccard"] = DF["title_jaccard"].astype(float)
DF["body_jaccard"] = DF["body_jaccard"].astype(float)

# Reusable group labels for the comparisons used in RQ1.
DF["account_group"] = DF["same_account"].map({True: "same_account", False: "different_account"})
DF[["account_group", "gap_hours", "title_exact", "code_bucket", "outcome_pair"]].to_csv(
    HERE / "rq1_pair_features.csv", index=False
)

print("RQ1: Basic characteristics of 899 candidate PR pairs")
print("=" * 55)
print(f"Candidate pairs: {len(DF)}")
print(f"Distinct PRs: {len(set(DF['earlier_id']) | set(DF['later_id']))}")
print(f"Repositories: {DF['repo'].nunique()}")
print(f"Same account: {DF['same_account'].sum()} ({DF['same_account'].mean():.1%})")
print(f"Different accounts: {(~DF['same_account']).sum()} ({(~DF['same_account']).mean():.1%})")

print("\nTop repositories")
print(DF["repo"].value_counts().head(10).to_string())

print("\nCreation-time gap")
for group, d in DF.groupby("account_group"):
    print(f"  {group}: median={d.gap_hours.median():.2f} hours; mean={d.gap_hours.mean():.2f} hours")

print("\nText similarity")
for group, d in DF.groupby("account_group"):
    print(f"  {group}: exact titles={d.title_exact.sum()}; median title similarity={d.title_jaccard.median():.2f}; median body similarity={d.body_jaccard.median():.2f}")

print("\nAI-agent appearances")
print(pd.concat([DF["earlier_agent"], DF["later_agent"]]).value_counts().to_string())

print("\nCode-evidence categories")
print(pd.crosstab(DF["code_bucket"], DF["account_group"]).to_string())

print("\nOutcomes")
print(DF["outcome_pair"].value_counts().to_string())

print("\nSubmission-group sizes")
chains = DF.groupby("component_id").apply(lambda x: len(set(x["earlier_id"]) | set(x["later_id"])), include_groups=False)
print(f"  2 PRs: {(chains == 2).sum()}")
print(f"  3 PRs: {(chains == 3).sum()}")
print(f"  4+ PRs: {(chains >= 4).sum()}")

summary = pd.DataFrame([
    {"group": g, "pairs": len(d), "median_gap_hours": d.gap_hours.median(), "mean_gap_hours": d.gap_hours.mean(),
     "exact_title_pairs": int(d.title_exact.sum()),
     "exact_patch_pairs": int((d.code_bucket == "exact_normalized_text_patch").sum()),
     "high_overlap_pairs": int((d.code_bucket == "high_bidirectional_overlap").sum())}
    for g, d in DF.groupby("account_group")
])
summary.to_csv(HERE / "rq1_group_summary.csv", index=False)
DF["repo"].value_counts().rename_axis("repository").reset_index(name="candidate_pairs").to_csv(HERE / "rq1_repository_summary.csv", index=False)
pd.concat([DF["earlier_agent"], DF["later_agent"]]).value_counts().rename_axis("agent").reset_index(name="pr_appearances").to_csv(HERE / "rq1_agent_summary.csv", index=False)
DF["outcome_pair"].value_counts().rename_axis("outcome_pair").reset_index(name="pairs").to_csv(HERE / "rq1_outcome_summary.csv", index=False)
chains.rename("pr_count").value_counts().sort_index().rename_axis("prs_in_group").reset_index(name="groups").to_csv(HERE / "rq1_chain_summary.csv", index=False)
