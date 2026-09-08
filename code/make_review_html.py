"""Create one searchable offline review page for each RQ1 layer."""
from __future__ import annotations

import argparse
import html
from pathlib import Path

import pandas as pd


def esc(value) -> str:
    if pd.isna(value):
        return ""
    return html.escape(str(value))


def build(layer_dir: Path, candidates_name: str, comments_name: str, out_name: str) -> None:
    candidates = pd.read_csv(layer_dir / candidates_name)
    comment_paths = sorted(layer_dir.glob("comment_evidence_*.parquet"))
    comments = pd.concat((pd.read_parquet(path) for path in comment_paths), ignore_index=True)
    evidence = comments.drop_duplicates("evidence_id").set_index("evidence_id")
    blocks = []
    for _, row in candidates.iterrows():
        pair_id = esc(row.pair_id)
        flags = f"same account={int(row.same_author)}; prior comment={int(row.prior_comment_awareness)}; snapshot reference={int(row.snapshot_reference_flag)}"
        body = [f'<article id="pair-{pair_id}"><h2>Pair {pair_id}</h2>',
                f'<p><a href="{esc(row.html_url_a)}">PR #{esc(row.pr_number_a)}</a> — {esc(row.title_a)}<br>'
                f'<a href="{esc(row.html_url_b)}">PR #{esc(row.pr_number_b)}</a> — {esc(row.title_b)}</p>',
                f'<p>Authors: {esc(row.author_a)} / {esc(row.author_b)}<br>{esc(flags)}</p>']
        for eid in dict.fromkeys(str(row.evidence_ids).split(";")):
            e = evidence.loc[eid]
            text = str(e.body)
            body.append(f'<details><summary>Evidence {esc(eid)} · {esc(e.comment_type)} · {esc(e.created_at)}</summary>'
                        f'<p>Source PR {esc(e.pr_id)}; commenter {esc(e.user)}</p>'
                        f'<pre>{html.escape(text[:4000])}</pre>'
                        + (f'<p><em>Excerpt only; full text is in the Parquet shards.</em></p>' if len(text) > 4000 else '')
                        + '</details>')
        body.append('<p class="review">Fill the matching row in reviewer_1.csv / reviewer_2.csv.</p></article>')
        blocks.append("\n".join(body))
    layer = layer_dir.name
    page = f'''<!doctype html><meta charset="utf-8"><title>{layer} RQ1 review</title>
<style>body{{font:14px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;background:#fafafa}}article{{background:white;border:1px solid #ddd;border-radius:8px;padding:1rem;margin:1rem 0}}pre{{white-space:pre-wrap;max-height:18rem;overflow:auto;background:#f3f3f3;padding:.7rem}}details{{margin:.7rem 0}}.review{{color:#555}}</style>
<h1>{layer} 层 RQ1 人工核查</h1><p>这是候选线索，不是确认结果。用浏览器 Ctrl+F 搜索 pair ID；两位同学分别填写 CSV。完整评论在本层 comment_evidence_*.parquet。</p>
{''.join(blocks)}'''
    (layer_dir / out_name).write_text(page, encoding="utf-8")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=Path("."))
    args = p.parse_args()
    build(args.root / "a_layer", "candidates.csv", "comment_evidence_01.parquet", "review.html")
    build(args.root / "b_layer", "candidates.csv", "comment_evidence_01.parquet", "review.html")


if __name__ == "__main__":
    main()
