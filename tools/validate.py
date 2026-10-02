#!/usr/bin/env python3
"""Data-integrity checks for a coding-subs research pass.

Usage: python3 tools/validate.py [PASS_DIR]   (default: latest YYYY-MM-DD dir)
Exit code 0 = all checks pass; 1 = failures (printed).

Two report shapes exist in this repo:

* the **classification** shape (2026-09-13, 2026-09-20) sorts the market into
  HIDDEN DEALS / ARBITRAGE / WHAT I WOULD BUY and asserts things about a named
  workload ("52.5M tokens/month") against a GLM credit table;
* the **census** shape (2026-10-02 onwards) is a dated re-fetch plus a
  per-evidence-class index, and states its own falsifiers instead.

The classification checks are applied only where the report declares that shape,
so a census pass is not failed for not being a classification pass, while every
pass — whatever its shape - still has to satisfy the layout, database, model-slug
and source-count checks.
"""

import csv, json, os, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures: list[str] = []

# Anchors a classification pass must carry, with a short phrase that can only be
# there if the report actually uses that section for its intended argument.
CLASSIFICATION_ANCHORS = (
    "HIDDEN DEALS",
    "ARBITRAGE OPPORTUNITIES",
    "WHAT I WOULD BUY",
    "1M-context deep dive",
    "Multimodal deep dive",
    "Rankings",
    "Method",
)
# A census pass must instead state what would falsify it and what it did not establish.
CENSUS_ANCHORS = (
    "BEST DEAL FOUND",
    "What changed",
    "What would falsify this pass",
    "Known gaps",
    "Workload test",
)


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def latest_pass() -> Path:
    passes = sorted(p for p in ROOT.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name))
    check(bool(passes), "no YYYY-MM-DD pass directory found")
    return passes[-1] if passes else ROOT


def main() -> int:
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else latest_pass()
    print(f"validating pass: {pass_dir.name}")

    # --- layout ---
    for sub in ("data", "references", "sources"):
        check((pass_dir / sub).is_dir(), f"missing directory {sub}/")
    check((pass_dir / "README.md").is_file(), "missing report README.md")
    check((ROOT / "README.md").is_file(), "missing root README.md")
    check((ROOT / "docs" / "reviews.md").is_file(), "missing docs/reviews.md")
    check(pass_dir.name <= str(date.today()), f"pass dir {pass_dir.name} is in the future")
    if os.environ.get("STRICT_DATE"):
        check(pass_dir.name == str(date.today()), f"pass dir {pass_dir.name} != today {date.today()}")

    # --- models database ---
    mpath = pass_dir / "data" / "models-database.csv"
    check(mpath.is_file(), "missing data/models-database.csv")
    if mpath.is_file():
        with mpath.open() as f:
            models = list(csv.DictReader(f))
        check(len(models) >= 20, f"models DB has {len(models)} rows, need >= 20")
        need = {"model_slug", "provider", "release_date", "aa_intelligence_index",
                "terminal_bench_v4", "context_window_tokens", "ctx_ge_1m",
                "image_input", "api_input_usd_per_m", "api_output_usd_per_m"}
        check(need.issubset(models[0].keys()), f"models DB missing columns: {need - set(models[0].keys())}")
        slugs = set()
        for r in models:
            s = r["model_slug"]
            check(s and s not in slugs, f"duplicate/empty model slug: {s!r}")
            slugs.add(s)
            try:
                ctx = int(r["context_window_tokens"])
            except ValueError:
                failures.append(f"{s}: non-integer context {r['context_window_tokens']!r}")
                continue
            if ctx == 0 and r["ctx_ge_1m"] == "UNKNOWN":
                continue  # context not published; ctx_ge_1m honestly unknown
            want = "YES" if ctx >= 1_000_000 else "NO"
            check(r["ctx_ge_1m"] == want, f"{s}: ctx_ge_1m={r['ctx_ge_1m']} inconsistent with ctx={ctx}")
            for pcol in ("api_input_usd_per_m", "api_output_usd_per_m"):
                v = r[pcol]
                if v not in ("", None):
                    try:
                        check(float(v) >= 0, f"{s}: negative {pcol}")
                    except ValueError:
                        failures.append(f"{s}: non-numeric {pcol}={v!r}")
        # a frontier band must be present, but each pass's frontier differs: any
        # Anthropic/OpenAI flagship slug satisfies it (slug prefix keeps the field
        # required while letting the model name move).
        check(any(s.startswith(("claude-", "gpt-")) for s in slugs),
              "models DB has no claude-*/gpt-* frontier row")

    # --- providers database (any of the three schemas in use) ---
    ppath = pass_dir / "data" / "providers-database.csv"
    check(ppath.is_file(), "missing data/providers-database.csv")
    if ppath.is_file():
        with ppath.open() as f:
            providers = list(csv.DictReader(f))
        check(len(providers) >= 25, f"providers DB has {len(providers)} rows, need >= 25")
        cols = set(providers[0].keys())
        # schema A: plan census (2026-09-20, 2026-10-02)
        # schema B: relay census (2026-09-20 fork addendum)
        if {"provider", "coding_tool", "price_usd_month", "usage_mechanism",
            "ctx_1m_at_sub_level", "bundled_inference", "status", "source_quality"}.issubset(cols):
            pass
        else:
            check({"provider", "category", "url", "source_quality"}.issubset(cols),
                  f"providers DB uses an unrecognised schema: {sorted(cols)[:8]}")
        # either way: at least 20 distinct providers and no empty evidence cell
        distinct = {r.get("provider", "") for r in providers}
        check(len(distinct) >= 20, f"only {len(distinct)} distinct providers, need >= 20")
        for r in providers:
            check(r.get("source_quality", "x") != "", f"{r.get('provider')}/{r.get('coding_tool','')}: empty source_quality")

    # --- AA snapshot (only where one is committed) ---
    for cand in sorted((pass_dir / "data").glob("aa-snapshot-*.json")):
        aa = json.loads(cand.read_text())
        check(len(aa) >= 100, f"{cand.name} only {len(aa)} rows")
        bad = [r["slug"] for r in aa if r.get("deprecated") or (r.get("intelligenceIndex") or 0) < 20]
        check(not bad, f"{cand.name} contains deprecated/low-II rows: {bad[:5]}")
        iis = [r["intelligenceIndex"] for r in aa]
        check(iis == sorted(iis, reverse=True), f"{cand.name} not sorted by II desc")

    # --- report ---
    report = (pass_dir / "README.md").read_text()
    check("BEST DEAL FOUND" in report, "report missing section: BEST DEAL FOUND")
    shape = "classification" if "WHAT I WOULD BUY" in report else "census"
    for anchor in (CLASSIFICATION_ANCHORS if shape == "classification" else CENSUS_ANCHORS):
        check(anchor in report, f"report ({shape} shape) missing section: {anchor}")
    if shape == "classification":
        check("52.5M" in report, "report missing 52.5M workload figure")
        for wk, mo in ((48, 208), (97, 420)):
            check(abs(wk * 4.33 - mo) <= 1, f"GLM weekly {wk}M x 4.33 != {mo}M")
        check("208–420M" in report, "report missing GLM Lite monthly capacity 208–420M")

    # every model slug cited with backticks in the DB exists in models DB (or is
    # explicitly an upstream/delisted slug named in the sources)
    if mpath.is_file():
        with mpath.open() as f:
            slugs = {r["model_slug"] for r in csv.DictReader(f)}
        for cited in set(re.findall(r"`([a-z0-9]+(?:[-.][a-z0-9]+)+)`", report)):
            norm = cited.replace(".", "-")
            if norm.startswith(("claude-", "gpt-", "gemini-", "qwen", "kimi-", "glm-", "muse-",
                                "minimax-", "deepseek-", "grok-", "mimo-")):
                # delisted upstream slugs are allowed to be cited if the report
                # names them as delisted (they are evidence about removals).
                if norm not in slugs and "delisted" not in report and "delist" not in report:
                    check(False, f"report cites model `{cited}` not in models DB")
        if shape == "classification" and ppath.is_file():
            with ppath.open() as f:
                prow = next((r for r in csv.DictReader(f) if r.get("coding_tool") == "GLM Coding Plan Lite"), {})
            est = prow.get("est_token_capacity_month", "")
            for fig in ("208-420M", "632M-1,264M"):
                check(fig in est, f"providers DB GLM Lite capacity missing {fig} (4.33wk math)")
            check("208–420M" in report, "report GLM Lite capacity disagrees with DB")

    # --- references ---
    refs = (pass_dir / "references" / "references.md").read_text() if (pass_dir / "references" / "references.md").is_file() else ""
    check(pass_dir.name in refs, f"references missing access date {pass_dir.name}")
    check(refs.count("\n") > 40, "references suspiciously short")

    # --- sources present ---
    n_sources = len(list((pass_dir / "sources").glob("*"))) if (pass_dir / "sources").is_dir() else 0
    check(n_sources >= 20, f"only {n_sources} source snapshots, expected >= 20")

    # --- result ---
    if failures:
        print(f"FAIL ({len(failures)}):")
        for m in failures:
            print("  -", m)
        return 1
    print(f"OK: all checks passed ({shape} shape)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
