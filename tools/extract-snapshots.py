#!/usr/bin/env python3
"""Turn the raw HTML snapshots into text extracts + structured configs.

Question this answers: what is the smallest faithful artifact that lets a later
session re-check a price or a public setting without re-fetching, and without
republishing a vendor's whole minified page?

For each sources/sites/*.html and sources/pricing/*.html:
  * writes a whitespace-collapsed visible-text .txt beside it (script/style
    stripped), which is what a citation quotes;
  * for sites, extracts window.__APP_CONFIG__ to sources/configs/<name>.json.
The .html files are then deleted by the caller (this script does not delete).

Usage: python3 tools/extract-snapshots.py [PASS_DIR]
"""
import html as htmllib
import json
import re
import sys
from pathlib import Path

TAG = re.compile(r"<[^>]+>")


def visible_text(raw: str) -> str:
    t = re.sub(r"<script.*?</script>", " ", raw, flags=re.S | re.I)
    t = re.sub(r"<style.*?</style>", " ", t, flags=re.S | re.I)
    t = TAG.sub(" ", t)
    return re.sub(r"\s+", " ", htmllib.unescape(t)).strip()


def app_config(raw: str):
    m = re.search(r"window\.__APP_CONFIG__=(\{.*?\});?</script>", raw, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:  # noqa: BLE001
        return None


def main():
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("2026-09-20")
    cfg_dir = pass_dir / "sources" / "configs"
    cfg_dir.mkdir(parents=True, exist_ok=True)
    n_txt = n_cfg = 0
    for sub in ("sites", "pricing"):
        for f in sorted((pass_dir / "sources" / sub).glob("*.html")):
            raw = f.read_text(encoding="utf-8", errors="replace")
            f.with_suffix(".txt").write_text(visible_text(raw) + "\n", encoding="utf-8")
            n_txt += 1
            if sub == "sites":
                cfg = app_config(raw)
                if cfg is not None:
                    camel = f.stem
                    (cfg_dir / f"{camel}.json").write_text(
                        json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
                    n_cfg += 1
    print(f"wrote {n_txt} text extracts, {n_cfg} app configs to {cfg_dir}")


if __name__ == "__main__":
    sys.exit(main())
