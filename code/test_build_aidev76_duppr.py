import json
from pathlib import Path
import sys
import tempfile
import unittest

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_aidev76_duppr as duppr


class AIDev76DupPRTests(unittest.TestCase):
    def test_parse_pr_numbers_accepts_hash_and_url(self):
        text = "Duplicate of #42; closed by https://github.com/a/b/pull/71."
        self.assertEqual(duppr.parse_pr_numbers(text), {42, 71})

    def test_title_normalisation_ignores_order_and_action_words(self):
        self.assertEqual(
            duppr.title_key("Fix the parser timeout"),
            duppr.title_key("Parser timeout fix"),
        )

    def test_initial_rules_match_duplicate_and_not_association(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        self.assertTrue(duppr.is_indicative("This is a duplicate of #123.", rules))
        self.assertFalse(duppr.is_indicative("Related to #123; please check CI.", rules))

    def test_rules_extract_only_the_linked_duplicate_pr(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        self.assertEqual(duppr.indicative_pr_numbers("Duplicate: #123, not #456.", rules), {123})

    def test_rule_config_is_versioned_json(self):
        config = json.loads(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json").read_text(encoding="utf-8"))
        self.assertEqual(config["rule_set"], "aidev76_duplicate_rules_msr2018_adapted_v1")
        self.assertGreater(len(config["rules"]), 0)

    def test_full_url_reference_is_rejected_for_foreign_repository(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        hits = duppr.scan_rule_matches(
            "Duplicate of https://github.com/other/project/pull/123",
            rules,
            "https://github.com/example/project",
        )
        self.assertTrue(hits)
        self.assertTrue(all(h["rejection_reason"] == "cross_repository_reference" for h in hits))

    def test_qualified_reference_preserves_repository_identity(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        hits = duppr.scan_rule_matches(
            "Duplicate of example/project#123",
            rules,
            "https://github.com/example/project",
        )
        self.assertTrue(hits)
        self.assertEqual(hits[0]["reference_kind"], "qualified")
        self.assertEqual(hits[0]["reference_repo"], "example/project")
        self.assertEqual(hits[0]["rejection_reason"], "")

    def test_unrelated_reference_is_not_indicative(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        self.assertFalse(duppr.is_indicative("Related to #123; see the discussion.", rules))

    def test_long_body_keeps_rule_match_offsets(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        prefix = "x" * 5000
        hits = duppr.scan_rule_matches(prefix + " Duplicate of #123", rules)
        self.assertTrue(hits)
        self.assertGreater(hits[0]["match_start"], 5000)
        self.assertEqual(hits[0]["reference_number"], 123)

    def test_foreign_qualified_r2_reference_is_rejected(self):
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        hits = duppr.scan_rule_matches(
            "other/repo#7 duplicate implementation",
            rules,
            "https://github.com/local/repo",
        )
        self.assertTrue(hits)
        self.assertTrue(any(h["rule_id"] == "MSR2018-R2" for h in hits))
        self.assertTrue(all(h["rejection_reason"] == "cross_repository_reference" for h in hits))

    def test_synthetic_discussion_mapping_preserves_large_ids_and_foreign_seed_ref(self):
        """Exercise the AIDev-pop joins without downloading the source tables."""
        root = Path(tempfile.mkdtemp(prefix="aidev_duppr_test_"))
        repo_url = "https://github.com/acme/project"
        ids = [3_000_000_001, 3_000_000_002, 3_000_000_003]
        prs = pd.DataFrame([
            {"id": ids[0], "number": 1, "title": "base", "body": "", "agent": "A", "user_id": 101, "user": "alice", "state": "open", "created_at": "2026-01-01T00:00:00Z", "closed_at": None, "merged_at": None, "repo_id": 7, "repo_url": repo_url, "html_url": repo_url + "/pull/1"},
            {"id": ids[1], "number": 2, "title": "dup", "body": "", "agent": "B", "user_id": 102, "user": "bob", "state": "closed", "created_at": "2026-01-02T00:00:00Z", "closed_at": None, "merged_at": None, "repo_id": 7, "repo_url": repo_url, "html_url": repo_url + "/pull/2"},
            {"id": ids[2], "number": 3, "title": "foreign", "body": "", "agent": "C", "user_id": 103, "user": "carol", "state": "closed", "created_at": "2026-01-03T00:00:00Z", "closed_at": None, "merged_at": None, "repo_id": 7, "repo_url": repo_url, "html_url": repo_url + "/pull/3"},
        ])
        prs.to_parquet(root / "pull_request.parquet", index=False)
        pd.DataFrame([
            {"id": 3_100_000_001, "pr_id": ids[1], "user": "bob", "user_id": 102, "user_type": "User", "created_at": "2026-01-02T01:00:00Z", "body": "Duplicate of #1"},
            {"id": 3_100_000_002, "pr_id": ids[2], "user": "carol", "user_id": 103, "user_type": "User", "created_at": "2026-01-03T01:00:00Z", "body": "Duplicate of https://github.com/foreign/project/pull/1"},
        ]).to_parquet(root / "pr_comments.parquet", index=False)
        pd.DataFrame([{"id": 4_100_000_001, "pr_id": ids[0], "pull_request_review_id": 4_100_000_001, "user": "reviewer", "user_type": "User", "submitted_at": "2026-01-01T02:00:00Z", "body": "Duplicate of #2"}]).to_parquet(root / "pr_reviews.parquet", index=False)
        pd.DataFrame([{"id": 4_200_000_001, "pull_request_review_id": 4_100_000_001, "user": "reviewer", "user_type": "User", "created_at": "2026-01-01T03:00:00Z", "body": "Duplicate of #2", "pull_request_url": repo_url + "/pull/1"}]).to_parquet(root / "pr_review_comments.parquet", index=False)
        pd.DataFrame([{"id": 7, "full_name": "acme/project", "stars": 101, "language": "Python", "is_forked": False}]).to_parquet(root / "repository.parquet", index=False)
        discussion, diag = duppr.build_discussion_table(prs, str(root))
        self.assertEqual(len(discussion), 4)
        self.assertEqual(int(discussion.loc[discussion.comment_type == "inline_review_comment", "pr_id"].iloc[0]), ids[0])
        self.assertEqual(discussion.loc[discussion.comment_type == "inline_review_comment", "pr_id"].dtype, "int64")
        _, rules = duppr.compile_rules(Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json"))
        match_path = root / "matches.csv"
        pairs, _ = duppr.scan_discussion(discussion, prs, rules, match_path)
        self.assertIn((ids[0], ids[1]), pairs)
        self.assertNotIn((ids[0], ids[2]), pairs)
        seed = duppr.write_seed_sample(discussion, prs, root, 1, 20, 1)
        self.assertNotIn(3_100_000_002, set(seed.comment_id.astype("int64")))

    def test_synthetic_candidate_export_has_blank_labels(self):
        prs = pd.DataFrame([
            {"id": 3_000_000_001, "number": 1, "title": "base", "body": "", "agent": "A", "user_id": 101, "user": "alice", "created_at": pd.Timestamp("2026-01-01", tz="UTC"), "repo_id": 7, "repo_url": "https://github.com/acme/project", "html_url": "https://github.com/acme/project/pull/1"},
            {"id": 3_000_000_002, "number": 2, "title": "dup", "body": "", "agent": "B", "user_id": 102, "user": "bob", "created_at": pd.Timestamp("2026-01-02", tz="UTC"), "repo_id": 7, "repo_url": "https://github.com/acme/project", "html_url": "https://github.com/acme/project/pull/2"},
        ])
        pairs = {(3_000_000_001, 3_000_000_002): [("e1", "pr_comment", 3_000_000_002, 3_000_000_001, pd.Timestamp("2026-01-02 01:00", tz="UTC"), "MSR2018-R3", "Duplicate of #1")]}
        candidates = duppr.candidate_rows(prs, pairs)
        self.assertEqual(candidates.iloc[0]["temporal_order"], "a_before_b")
        self.assertTrue(pd.isna(candidates.iloc[0]["duplicate_label"]))
        self.assertEqual(candidates.iloc[0]["pair_id"], "3000000001_3000000002")


if __name__ == "__main__":
    unittest.main()
