"""生成可离线双击打开的中文 RQ1 候选核查页。"""
from __future__ import annotations

import argparse
import html
from pathlib import Path
from urllib.parse import urlsplit

import pandas as pd


def esc(value) -> str:
    """Escape every value so candidate text is never interpreted as markup."""
    if pd.isna(value):
        return ""
    return html.escape(str(value), quote=True)


def text(value) -> str:
    return "" if pd.isna(value) else str(value)


def github_url(value: object) -> str:
    url = text(value).strip()
    # Candidate input is expected to contain GitHub PR URLs.  Never emit a
    # non-GitHub URL into an href; show it as escaped text if the source is bad.
    try:
        parsed = urlsplit(url)
        if (parsed.scheme == "https" and parsed.netloc == "github.com"
                and not any(ord(char) < 32 for char in url) and "\\" not in url):
            return url
    except ValueError:
        pass
    return ""


def yes_no(value: object) -> str:
    normalized = text(value).strip().lower()
    if normalized in {"true", "yes", "1"}:
        return "有"
    if normalized in {"false", "no", "0"}:
        return "无"
    return "待核对"


def evidence_type(value: object) -> str:
    return {
        "pr_comment": "PR 评论",
        "pr_review_body": "审查正文",
        "inline_review_comment": "行内审查评论",
        "review": "审查正文",
        "review_comment": "行内审查评论",
    }.get(text(value), text(value) or "未知类型")


def href_or_text(url: object, label: str) -> str:
    safe_url = github_url(url)
    return f'<a href="{esc(safe_url)}" target="_blank" rel="noopener">{esc(label)}</a>' if safe_url else esc(label)


def build(layer_dir: Path, candidates_name: str = "candidates.csv", comments_name: str = "comment_evidence_01.parquet", out_name: str = "review.html") -> None:
    """Build one page in ``layer_dir``; kept dependency-light for offline use."""
    candidates = pd.read_csv(layer_dir / candidates_name, dtype=str, keep_default_na=False)
    candidates["same_author"] = candidates["same_author"].map(yes_no)
    candidates["prior_comment_awareness"] = candidates["prior_comment_awareness"].map(yes_no)
    candidates["snapshot_reference_flag"] = candidates["snapshot_reference_flag"].map(yes_no)
    comment_paths = sorted(layer_dir.glob("comment_evidence_[0-9][0-9].parquet"))
    if not comment_paths:
        raise FileNotFoundError(f"No sharded comment evidence found in {layer_dir}")
    comments = pd.concat((pd.read_parquet(path) for path in comment_paths), ignore_index=True)
    evidence = comments.drop_duplicates("evidence_id").set_index("evidence_id")
    layer_code = "A" if layer_dir.name.lower().startswith("a_") else "B"
    layer_note = (
        "A 层按论文中的重复表达规则筛选；严格子集已包含在本层，不应重复计数。"
        if layer_code == "A" else
        "B 层放宽关键词收集同仓库 PR 引用，已排除 A 层；本页是排序后的优先核查队列，不是随机样本。"
    )
    blocks: list[str] = []
    for _, row in candidates.iterrows():
        pair_id = text(row.pair_id)
        anchor = f"pair-{pair_id}"
        a_url, b_url = github_url(row.html_url_a), github_url(row.html_url_b)
        a_link = href_or_text(a_url, f"PR #{text(row.pr_number_a)}")
        b_link = href_or_text(b_url, f"PR #{text(row.pr_number_b)}")
        body: list[str] = [
            f'<article id="{esc(anchor)}">',
            f'<h2>{esc(pair_id)}</h2>',
            '<div class="pr-grid">',
            '<section class="pr-card"><h3>PR A（左侧记录）</h3>'
            f'<p><strong>标题：</strong>{esc(row.title_a)}</p>'
            f'<p><strong>仓库：</strong>{esc("/".join(a_url.split("/")[3:5]))}<br>'
            f'<strong>链接：</strong>{a_link}<br><strong>作者：</strong>{esc(row.author_a)}<br>'
            f'<strong>创建时间（UTC）：</strong>{esc(row.created_at_a)}</p></section>',
            '<section class="pr-card"><h3>PR B（右侧记录）</h3>'
            f'<p><strong>标题：</strong>{esc(row.title_b)}</p>'
            f'<p><strong>仓库：</strong>{esc("/".join(b_url.split("/")[3:5]))}<br>'
            f'<strong>链接：</strong>{b_link}<br><strong>作者：</strong>{esc(row.author_b)}<br>'
            f'<strong>创建时间（UTC）：</strong>{esc(row.created_at_b)}</p></section>',
            '</div>',
            '<p class="flags"><strong>风险标记：</strong>'
            f'同账号：{esc(row.same_author)}；提交前评论：{esc(row.prior_comment_awareness)}；'
            f'快照引用：{esc(row.snapshot_reference_flag)}。无标记不等于已证明“不知情”，仍需人工核对。</p>',
        ]
        for eid in dict.fromkeys(text(row.evidence_ids).split(";")):
            if not eid:
                continue
            if eid not in evidence.index:
                raise ValueError(f"Missing evidence {eid} for pair {pair_id}")
            e = evidence.loc[eid]
            body_text = text(e.body)
            excerpt = body_text[:4000]
            full_note = "；全文请在本层 comment_evidence_*.parquet 分片中按 evidence_id 查询。" if len(body_text) > 4000 else ""
            body.append(
                '<details open class="evidence"><summary>'
                f'证据 {esc(eid)} · {esc(evidence_type(e.comment_type))} · {esc(e.created_at)}</summary>'
                f'<p><strong>评论者：</strong>{esc(e.user)}　<strong>来源 PR ID：</strong>{esc(e.pr_id)}　'
                f'<strong>类型：</strong>{esc(evidence_type(e.comment_type))}</p>'
                f'<pre>{esc(excerpt)}</pre>'
                f'<p class="note">{esc("这是前 4,000 字符摘录" if len(body_text) > 4000 else "这是完整评论")}{esc(full_note)}</p>'
                '</details>'
            )
        body.append('<p class="todo">请在对应的 reviewer_1.csv / reviewer_2.csv 中填写这对 PR 的判断。</p></article>')
        blocks.append("\n".join(body))
    title = f"{layer_code} 层 RQ1 候选人工核查"
    page = f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<style>
body{{font:15px system-ui,-apple-system,"Microsoft YaHei",sans-serif;max-width:1180px;margin:2rem auto;padding:0 1rem;background:#f6f7f9;color:#202124;line-height:1.55}}
header,article{{background:#fff;border:1px solid #d9dce1;border-radius:10px;padding:1rem 1.2rem;margin:1rem 0;box-shadow:0 1px 2px #0000000d}}
h1{{margin-top:0}} h2{{border-bottom:1px solid #eee;padding-bottom:.35rem}} h3{{margin:.2rem 0 .5rem;color:#374151}}
.pr-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}} .pr-card{{border:1px solid #e2e5ea;border-radius:8px;padding:.7rem}}
.flags{{background:#fff8e1;border-left:4px solid #e0a800;padding:.6rem}} details{{margin:.8rem 0;border:1px solid #e2e5ea;border-radius:7px;padding:.5rem .7rem}} summary{{cursor:pointer;font-weight:600}}
pre{{white-space:pre-wrap;overflow:auto;background:#f1f3f5;padding:.8rem;border-radius:5px;max-height:22rem}} .note,.todo{{color:#5f6368}} a{{color:#0759a5}}
@media(max-width:760px){{.pr-grid{{grid-template-columns:1fr}}}}
</style></head><body>
<header><h1>{esc(title)}</h1><p>本页展示的是候选线索，不是人工确认结论。共有 <strong>{len(candidates):,}</strong> 对 PR；一块代表一对 PR。{esc(layer_note)}</p><p>请用浏览器 Ctrl+F 搜索 pair_id。先对比两份 PR 是否想做同一修改，再查账号是否不同、后提交者是否知情，以及讨论是否明确认定重复；两位同学分别填 reviewer_1.csv / reviewer_2.csv，最终在 adjudication.csv 裁决。</p><p>左右顺序不代表提交先后，请查看创建时间。GitHub 链接打开的是当前网页，可能不同于截至 2026-03-31 的数据快照；证据默认展开，全文在本层评论 Parquet 分片中。所有原文均按纯文本显示。</p></header>
{''.join(blocks)}
</body></html>'''
    (layer_dir / out_name).write_text(page, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="生成 A/B 层离线中文人工核查页")
    parser.add_argument("--root", type=Path, default=Path("."), help="包含 a_layer 和 b_layer 的发布目录")
    args = parser.parse_args()
    build(args.root / "a_layer")
    build(args.root / "b_layer")


if __name__ == "__main__":
    main()
