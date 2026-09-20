#!/usr/bin/env python3
"""Probe reachability of every sub2api sponsor endpoint, N rounds.

Question this answers: which advertised provider endpoints were actually
reachable, at what HTTP status and TTFB, from this sandbox on the research date?
Every request goes through the pkgforge reverse proxy, so the latency is the
proxy's, NOT the provider's own network quality, and the result must be read
that way. The status is the useful part; the milliseconds are indicative only.

Usage: python3 tools/probe-uptime.py [PASS_DIR] [ROUNDS]
Exit: 0 ran, 1 ran and <50% of endpoints were reachable in the final round, 2 could not run.
Writes PASS_DIR/data/reachability.json.
"""
import concurrent.futures as cf
import json
import sys
import time
import urllib.request
from pathlib import Path

PROXY = "https://api.rv.pkgforge.dev/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# base, health path ("" = none)
ENDPOINTS = {
    "CCTK.AI": ("https://cctk.ai", "/health"),
    "OpenModel": ("https://www.openmodel.ai", ""),
    "ETok": ("https://etok.ai", ""),
    "APIKEY.FUN": ("https://apikey.fan", "/health"),
    "AIGoCode": ("https://aigocode.com", ""),
    "CodexEverywhere": ("https://codex-everywhere.com", ""),
    "BmoPlus": ("https://shop.bmoplus.com", ""),
    "Pateway": ("https://pateway.ai", ""),
    "PPToken": ("https://api.pptoken.cc", "/health"),
    "Aimzoon": ("http://aimzoon.com", ""),
    "Nagora": ("https://nagora.ai", "/health"),
    "QiniuAI": ("https://www.qiniu.com", ""),
    "FennoAI": ("https://api.fenno.ai", "/health"),
    "LanoX": ("https://lanox.ai", ""),
    "hao.ai": ("https://hao.ai", ""),
    "APIMart": ("https://go.apimart.ai", ""),
    "PP.dog": ("https://pp.dog", "/health"),
    "Bestproxy": ("https://bestproxy.com", ""),
    "Veilx": ("https://veilx.io", ""),
    "RoxyBrowser": ("https://roxybrowser.com", ""),
    "Proxy4Free": ("https://www.proxy4free.com", ""),
    "RapidProxy": ("https://www.rapidproxy.io", ""),
    "Swiftproxy": ("https://www.swiftproxy.net", ""),
    "DuckIP": ("https://www.duckip.cn", ""),
    "AxisNow": ("https://www.axisnow.io", ""),
    "ColaProxy": ("https://colaproxy.com", ""),
}


def one(url: str, timeout: int = 40):
    req = urllib.request.Request(PROXY + url, headers={"User-Agent": UA}, method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            r.read(2048)
            return {"http": r.status, "ms": round((time.time() - t0) * 1000), "error": None}
    except Exception as e:  # noqa: BLE001
        code = getattr(e, "code", None)
        return {"http": code, "ms": round((time.time() - t0) * 1000), "error": type(e).__name__}


def main():
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("2026-09-20")
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    results = {name: [] for name in ENDPOINTS}
    for rnd in range(rounds):
        with cf.ThreadPoolExecutor(max_workers=8) as ex:
            futs = {}
            for name, (base, health) in ENDPOINTS.items():
                futs[ex.submit(one, base + health)] = name
            for f in cf.as_completed(futs):
                results[futs[f]].append(f.result())
        print(f"round {rnd + 1}/{rounds} done")
    summary = {}
    reachable = 0
    for name, runs in results.items():
        ok = sum(1 for r in runs if r["http"] == 200)
        ttfbs = sorted(r["ms"] for r in runs if r["http"] == 200)
        summary[name] = {
            "runs": runs,
            "ok": ok,
            "rounds": rounds,
            "median_ms_ok": ttfbs[len(ttfbs) // 2] if ttfbs else None,
        }
        if ok:
            reachable += 1
        print(f"  {name:16} ok={ok}/{rounds} median_ms={summary[name]['median_ms_ok']}")
    out = pass_dir / "data" / "reachability.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"date": "2026-09-20", "via": "api.rv.pkgforge.dev reverse proxy",
                               "rounds": rounds, "results": summary}, indent=2))
    print(f"\n{reachable}/{len(ENDPOINTS)} endpoints reachable; wrote {out}")
    if reachable < len(ENDPOINTS) / 2:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
