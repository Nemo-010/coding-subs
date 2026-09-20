#!/usr/bin/env python3
"""Data-integrity checks for coding-subs research passes.

Usage: python3 tools/validate.py [PASS_DIR]   (default: latest YYYY-MM-DD dir)
Exit code 0 = all checks pass; 1 = failures (printed).

Two pass shapes exist:
  * model/subscription pass  -> data/models-database.csv (original 2026-09-13 checks)
  * provider/relay pass      -> data/providers-database.csv (2026-09-20 checks)
A pass is validated against whichever shape its data/ directory matches.
"""
import csv, json, os, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
failures: list[str] = []


def check(cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def latest_pass() -> Path:
    passes = sorted(p for p in ROOT.iterdir() if p.is_dir() and re.fullmatch(r"\d{4}-\d{2}-\d{2}", p.name))
    check(bool(passes), "no YYYY-MM-DD pass directory found")
    return passes[-1] if passes else ROOT


def layout_checks(pass_dir: Path) -> None:
    for sub in ("data", "references", "sources"):
        check((pass_dir / sub).is_dir(), f"missing directory {sub}/")
    check((pass_dir / "README.md").is_file(), "missing report README.md")
    check((ROOT / "README.md").is_file(), "missing root README.md")
    check((ROOT / "docs" / "reviews.md").is_file(), "missing docs/reviews.md")
    check(pass_dir.name <= str(date.today()), f"pass dir {pass_dir.name} is in the future")
    if os.environ.get("STRICT_DATE"):
        check(pass_dir.name == str(date.today()), f"pass dir {pass_dir.name} != today {date.today()}")


def model_pass_checks(pass_dir: Path) -> None:
    mpath = pass_dir / "data" / "models-database.csv"
    with mpath.open() as f:
        models = list(csv.DictReader(f))
    check(len(models) >= 30, f"models DB has {len(models)} rows, need >= 30")
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
        want = "YES" if ctx >= 1_000_000 else "NO"
        check(r["ctx_ge_1m"] == want, f"{s}: ctx_ge_1m={r['ctx_ge_1m']} inconsistent with ctx={ctx}")
        for pcol in ("api_input_usd_per_m", "api_output_usd_per_m"):
            v = r[pcol]
            if v not in ("", None):
                try:
                    check(float(v) >= 0, f"{s}: negative {pcol}")
                except ValueError:
                    failures.append(f"{s}: non-numeric {pcol}={v!r}")
    check("claude-opus-5" in slugs, "models DB missing claude-opus-5")

    ppath = pass_dir / "data" / "providers-database.csv"
    with ppath.open() as f:
        providers = list(csv.DictReader(f))
    check(len(providers) >= 25, f"providers DB has {len(providers)} rows, need >= 25")
    pneed = {"provider", "coding_tool", "price_usd_month", "usage_mechanism",
             "ctx_1m_at_sub_level", "bundled_inference", "status", "source_quality"}
    check(pneed.issubset(providers[0].keys()), f"providers DB missing columns: {pneed - set(providers[0].keys())}")
    distinct = {r["provider"] for r in providers}
    check(len(distinct) >= 20, f"only {len(distinct)} distinct providers, need >= 20")
    for r in providers:
        check(r["source_quality"] != "", f"{r['provider']}/{r['coding_tool']}: empty source_quality")

    apath = pass_dir / "data" / "aa-snapshot-2026-09-13.json"
    if apath.is_file():
        aa = json.loads(apath.read_text())
        check(len(aa) >= 100, f"AA snapshot only {len(aa)} rows")
        bad = [r["slug"] for r in aa if r.get("deprecated") or (r.get("intelligenceIndex") or 0) < 20]
        check(not bad, f"AA snapshot contains deprecated/low-II rows: {bad[:5]}")
        iis = [r["intelligenceIndex"] for r in aa]
        check(iis == sorted(iis, reverse=True), "AA snapshot not sorted by II desc")

    report = (pass_dir / "README.md").read_text()
    for anchor in ("BEST DEAL FOUND", "HIDDEN DEALS", "ARBITRAGE OPPORTUNITIES",
                   "WHAT I WOULD BUY", "Workload test", "1M-context deep dive",
                   "Multimodal deep dive", "Rankings", "Method"):
        check(anchor in report, f"report missing section: {anchor}")
    check("52.5M" in report, "report missing 52.5M workload figure")
    check(15 + 37.5 == 52.5, "workload arithmetic 15M + 37.5M != 52.5M")
    for wk, mo in ((48, 208), (97, 420)):
        check(abs(wk * 4.33 - mo) <= 1, f"GLM weekly {wk}M x 4.33 != {mo}M")
    check("208–420M" in report, "report missing GLM Lite monthly capacity 208–420M")
    if mpath.is_file():
        with mpath.open() as f:
            slugs = {r["model_slug"] for r in csv.DictReader(f)}
        for cited in set(re.findall(r"`([a-z0-9]+(?:[-.][a-z0-9]+)+)`", report)):
            norm = cited.replace(".", "-")
            if norm.startswith(("claude-", "gpt-", "gemini-", "qwen", "kimi-", "glm-", "muse-",
                                "minimax-", "deepseek-", "grok-", "mimo-")):
                check(norm in slugs, f"report cites model `{cited}` not in models DB")
        with ppath.open() as f:
            prow = next((r for r in csv.DictReader(f) if r["coding_tool"] == "GLM Coding Plan Lite"), {})
        est = prow.get("est_token_capacity_month", "")
        for fig in ("208-420M", "632M-1,264M"):
            check(fig in est, f"providers DB GLM Lite capacity missing {fig} (4.33wk math)")
        check("208–420M" in report, "report GLM Lite capacity disagrees with DB")


def provider_pass_checks(pass_dir: Path) -> None:
    drop = pass_dir.name  # e.g. 2026-09-20
    ppath = pass_dir / "data" / "providers-database.csv"
    check(ppath.is_file(), "missing data/providers-database.csv")
    if ppath.is_file():
        with ppath.open() as f:
            provs = list(csv.DictReader(f))
        check(len(provs) >= 26, f"provider DB has {len(provs)} rows, need >= 26")
        need = {"provider", "category", "url", "free_offer", "price_basis",
                "cheapest_published", "rate_card_published", "source_quality"}
        check(need.issubset(provs[0].keys()), f"provider DB missing columns: {need - set(provs[0].keys())}")
        distinct = {r["provider"] for r in provs}
        check(len(distinct) >= 20, f"only {len(distinct)} distinct providers, need >= 20")
        for r in provs:
            check(r["source_quality"] in ("VERIFIED", "ADVERTISED", "UNKNOWN"),
                  f"{r['provider']}: bad source_quality {r['source_quality']!r}")

    rpath = pass_dir / "data" / "rate-cards.csv"
    check(rpath.is_file(), "missing data/rate-cards.csv")
    if rpath.is_file():
        with rpath.open() as f:
            cards = list(csv.DictReader(f))
        check(len(cards) >= 20, f"rate-cards has {len(cards)} rows, need >= 20")
        for r in cards:
            try:
                oi, oo = float(r["official_in_usd_per_m"]), float(r["official_out_usd_per_m"])
                pi, po = float(r["provider_in_usd_per_m"]), float(r["provider_out_usd_per_m"])
                mult = float(r["multiple"])
            except ValueError as e:
                failures.append(f"rate-card non-numeric: {r} ({e})")
                continue
            for val, name in ((oi, "official_in"), (oo, "official_out"), (pi, "provider_in"),
                              (po, "provider_out"), (mult, "multiple")):
                check(val > 0, f"{r['provider']}/{r['model']}: non-positive {name}")
            check(abs(pi / oi - mult) <= 0.005,
                  f"{r['provider']}/{r['model']}: input multiple {pi/oi:.4f} != {mult}")
            check(abs(po / oo - mult) <= 0.005,
                  f"{r['provider']}/{r['model']}: output multiple {po/oo:.4f} != {mult}")

    apath = pass_dir / "data" / "subscription-plans.csv"
    check(apath.is_file(), "missing data/subscription-plans.csv")

    ipath = pass_dir / "data" / "reachability.json"
    check(ipath.is_file(), "missing data/reachability.json")
    if ipath.is_file():
        rj = json.loads(ipath.read_text())
        check(rj.get("rounds") == 3, f"reachability rounds={rj.get('rounds')}, expected 3")
        check(len(rj.get("results", {})) >= 26, "reachability covers <26 endpoints")

    sidx = pass_dir / "sources" / "sites" / "index.json"
    check(sidx.is_file(), "missing sources/sites/index.json")
    if sidx.is_file():
        sites = json.loads(sidx.read_text())
        check(len(sites) >= 26, f"only {len(sites)} site snapshots, need >= 26")

    upath = pass_dir / "data" / "providers-union.csv"
    check(upath.is_file(), "missing data/providers-union.csv (run tools/research-providers.sh)")
    if upath.is_file():
        with upath.open() as f:
            union = list(csv.DictReader(f))
        check(len(union) >= 40, f"provider union has {len(union)} rows, need >= 40")
        uneed = {"provider", "display_name", "kind", "repos", "in_both",
                 "confidence", "methods", "evidence_count", "first_evidence"}
        check(uneed.issubset(union[0].keys()),
              f"union missing columns: {uneed - set(union[0].keys())}")
        both = [r for r in union if r["in_both"] == "yes"]
        check(len(both) >= 15, f"only {len(both)} providers appear in both repos")
        for r in union:
            check(r["repos"] != "", f"{r['provider']}: empty repos")
            check(r["evidence_count"] != "", f"{r['provider']}: empty evidence_count")
    for sub in ("sub2api", "cliproxyapi"):
        sp = pass_dir / "data" / f"providers-{sub}.csv"
        check(sp.is_file(), f"missing data/providers-{sub}.csv")
        check((pass_dir / "data" / f"providers-{sub}.jsonl").is_file(),
              f"missing data/providers-{sub}.jsonl evidence")

    recon = pass_dir / "RECONCILED-PROVIDERS.md"
    check(recon.is_file(), "missing RECONCILED-PROVIDERS.md")
    if recon.is_file():
        rtext = recon.read_text()
        check("CLIProxyAPI" in rtext, "reconciled report does not mention CLIProxyAPI")
        check("did NOT establish" in rtext, "reconciled report missing 'did NOT establish'")
        check("61fdfc34" in rtext, "reconciled report missing CLIProxyAPI commit pin")

    report = (pass_dir / "README.md").read_text()
    for anchor in ("BEST DEAL FOUND", "did NOT establish", "RANKING 1", "RANKING 2",
                   "Best \"free\"", "Best \"cheap\"", "Best \"reliable\"", "Best \"deal\"",
                   "Known gaps", "Provenance"):
        check(anchor in report, f"report missing section: {anchor}")
    check("2026-09-20" in report, "report missing research date")
    check("19794bc" in report, "report missing subject commit pin")

    refs = (pass_dir / "references" / "references.md").read_text()
    check(drop in refs, f"references missing access date {drop}")
    ref_nums = {int(m.group(1)) for m in re.finditer(r"^(\d+)\.", refs, re.M)}
    check(len(ref_nums) >= 20, f"references has {len(ref_nums)} numbered entries, need >= 20")
    for cited in {int(n) for n in re.findall(r"source (\d+)", report)}:
        check(cited in ref_nums, f"report cites source {cited} with no reference entry")


def main() -> int:
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else latest_pass()
    print(f"validating pass: {pass_dir.name}")
    layout_checks(pass_dir)

    model_shape = (pass_dir / "data" / "models-database.csv").is_file()
    provider_shape = (pass_dir / "data" / "providers-database.csv").is_file()
    if model_shape:
        model_pass_checks(pass_dir)
    if provider_shape and not model_shape:
        provider_pass_checks(pass_dir)
    if not model_shape and not provider_shape:
        failures.append("pass has neither models-database.csv nor providers-database.csv")

    if failures:
        print(f"FAIL ({len(failures)}):")
        for m in failures:
            print("  -", m)
        return 1
    print("OK: all checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
