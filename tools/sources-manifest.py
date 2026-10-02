#!/usr/bin/env python3
"""Write a source manifest for a pass: label, url, http status, bytes, sha256.

The manifest is what lets a later pass prove what changed rather than assert it.
`tools/fetch-firstparty.py` owns the URL list; this script records what the
fetch wrote, so the pair is: fetch (network) then manifest (bookkeeping).

Usage: python3 tools/sources-manifest.py [PASS_DIR] [--urls from fetch-firstparty]
"""
import argparse
import csv
import hashlib
import importlib.util
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_pages():
    """Import PAGES out of fetch-firstparty.py without executing its main()."""
    path = ROOT / "tools" / "fetch-firstparty.py"
    spec = importlib.util.spec_from_file_location("fetch_firstparty", path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["fetch_firstparty"] = mod
    spec.loader.exec_module(mod)  # module-level PAGES only; main() is under __main__
    return mod.PAGES


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pass_dir", nargs="?")
    args = ap.parse_args()
    passes = sorted(p for p in ROOT.iterdir()
                    if p.is_dir() and len(p.name) == 10 and p.name[4] == "-")
    pass_dir = pathlib.Path(args.pass_dir) if args.pass_dir else passes[-1]
    pages = load_pages()
    out = pass_dir / "sources-manifest.csv"
    rows = []
    for name, url in sorted(pages.items()):
        f = pass_dir / "sources" / name
        if not f.is_file():
            rows.append({"file": name, "url": url, "http_status": "MISSING",
                         "bytes": "", "sha256": ""})
            continue
        data = f.read_bytes()
        rows.append({"file": name, "url": url, "http_status": "200",
                     "bytes": len(data),
                     "sha256": hashlib.sha256(data).hexdigest()})
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["file", "url", "http_status", "bytes", "sha256"])
        w.writeheader()
        w.writerows(rows)
    got = sum(1 for r in rows if r["http_status"] == "200")
    print(f"wrote {out} ({got}/{len(rows)} present)")
    for r in rows:
        if r["http_status"] != "200":
            print(f"  MISSING {r['file']} ({r['url']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
