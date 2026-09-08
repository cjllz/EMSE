"""Download and verify the population files used by the AIDev DupPR pipeline.

The script is intentionally scoped to the seven files already selected for the
v5 AIDev-pop population: six parquet files plus ``README.md``.
It queries the pinned Hugging Face tree, skips files whose local LFS hash and
size already match, downloads only missing or corrupt files, and writes a
machine-readable integrity manifest.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests


DATASET = "hao-li/AIDev-7.6M"
REVISION = "37bbe1533e26cc1e1374917dba1186d1c8a4dc81"
FILES = (
    "pull_request.parquet",
    "pr_comments.parquet",
    "pr_reviews.parquet",
    "pr_review_comments.parquet",
    "related_issue.parquet",
    "repository.parquet",
    "README.md",
)
TREE_URL = (
    "https://huggingface.co/api/datasets/{dataset}/tree/{revision}"
    "?recursive=true&expand=false"
)
RESOLVE_URL = (
    "https://huggingface.co/datasets/{dataset}/resolve/{revision}/{path}"
    "?download=true"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_tree(session: requests.Session) -> dict[str, dict[str, Any]]:
    response = session.get(
        TREE_URL.format(dataset=DATASET, revision=REVISION), timeout=60
    )
    response.raise_for_status()
    entries = {item["path"]: item for item in response.json() if item.get("type") == "file"}
    missing = [name for name in FILES if name not in entries]
    if missing:
        raise RuntimeError(f"Pinned dataset tree is missing expected files: {missing}")
    return {name: entries[name] for name in FILES}


def download_one(session: requests.Session, path: Path, name: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    url = RESOLVE_URL.format(dataset=DATASET, revision=REVISION, path=name)
    with session.get(url, stream=True, timeout=(30, 300)) as response:
        response.raise_for_status()
        temporary = path.with_suffix(path.suffix + ".part")
        with temporary.open("wb") as handle:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    handle.write(chunk)
        temporary.replace(path)


def parquet_info(path: Path) -> tuple[int | None, list[str] | None]:
    if path.suffix != ".parquet":
        return None, None
    try:
        import pyarrow.parquet as parquet

        metadata = parquet.ParquetFile(path).metadata
        schema = parquet.ParquetFile(path).schema_arrow
        return metadata.num_rows, list(schema.names)
    except Exception as exc:  # pragma: no cover - diagnostic path
        raise RuntimeError(f"Could not inspect parquet file {path}: {exc}") from exc


def local_record(path: Path, remote: dict[str, Any]) -> dict[str, Any]:
    size = path.stat().st_size
    actual_sha = sha256_file(path)
    rows, columns = parquet_info(path)
    lfs = remote.get("lfs") or {}
    expected_sha = lfs.get("oid")
    expected_size = lfs.get("size", remote.get("size"))
    return {
        "path": remote["path"],
        "exists": path.exists(),
        "bytes": size,
        "expected_bytes": expected_size,
        "sha256": actual_sha,
        "expected_sha256": expected_sha,
        "git_oid": remote.get("oid"),
        "xet_hash": remote.get("xetHash"),
        "verified": (expected_size == size and (expected_sha is None or expected_sha == actual_sha)),
        "rows": rows,
        "columns": columns,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "aidev-7.6m",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="Manifest path (default: <data-dir>/download_manifest.json)",
    )
    parser.add_argument("--verify-only", action="store_true", help="Do not download missing files")
    args = parser.parse_args(argv)
    data_dir = args.data_dir.resolve()
    manifest_path = (args.manifest or data_dir / "download_manifest.json").resolve()
    data_dir.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"User-Agent": "AIDev-DupPR-pop-downloader/1.0"})
    tree = fetch_tree(session)
    records: list[dict[str, Any]] = []
    failures: list[str] = []
    for name in FILES:
        target = data_dir / name
        remote = tree[name]
        expected_size = (remote.get("lfs") or {}).get("size", remote.get("size"))
        expected_sha = (remote.get("lfs") or {}).get("oid")
        if target.exists():
            current_size = target.stat().st_size
            current_sha = sha256_file(target)
            valid = current_size == expected_size and (expected_sha is None or current_sha == expected_sha)
        else:
            valid = False
        if not valid and not args.verify_only:
            download_one(session, target, name)
        if not target.exists():
            failures.append(f"missing: {name}")
            continue
        record = local_record(target, remote)
        records.append(record)
        if not record["verified"]:
            failures.append(f"verification failed: {name}")

    manifest = {
        "dataset": DATASET,
        "revision": REVISION,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "files": records,
        "all_verified": not failures and len(records) == len(FILES),
        "failures": failures,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))
    return 0 if manifest["all_verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
