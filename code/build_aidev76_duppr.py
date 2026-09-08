"""Build an auditable MSR2018-style duplicate-PR review queue from AIDev v5."""
from __future__ import annotations
import argparse, csv, gc, json, re
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse
import fsspec
import pandas as pd
import pyarrow.parquet as pq

DATASET_ID = "hao-li/AIDev-7.6M"
REVISION = "37bbe1533e26cc1e1374917dba1186d1c8a4dc81"
DEFAULT_DATA_ROOT = "data/aidev-7.6m"
DEFAULT_RULES_PATH = Path("research/aidev76_duplicate_rules_msr2018_adapted_v1.json")
TABLE_COLUMNS = {
    "pull_request": ["id","number","title","body","agent","user_id","user","state","created_at","closed_at","merged_at","repo_id","repo_url","html_url"],
    "pr_comments": ["id","pr_id","user","user_id","user_type","created_at","body"],
    "pr_reviews": ["id","pr_id","pull_request_review_id","user","user_type","submitted_at","body"],
    "pr_review_comments": ["id","pull_request_review_id","user","user_type","created_at","body","pull_request_url"],
    "repository": ["id","full_name","stars","language","is_forked"],
}
FULL_URL = re.compile(r"(?i)https?://(?:api\.github\.com/repos/|github\.com/)([\w.\-]+/[\w.\-]+)/pulls?/(\d+)\b")
QUALIFIED = re.compile(r"(?<![\w/])([\w.\-]+/[\w.\-]+)#(\d+)\b")
BARE = re.compile(r"(?<![\w/])#(\d+)\b")
ANY_REF = re.compile(r"(?i)https?://(?:api\.github\.com/repos/|github\.com/)[\w.\-]+/[\w.\-]+/pulls?/\d+\b|(?<![\w/])[\w.\-]+/[\w.\-]+#\d+\b|(?<![\w/])#\d+\b")

def log(s: str) -> None: print(s, flush=True)
def source_path(root: str, name: str) -> str: return f"{root.rstrip('/\\')}/{name}.parquet"
def text_or_empty(v: Any) -> str:
    if v is None: return ""
    try:
        if pd.isna(v): return ""
    except (TypeError, ValueError): pass
    return str(v)
def norm_login(v: Any) -> str: return text_or_empty(v).strip().casefold()
def repository_key(v: Any) -> str:
    p = urlparse(text_or_empty(v).strip().rstrip("/"))
    host, path = (p.netloc or "").casefold(), p.path.strip("/")
    if path.startswith("repos/"): path = path[6:]
    parts = [x for x in path.split("/") if x]
    return "/".join(parts[:2]).casefold() if host in {"github.com","www.github.com","api.github.com"} and len(parts) >= 2 else ""
def parse_pr_numbers(text: str) -> set[int]:
    out = set()
    for m in ANY_REF.finditer(text_or_empty(text)):
        n = re.search(r"(\d+)\s*$", m.group(0))
        if n: out.add(int(n.group(1)))
    return out
def _normalise_refs(text: str) -> str:
    # Keep source offsets intact; the adapted rule expressions match qualified
    # owner/repo#number references directly.
    return text
def _ref_for_span(text: str, start: int, end: int) -> dict[str, str]:
    window_start, window = max(0, start-300), text[max(0, start-300):end]
    found = []
    for m in FULL_URL.finditer(window):
        if window_start + m.end(2) == end: found.append((m.start(), "url", m.group(1).casefold(), m.group(0)))
    for m in QUALIFIED.finditer(window):
        if window_start + m.end(2) == end: found.append((m.start(), "qualified", m.group(1).casefold(), m.group(0)))
    for m in BARE.finditer(window):
        if window_start + m.end(1) == end: found.append((m.start(), "local_hash", "", m.group(0)))
    if found:
        _, kind, repo, token = max(found, key=lambda x:x[0])
        return {"reference_kind": kind, "reference_repo": repo, "reference_token": token}
    return {"reference_kind":"unknown", "reference_repo":"", "reference_token":text[start:end]}

class Rule:
    def __init__(self, rule_id: str, expression: str): self.rule_id, self.pattern = rule_id, re.compile(expression)
def compile_rules(path: Path) -> tuple[str, list[Rule]]:
    cfg = json.loads(path.read_text(encoding="utf-8")); defs = cfg.get("rules")
    if not isinstance(defs, list) or len(defs) != 3: raise ValueError("exactly three MSR2018 rules are required")
    rules = [Rule(str(d["id"]), str(d["expression"])) for d in defs]
    if any(r.pattern.groups < 1 for r in rules): raise ValueError("each rule needs capture group 1")
    return str(cfg.get("rule_set", path.stem)), rules
def scan_rule_matches(text: str, rules: Iterable[Rule], source_repo_url: str = "") -> list[dict[str, Any]]:
    original, normalised, source_repo = text_or_empty(text), _normalise_refs(text_or_empty(text)), repository_key(source_repo_url)
    # Most discussion rows contain no PR marker or duplicate-language cue.
    # Avoid running the three backtracking expressions on those long bodies.
    if "#" not in original and "github.com/" not in original.lower():
        return []
    out = []
    # Bound regex work on unusually long generated comments while retaining
    # enough overlap to catch cues spanning a chunk boundary.
    spans = [(0, len(normalised))] if len(normalised) <= 20000 else [(s, min(len(normalised), s + 8000)) for s in range(0, len(normalised), 7500)]
    seen = set()
    for rule in rules:
        for ss, ee in spans:
          for m in rule.pattern.finditer(normalised[ss:ee]):
            ns, ne, number = ss + m.span(1)[0], ss + m.span(1)[1], int(m.group(1)); key=(rule.rule_id, ns, ne)
            if key in seen: continue
            seen.add(key); ref = _ref_for_span(original, ns, ne); rejection = ""
            if ref["reference_kind"] in {"url","qualified"}:
                if not source_repo: rejection = "source_repository_unknown_for_qualified_reference"
                elif ref["reference_repo"] != source_repo: rejection = "cross_repository_reference"
            out.append({"rule_id":rule.rule_id,"matched_text":original[ss+m.start():ss+m.end()],"reference_number":number,"match_start":ss+m.start(),"match_end":ss+m.end(),**ref,"source_repository":source_repo,"rejection_reason":rejection})
    return out
def indicative_pr_numbers(text: str, rules: Iterable[Rule]) -> set[int]: return {h["reference_number"] for h in scan_rule_matches(text, rules) if not h["rejection_reason"]}
def is_indicative(text: str, rules: Iterable[Rule]) -> bool: return bool(indicative_pr_numbers(text, rules))
def title_key(text: str) -> str:
    stop = {'a','an','and','as','at','by','for','from','in','into','is','it','of','on','or','the','to','with','fix','fixed','fixes','change','changes','update','updates'}
    return ' '.join(sorted(x for x in re.findall(r'[a-z][a-z0-9_-]{2,}', text_or_empty(text).lower()) if x not in stop))

def source_inventory(root: str, require_manifest: bool = True) -> dict[str, Any]:
    inv = {"dataset":DATASET_ID,"revision":REVISION,"data_root":root,"tables":{}}
    local = Path(root) if not root.startswith(("hf://","s3://","gs://")) else None
    if local:
        manifest = local / "download_manifest.json"
        if require_manifest and not manifest.exists(): raise FileNotFoundError(f"required source manifest missing: {manifest}")
        if manifest.exists():
            data = json.loads(manifest.read_text(encoding="utf-8"))
            if not data.get("all_verified", False): raise ValueError("source manifest is not verified")
            inv["manifest"] = str(manifest)
            by_path = {x.get("path"):x for x in data.get("files",[])}
        else: by_path = {}
    else: by_path = {}
    for name, cols in TABLE_COLUMNS.items():
        with fsspec.open(source_path(root,name), "rb") as fh:
            pf = pq.ParquetFile(fh); available = pf.schema_arrow.names; missing = sorted(set(cols)-set(available))
            inv["tables"][name] = {"rows":pf.metadata.num_rows,"columns":available,"missing_required_columns":missing}
            if missing: raise ValueError(f"{name} lacks required columns: {missing}")
        if local and name+".parquet" in by_path and local.joinpath(name+".parquet").stat().st_size != int(by_path[name+".parquet"]["bytes"]): raise ValueError(f"manifest byte mismatch for {name}")
    return inv
def load_table(root: str, name: str) -> pd.DataFrame: return pd.read_parquet(source_path(root,name), columns=TABLE_COLUMNS[name])

def build_discussion_table(prs: pd.DataFrame, root: str) -> tuple[pd.DataFrame, dict[str,int]]:
    reviews = load_table(root,"pr_reviews"); review_map = {int(r.id):int(r.pr_id) for r in reviews.itertuples(index=False)}
    review_map.update({int(r.pull_request_review_id):int(r.pr_id) for r in reviews.itertuples(index=False)})
    parts=[]
    general=load_table(root,"pr_comments").rename(columns={"id":"comment_id"}); general["comment_type"]="pr_comment"; general["evidence_id"]="pr_comment:"+general.comment_id.astype(str); general["mapping_source"]="direct_pr_id"; parts.append(general)
    rb=reviews.rename(columns={"id":"comment_id","submitted_at":"created_at"}).copy(); rb["comment_type"]="pr_review_body"; rb["evidence_id"]="pr_review:"+rb.comment_id.astype(str); rb["mapping_source"]="direct_review_pr_id"; parts.append(rb)
    inline=load_table(root,"pr_review_comments").rename(columns={"id":"comment_id"}); inline["pr_id"]=inline.pull_request_review_id.map(review_map); inline["comment_type"]="inline_review_comment"; inline["evidence_id"]="inline_review_comment:"+inline.comment_id.astype(str); inline["mapping_source"]="review_id"; inline["user_id"]=pd.NA
    url_repo=inline.pull_request_url.map(repository_key); url_num=inline.pull_request_url.map(lambda x: next((int(m.group(1)) for m in re.finditer(r"/pulls?/(\d+)\b",text_or_empty(x),re.I)),pd.NA))
    key_to_id={(repository_key(r.repo_url),int(r.number)):int(r.id) for r in prs.itertuples(index=False) if repository_key(r.repo_url)}
    url_ids=[key_to_id.get((repo,int(num))) if repo and pd.notna(num) else pd.NA for repo,num in zip(url_repo,url_num)]
    fallback=int(inline.pr_id.isna().sum()); inline.loc[inline.pr_id.isna(),"pr_id"]=pd.Series(url_ids,index=inline.index)[inline.pr_id.isna()]; unresolved=int(inline.pr_id.isna().sum()); inline=inline.dropna(subset=["pr_id"]); inline["pr_id"]=inline.pr_id.astype("int64"); parts.append(inline)
    cols=["evidence_id","comment_id","comment_type","pr_id","user","user_id","user_type","created_at","body","mapping_source"]
    norm=[]
    for p in parts:
        for c in cols:
            if c not in p: p[c]=pd.NA
        norm.append(p[cols])
    c=pd.concat(norm,ignore_index=True); c=c.merge(prs[["id","repo_id","repo_url","number"]],left_on="pr_id",right_on="id",how="inner").drop(columns=["id"]).rename(columns={"number":"source_pr_number"})
    c["created_at"]=pd.to_datetime(c.created_at,utc=True,errors="coerce"); c["body_text"]=c.body.map(text_or_empty); c["user_norm"]=c.user.map(norm_login)
    return c,{"unmapped_inline_review_comments":unresolved,"inline_review_id_fallbacks":fallback}

def scan_discussion(comments:pd.DataFrame,prs:pd.DataFrame,rules:list[Rule],matches_path:Path):
    repo_num=prs.set_index(["repo_id","number"])["id"].to_dict(); key_num={(repository_key(r.repo_url),int(r.number)):int(r.id) for r in prs.itertuples(index=False) if repository_key(r.repo_url)}; pairs=defaultdict(list); counts=defaultdict(int)
    match_fields=["evidence_id","comment_id","comment_type","source_pr_id","source_repo_id","source_repo","source_pr_number","evidence_created_at","evidence_user","rule_id","matched_text","reference_kind","reference_repo","reference_number","target_pr_id","resolved","rejection_reason"]
    with matches_path.open("w", newline="", encoding="utf-8") as match_file:
      writer=csv.DictWriter(match_file,fieldnames=match_fields); writer.writeheader()
      for idx, row in enumerate(comments.itertuples(index=False), start=1):
        if idx % 100000 == 0: log(f"scanning discussion evidence: {idx:,}/{len(comments):,}")
        source_repo=repository_key(row.repo_url)
        for hit in scan_rule_matches(row.body_text,rules,row.repo_url):
            if hit["reference_kind"] in {"url","qualified"}:
                target=key_num.get((source_repo,hit["reference_number"])) if not hit["rejection_reason"] else None
            else: target=repo_num.get((int(row.repo_id),hit["reference_number"]))
            reason=hit["rejection_reason"]
            if target is None and not reason: reason="target_pr_missing_or_issue"
            if target is not None and int(target)==int(row.pr_id): reason="self_reference"
            resolved=target is not None and not reason
            if resolved:
                pairs[tuple(sorted((int(row.pr_id),int(target))))].append((str(row.evidence_id),str(row.comment_type),int(row.pr_id),int(target),row.created_at,hit["rule_id"],hit["matched_text"][:240])); counts["resolved_rule_hits"]+=1
            else: counts["rejected_rule_hits"]+=1
            writer.writerow({"evidence_id":str(row.evidence_id),"comment_id":int(row.comment_id),"comment_type":str(row.comment_type),"source_pr_id":int(row.pr_id),"source_repo_id":int(row.repo_id),"source_repo":source_repo,"source_pr_number":int(row.source_pr_number),"evidence_created_at":row.created_at,"evidence_user":text_or_empty(row.user),"rule_id":hit["rule_id"],"matched_text":hit["matched_text"][:240],"reference_kind":hit["reference_kind"],"reference_repo":hit["reference_repo"],"reference_number":int(hit["reference_number"]),"target_pr_id":target,"resolved":resolved,"rejection_reason":reason})
    return pairs,dict(counts)

def candidate_rows(prs,pairs):
    by=prs.set_index("id",drop=False); rows=[]
    for (x,y),hits in sorted(pairs.items()):
        a,b=by.loc[x],by.loc[y]; ca,cb=a.created_at,b.created_at
        if pd.notna(ca) and pd.notna(cb) and ca<cb: earlier,later,order=x,y,"a_before_b"
        elif pd.notna(ca) and pd.notna(cb) and cb<ca: earlier,later,order=y,x,"b_before_a"
        else: earlier=later=pd.NA; order="tie_or_missing"
        hs=sorted(hits,key=lambda h:(pd.isna(h[4]),h[4] if pd.notna(h[4]) else pd.Timestamp.max,h[0])); first=hs[0]
        rows.append({"pair_id":f"{x}_{y}","pr_id_a":x,"pr_id_b":y,"repo_id":int(a.repo_id),"pr_number_a":int(a.number),"pr_number_b":int(b.number),"title_a":text_or_empty(a.title),"title_b":text_or_empty(b.title),"author_a":text_or_empty(a.user),"author_b":text_or_empty(b.user),"author_user_id_a":a.user_id,"author_user_id_b":b.user_id,"agent_a":text_or_empty(a.agent),"agent_b":text_or_empty(b.agent),"html_url_a":text_or_empty(a.html_url),"html_url_b":text_or_empty(b.html_url),"created_at_a":ca,"created_at_b":cb,"earlier_pr_id":earlier,"later_pr_id":later,"temporal_order":order,"evidence_count":len(hs),"evidence_ids":";".join(h[0] for h in hs),"evidence_rule_ids":";".join(h[5] for h in hs),"evidence_types":";".join(sorted({h[1] for h in hs})),"first_indicator_evidence_id":first[0],"first_indicator_rule_id":first[5],"first_indicator_at":first[4],"candidate_detection_latency_hours":((first[4]-by.loc[int(later)].created_at).total_seconds()/3600 if pd.notna(later) and pd.notna(first[4]) and pd.notna(by.loc[int(later)].created_at) and first[4]>=by.loc[int(later)].created_at else pd.NA),"same_author":pd.NA,"same_author_basis":pd.NA,"prior_comment_awareness":pd.NA,"snapshot_reference_flag":pd.NA,"prefilter_exclusion_reason":"","duplicate_label":pd.NA,"rater_1_label":pd.NA,"rater_2_label":pd.NA,"adjudicated_label":pd.NA,"adjudicated_master_pr_id":pd.NA,"adjudicated_duplicate_pr_id":pd.NA,"adjudication_rationale":pd.NA})
    return pd.DataFrame(rows)

def _snapshot_targets(text,row,nums,key):
    src=repository_key(row.repo_url); out=set()
    for m in ANY_REF.finditer(text_or_empty(text)):
        tok=m.group(0); nm=re.search(r"(\d+)\s*$",tok)
        if not nm: continue
        n=int(nm.group(1)); fu=FULL_URL.fullmatch(tok); qu=QUALIFIED.fullmatch(tok)
        if fu or qu:
            repo=(fu.group(1) if fu else qu.group(1)).casefold(); target=key.get((repo,n)) if repo==src else None
        else: target=nums.get((int(row.repo_id),n))
        if target is not None: out.add(int(target))
    return out
def _awareness_maps(comments):
    first_id={}; first_login={}
    for r in comments.dropna(subset=["created_at"]).itertuples(index=False):
        if pd.notna(r.user_id): first_id[(int(r.pr_id),int(r.user_id))]=min(first_id.get((int(r.pr_id),int(r.user_id)),r.created_at),r.created_at)
        login=norm_login(r.user)
        if login: first_login[(int(r.pr_id),login)]=min(first_login.get((int(r.pr_id),login),r.created_at),r.created_at)
    return first_id,first_login

def apply_prefilter(candidates,prs,comments):
    first_id,first_login=_awareness_maps(comments)
    return apply_prefilter_maps(candidates,prs,first_id,first_login)

def apply_prefilter_maps(candidates,prs,first_id,first_login):
    if candidates.empty: return candidates.copy(),candidates.copy(),candidates.copy()
    by=prs.set_index("id",drop=False)
    # Build the PR reference maps once.  Rebuilding these 361k-row dictionaries
    # inside the candidate loop causes runaway memory/time on the full dataset.
    nums=prs.set_index(["repo_id","number"])["id"].to_dict()
    key={(repository_key(r.repo_url),int(r.number)):int(r.id) for r in prs.itertuples(index=False) if repository_key(r.repo_url)}
    same=[]; basis=[]; prior=[]; snap=[]
    for r in candidates.itertuples(index=False):
        a,b=by.loc[int(r.pr_id_a)],by.loc[int(r.pr_id_b)]; eq=False; why=""
        if pd.notna(a.user_id) and pd.notna(b.user_id) and int(a.user_id)==int(b.user_id): eq=True; why="user_id"
        elif norm_login(a.user) and norm_login(a.user)==norm_login(b.user): eq=True; why="normalized_login"
        same.append(eq); basis.append(why)
        if pd.isna(r.later_pr_id): prior.append(False); snap.append(False); continue
        early,later=by.loc[int(r.earlier_pr_id)],by.loc[int(r.later_pr_id)]; pt=first_id.get((int(early.id),int(later.user_id))) if pd.notna(later.user_id) else None
        if pt is None: pt=first_login.get((int(early.id),norm_login(later.user)))
        prior.append(bool(pt is not None and pd.notna(later.created_at) and pt<later.created_at)); snap.append(int(early.id) in _snapshot_targets(f"{later.title}\n{later.body}",later,nums,key))
    out=candidates.copy(); out["same_author"]=same; out["same_author_basis"]=basis; out["prior_comment_awareness"]=prior; out["snapshot_reference_flag"]=snap; out["prefilter_exclusion_reason"]= [";".join(x for x,y in [("same_author",s),("prior_comment_awareness",p),("snapshot_reference_flag",z)] if y) for s,p,z in zip(same,prior,snap)]
    excluded=out[out.prefilter_exclusion_reason!=""].reset_index(drop=True); compatible=out[out.prefilter_exclusion_reason==""].reset_index(drop=True)
    return out.reset_index(drop=True),excluded,compatible
def annotation_template(candidates): return candidates.copy()
def write_seed_sample(comments,prs,out_dir,count,per_repo,seed):
    nums=prs.set_index(["repo_id","number"])["id"].to_dict(); key={(repository_key(r.repo_url),int(r.number)):int(r.id) for r in prs.itertuples(index=False) if repository_key(r.repo_url)}; rows=[]
    for r in comments.itertuples(index=False):
        if "#" not in r.body_text and "github.com/" not in r.body_text.lower():
            continue
        targets=set(); src_repo=repository_key(r.repo_url)
        for m in ANY_REF.finditer(r.body_text):
            tok=m.group(0); nm=re.search(r"(\d+)\s*$",tok)
            if not nm: continue
            n=int(nm.group(1)); fu=FULL_URL.fullmatch(tok); qu=QUALIFIED.fullmatch(tok)
            if fu or qu:
                ref_repo=(fu.group(1) if fu else qu.group(1)).casefold()
                target=key.get((ref_repo,n)) if ref_repo==src_repo else None
            else: target=nums.get((int(r.repo_id),n))
            if target is not None and int(target)!=int(r.pr_id): targets.add(n)
        targets=sorted(targets)
        
        if targets: rows.append({"comment_key":r.evidence_id,"comment_id":r.comment_id,"comment_type":r.comment_type,"repo_id":r.repo_id,"pr_id":r.pr_id,"source_pr_number":r.source_pr_number,"created_at":r.created_at,"referenced_pr_numbers":";".join(map(str,targets)),"comment_body":r.body_text})
    s=pd.DataFrame(rows); selected=pd.DataFrame()
    if not s.empty:
        stats=s.groupby("repo_id").agg(eligible_source_pr_count=("pr_id","nunique"),eligible_comment_count=("comment_id","size")).reset_index(); selected=stats.sort_values(["eligible_source_pr_count","eligible_comment_count","repo_id"],ascending=[False,False,True]).head(count); parts=[g.sample(n=min(per_repo,len(g)),random_state=seed+int(k)) for k,g in s[s.repo_id.isin(set(selected.repo_id))].groupby("repo_id",sort=False)]; s=pd.concat(parts,ignore_index=True) if parts else s.head(0); selected=selected.merge(s.groupby("repo_id").size().rename("sample_count"),on="repo_id",how="left").fillna(0)
    selected.to_csv(out_dir/"seed_repositories.csv",index=False)
    for c in ["adjudicated_indicative","rater_1_indicative","rater_1_notes","rater_2_indicative","rater_2_notes"]: s[c]=pd.NA
    s.to_csv(out_dir/"seed_indicative_comment_sample.csv",index=False); return s
def build(args):
    out=Path(args.output_dir); out.mkdir(parents=True,exist_ok=True); inv=source_inventory(args.data_root,not args.allow_unmanifested); (out/"source_inventory.json").write_text(json.dumps(inv,indent=2,default=str),encoding="utf-8")
    if args.source_check: print(json.dumps(inv,indent=2,default=str)); return inv
    rule_set,rules=compile_rules(Path(args.rules_path)); log("loading pull requests"); prs=load_table(args.data_root,"pull_request");
    for c in ["created_at","closed_at","merged_at"]: prs[c]=pd.to_datetime(prs[c],utc=True,errors="coerce")
    prs["title"]=prs.title.map(text_or_empty); prs["body"]=prs.body.map(text_or_empty); log("loading discussions"); comments,diag=build_discussion_table(prs,args.data_root); input_discussion_rows=len(comments); seed=write_seed_sample(comments,prs,out,args.seed_repository_count,args.seed_sample_per_repository,args.random_seed); log(f"seed rows: {len(seed):,}"); first_id,first_login=_awareness_maps(comments); pairs,scan=scan_discussion(comments,prs,rules,out/"rule_matches.csv"); del comments; gc.collect(); cand=candidate_rows(prs,pairs); del pairs; gc.collect(); ledger,excluded,compat=apply_prefilter_maps(cand,prs,first_id,first_login); del cand,first_id,first_login; gc.collect(); main=ledger[(~ledger.same_author.astype(bool)) & (~ledger.prior_comment_awareness.astype(bool))].reset_index(drop=True)
    ledger.to_csv(out/"duplicate_candidate_ledger.csv",index=False); main.to_csv(out/"duplicate_candidates.csv",index=False); excluded.to_csv(out/"duplicate_prefilter_excluded.csv",index=False); compat.to_csv(out/"duplicate_msr_compatible_candidates.csv",index=False); annotation_template(main).to_csv(out/"duplicate_annotations_template.csv",index=False)
    # Explicit int64 avoids the 32-bit `int` alias on Windows corrupting GitHub
    # PR IDs above 2^31 when exporting candidate evidence packets.
    ids=set(ledger.pr_id_a.astype("int64")).union(set(ledger.pr_id_b.astype("int64"))) if not ledger.empty else set(); pp=prs[prs.id.isin(ids)].copy(); log("reloading discussions for candidate packet"); packet_comments,_=build_discussion_table(prs,args.data_root); cp=packet_comments[packet_comments.pr_id.isin(ids)].copy(); del packet_comments; gc.collect(); pp.to_parquet(out/"candidate_pr_packet.parquet",index=False); cp.to_parquet(out/"candidate_comment_packet.parquet",index=False); pp.to_csv(out/"candidate_pr_packet.csv",index=False); cp.to_csv(out/"candidate_comment_packet.csv",index=False)
    summary={"dataset":DATASET_ID,"revision":REVISION,"input_prs":len(prs),"input_discussion_rows":input_discussion_rows,"seed_sample_rows":len(seed),"candidate_pairs_all":len(ledger),"retained_candidate_pairs":len(main),"prefilter_excluded_pairs":len(excluded),"msr_compatible_pairs":len(compat),"rule_set":rule_set,"rule_matches":int(scan.get("resolved_rule_hits",0)+scan.get("rejected_rule_hits",0)),**diag,**scan,"interpretation":"Candidates and evidence only; no duplicate label inferred."}; (out/"candidate_summary.json").write_text(json.dumps(summary,indent=2,default=str),encoding="utf-8"); print(json.dumps(summary,indent=2,default=str)); return summary
def parse_args():
    p=argparse.ArgumentParser(); p.add_argument("--data-root",default=DEFAULT_DATA_ROOT); p.add_argument("--output-dir",default="results/aidev76_duppr"); p.add_argument("--rules-path",default=str(DEFAULT_RULES_PATH)); p.add_argument("--source-check",action="store_true"); p.add_argument("--allow-unmanifested",action="store_true"); p.add_argument("--seed-repository-count",type=int,default=26); p.add_argument("--seed-sample-per-repository",type=int,default=200); p.add_argument("--random-seed",type=int,default=20260908); return p.parse_args()
if __name__ == "__main__": build(parse_args())
