#!/usr/bin/env python3
"""Parse the Artificial Analysis model list out of a saved models-page snapshot.

The AA page ships its chart data inline (Next.js flight payload) plus a manifest
pointing at a brotli-compressed dataset that this network cannot decompress. The
inline payload is enough for the fields this repo publishes: the top-list chart
gives Intelligence Index, release date and weighted cost per Intelligence Index
task for the head of the field, and each per-model object carries
contextWindowTokens, isOpenWeights, cacheHitPrice, cacheWritePrice and the
benchmark sub-scores.

Usage: python3 tools/parse-aa.py <snapshot.html> [--json OUT]
"""
import argparse
import json
import pathlib
import re
import sys

# chart series entries look like: {"id":"...","label":"...","color":"#x","logo":"/img/...","url":"/models/x","pattern":"...","value":N}
CHART_ENTRY = re.compile(
    r'"label":"([^"]+)","color":"[^"]*","logo":"[^"]*","url":"(/models/[^"]+)","pattern":"[^"]*","value":([\d.]+)'
)
MODEL_OBJ = re.compile(r'"slug":"([a-z0-9.\-]+)","name":"([^"]*)"')


def unescape(html: str) -> str:
    """The flight payload is JSON-in-JS-string; undo one round of escaping."""
    return html.replace('\\\\"', '"').replace('\\"', '"')


def top_list(text: str, upto: int) -> dict:
    """The primary Intelligence Index chart, keyed by model url."""
    out = {}
    for label, url, value in CHART_ENTRY.findall(text):
        out.setdefault(url, {"label": label, "ii": float(value)})
    return out


def per_model(text: str) -> dict:
    """Fields the per-model objects carry, keyed by slug."""
    out = {}
    for m in MODEL_OBJ.finditer(text):
        slug = m.group(1)
        if slug in out:
            continue
        seg = text[m.end():m.end() + 3500]

        def g(key):
            mm = re.search(rf'"{key}":("?)(-?[\d.]+|null|true|false|[^",}}]+)\1', seg)
            return mm.group(2) if mm else None

        out[slug] = {
            "slug": slug,
            "short_name": g("shortName"),
            "release_date": g("releaseDate"),
            "context_window_tokens": g("contextWindowTokens"),
            "is_open_weights": g("isOpenWeights"),
            "intelligence_index": g("intelligenceIndex"),
            "cache_hit_price": g("cacheHitPrice"),
            "cache_write_price": g("cacheWritePrice"),
            "terminal_bench_science": g("terminalBenchScience"),
            "scicode": g("scicode"),
            "hle": g("hle"),
            "mmmu_pro": g("mmmuPro"),
            "deprecated": g("deprecated"),
        }
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshot")
    ap.add_argument("--json", dest="out")
    args = ap.parse_args()
    raw = pathlib.Path(args.snapshot).read_text(encoding="utf-8", errors="ignore")
    text = unescape(raw)
    fields = {"top_list": top_list(text, 0), "models": per_model(text)}
    if args.out:
        pathlib.Path(args.out).write_text(json.dumps(fields, indent=1))
    print(f"{len(fields['models'])} model objects, {len(fields['top_list'])} top-list entries")
    for url, d in sorted(fields["top_list"].items(), key=lambda x: -x[1]["ii"]):
        print(f"{d['ii']:7.2f}  {d['label']:42s} {url}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
