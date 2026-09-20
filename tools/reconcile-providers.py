#!/usr/bin/env python3
"""
reconcile-providers.py - merge per-repo provider lists into one union table.

Reads any number of providers-*.csv files produced by mine-providers.py and
writes:

  providers-union.csv   one row per provider, with which repos mention it,
                        the union of evidence and the strongest confidence.

Categories with no model/relay counterpart (infra:proxy, infra:cdn, ...) are
kept but flagged, so a reader ranking "AI providers" can filter them out.

Usage:
  python3 reconcile-providers.py --out DIR providers-sub2api.csv providers-cliproxyapi.csv
"""

import argparse
import csv
import os
from collections import defaultdict

ORDER = {"high": 3, "medium": 2, "low": 1}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csvs", nargs="+")
    ap.add_argument("--out", default=".")
    args = ap.parse_args()

    merged = {}
    for path in args.csvs:
        with open(path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                p = row["provider"]
                m = merged.setdefault(p, {
                    "provider": p,
                    "display_name": row["display_name"],
                    "kind": row["kind"],
                    "repos": set(),
                    "methods": set(),
                    "confidence": "low",
                    "evidence_count": 0,
                    "first_evidence": row["first_evidence"],
                })
                m["repos"].add(row["repo"])
                m["methods"].update(row["methods"].split("|"))
                if ORDER[row["confidence"]] > ORDER[m["confidence"]]:
                    m["confidence"] = row["confidence"]
                    m["display_name"] = row["display_name"]
                    m["kind"] = row["kind"]
                m["evidence_count"] += int(row["evidence_count"])

    rows = []
    for m in merged.values():
        m = dict(m)
        m["repos"] = "|".join(sorted(m["repos"]))
        m["methods"] = "|".join(sorted(x for x in m["methods"] if x))
        m["in_both"] = "yes" if "|" in m["repos"] else "no"
        rows.append(m)
    rows.sort(key=lambda r: (r["kind"], r["provider"]))

    fields = ["provider", "display_name", "kind", "repos", "in_both",
              "confidence", "methods", "evidence_count", "first_evidence"]
    out = os.path.join(args.out, "providers-union.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    kinds = defaultdict(int)
    for r in rows:
        kinds[r["kind"]] += 1
    print(f"union: {len(rows)} providers -> {out}")
    for k in sorted(kinds):
        print(f"   {k:24} {kinds[k]}")
    both = [r["provider"] for r in rows if r["in_both"] == "yes"]
    print(f"   in both repos: {len(both)}")


if __name__ == "__main__":
    main()
