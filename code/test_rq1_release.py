"""Read-only integrity tests for the published RQ1 candidate/annotation package.

Run from the release root with ``python code/test_rq1_release.py``.
The tests do not rebuild data and deliberately ignore legacy, unsharded
``comment_evidence.parquet`` files.
"""
from __future__ import annotations

import unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
REVIEW_COLUMNS = [
    "pair_id", "layer", "pr_url_a", "pr_url_b", "evidence_page",
    "same_intent", "different_accounts", "prior_awareness",
    "discussion_consensus", "label", "master_pr_id", "duplicate_pr_id",
    "evidence_notes", "reviewer_id", "reviewed_at_utc",
]
TEMPLATE_NAMES = ("reviewer_1.csv", "reviewer_2.csv", "adjudication.csv")
class HTMLReviewParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if attr.get("id"):
            self.ids.add(str(attr["id"]))
        if tag == "a" and attr.get("href"):
            self.hrefs.append(str(attr["href"]))


def read_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path, dtype=str, keep_default_na=False)


def id_set(values: pd.Series) -> set[str]:
    return set(values.astype(str))


def required_evidence(candidates: pd.DataFrame) -> set[str]:
    return {
        evidence_id
        for entry in candidates["evidence_ids"]
        for evidence_id in entry.split(";")
        if evidence_id
    }


class RQ1ReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.candidates = {
            layer: read_csv(ROOT / f"{layer.lower()}_layer" / "candidates.csv")
            for layer in ("A", "B")
        }
        cls.a_strict = read_csv(ROOT / "a_layer" / "strict_candidates.csv")
        cls.b_all = read_csv(ROOT / "b_layer" / "all_candidates.csv")
        cls.templates = {
            layer: {
                name: read_csv(ROOT / f"{layer.lower()}_layer" / name)
                for name in TEMPLATE_NAMES
            }
            for layer in ("A", "B")
        }
        cls.review_parsers = {}
        for layer in ("A", "B"):
            review = ROOT / f"{layer.lower()}_layer" / "review.html"
            parser = HTMLReviewParser()
            parser.feed(review.read_text(encoding="utf-8"))
            cls.review_parsers[layer] = parser

    def test_candidate_counts_and_unique_pairs(self) -> None:
        expected = ((self.candidates["A"], 124), (self.a_strict, 87),
                    (self.candidates["B"], 1500), (self.b_all, 7297))
        for frame, count in expected:
            with self.subTest(count=count):
                self.assertEqual(len(frame), count)
                self.assertEqual(frame["pair_id"].nunique(), count)

    def test_strict_a_is_subset_and_layers_are_disjoint(self) -> None:
        a_pairs = id_set(self.candidates["A"]["pair_id"])
        self.assertTrue(id_set(self.a_strict["pair_id"]).issubset(a_pairs))
        self.assertFalse(a_pairs & id_set(self.b_all["pair_id"]))
        self.assertFalse(a_pairs & id_set(self.candidates["B"]["pair_id"]))

    def test_b_priority_is_first_1500_of_full_pool(self) -> None:
        pd.testing.assert_frame_equal(
            self.candidates["B"].reset_index(drop=True),
            self.b_all.head(1500).reset_index(drop=True),
        )

    def test_annotation_templates_align_and_are_unfilled(self) -> None:
        for layer, candidates in self.candidates.items():
            reference = self.templates[layer]["reviewer_1.csv"]
            for name, frame in self.templates[layer].items():
                with self.subTest(layer=layer, template=name):
                    self.assertEqual(list(frame.columns), REVIEW_COLUMNS)
                    self.assertEqual(len(frame), len(candidates))
                    self.assertEqual(frame["pair_id"].tolist(), candidates["pair_id"].tolist())
                    self.assertEqual(frame["layer"].tolist(), [layer] * len(frame))
                    self.assertEqual(frame["pr_url_a"].tolist(), candidates["html_url_a"].tolist())
                    self.assertEqual(frame["pr_url_b"].tolist(), candidates["html_url_b"].tolist())
                    expected_pages = [f"review.html#pair-{pair_id}" for pair_id in candidates["pair_id"]]
                    self.assertEqual(frame["evidence_page"].tolist(), expected_pages)
                    self.assertEqual(reference["evidence_page"].tolist(), expected_pages)
                    self.assertTrue(frame["evidence_page"].str.len().gt(0).all())
                    for column in REVIEW_COLUMNS[5:]:
                        self.assertTrue(frame[column].eq("").all(), f"Nonempty {column}")

    def test_pr_evidence_exactly_covers_selected_candidates(self) -> None:
        for layer, candidates in self.candidates.items():
            with self.subTest(layer=layer):
                prs = pd.read_parquet(ROOT / f"{layer.lower()}_layer" / "pr_evidence.parquet")
                needed = id_set(candidates["pr_id_a"]) | id_set(candidates["pr_id_b"])
                self.assertEqual(id_set(prs["id"]), needed)
                self.assertFalse(prs["id"].duplicated().any())

    def test_sharded_comment_evidence_coverage_and_uniqueness(self) -> None:
        for layer, candidates in self.candidates.items():
            with self.subTest(layer=layer):
                layer_dir = ROOT / f"{layer.lower()}_layer"
                shards = sorted(layer_dir.glob("comment_evidence_[0-9][0-9].parquet"))
                self.assertTrue(shards, "Missing sharded comment evidence")
                comments = pd.concat(
                    [pd.read_parquet(path, columns=["evidence_id", "pr_id"]) for path in shards],
                    ignore_index=True,
                )
                self.assertFalse(comments["evidence_id"].duplicated().any())
                self.assertFalse(comments["evidence_id"].isna().any())
                self.assertTrue(required_evidence(candidates).issubset(id_set(comments["evidence_id"])))
                needed_prs = id_set(candidates["pr_id_a"]) | id_set(candidates["pr_id_b"])
                self.assertTrue(id_set(comments["pr_id"]).issubset(needed_prs))

    def _assert_pair_link(self, link: str, source: Path) -> str:
        parsed = urlsplit(link)
        self.assertFalse(parsed.scheme, link)
        allowed_paths = ("", "review.html") if source.name == "review.html" else ("review.html",)
        self.assertIn(unquote(parsed.path), allowed_paths, link)
        target = source.parent / "review.html"
        target = target.resolve()
        self.assertTrue(target.is_relative_to(ROOT), link)
        self.assertTrue(target.is_file(), link)
        anchor = unquote(parsed.fragment)
        self.assertTrue(anchor.startswith("pair-"), link)
        parser = self.review_parsers[source.parent.name[0].upper()]
        self.assertIn(anchor, parser.ids, link)
        return anchor.removeprefix("pair-")

    def test_all_generated_pair_links_and_page_anchors_exist(self) -> None:
        for layer, candidates in self.candidates.items():
            layer_dir = ROOT / f"{layer.lower()}_layer"
            expected_pairs = id_set(candidates["pair_id"])
            with self.subTest(layer=layer):
                for name, frame in self.templates[layer].items():
                    for row in frame.itertuples(index=False):
                        self.assertEqual(self._assert_pair_link(row.evidence_page, layer_dir / name), row.pair_id)
                review = layer_dir / "review.html"
                self.assertTrue(review.is_file())
                parser = self.review_parsers[layer]
                html_pairs = {anchor.removeprefix("pair-") for anchor in parser.ids if anchor.startswith("pair-")}
                self.assertEqual(html_pairs, expected_pairs)
                self.assertEqual(len(html_pairs), len(expected_pairs))
                for href in parser.hrefs:
                    if "#pair-" in href:
                        self._assert_pair_link(href, review)

    def test_each_comment_shard_is_under_24_mb(self) -> None:
        for layer in ("A", "B"):
            paths = sorted((ROOT / f"{layer.lower()}_layer").glob("comment_evidence_[0-9][0-9].parquet"))
            self.assertTrue(paths)
            for path in paths:
                with self.subTest(path=path.name, layer=layer):
                    self.assertLess(path.stat().st_size, 24_000_000)


if __name__ == "__main__":
    unittest.main(verbosity=2)
