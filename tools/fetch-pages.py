#!/usr/bin/env python3
"""Fetch the published pricing / plan / docs pages of every sub2api sponsor.

Question this answers: for each provider, is there a public rate card, and what
does it literally say? Complements tools/fetch-sources.py (landing pages +
embedded __APP_CONFIG__). Raw snapshots land in PASS_DIR/sources/pricing/.

Usage: python3 tools/fetch-pages.py [PASS_DIR]
"""
import concurrent.futures as cf
import re
import sys
import time
import urllib.request
from pathlib import Path

PROXY = "https://api.rv.pkgforge.dev/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# label -> url
PAGES = {
    "OpenModel__model-pricing": "https://www.openmodel.ai/model-pricing",
    "OpenModel__docs": "https://docs.openmodel.ai/",
    "hao.ai__models": "https://hao.ai/models",
    "hao.ai__docs": "https://hao.ai/docs",
    "LanoX__model-access": "https://lanox.ai/model-access",
    "CodexEverywhere__docs-models": "https://docs.codex-everywhere.com/models/",
    "Qiniu__ai-plan": "https://qiniu.com/ai/plan",
    "Qiniu__ai-models": "https://www.qiniu.com/ai/models",
    "APIMart__model": "https://go.apimart.ai/model",
    "ETok__claude": "https://etok.ai/models/claude",
    "ETok__openai": "https://etok.ai/models/openai",
    "ETok__gemini": "https://etok.ai/models/gemini",
    "CCTK__home": "https://www.cctk.ai/",
    "CCTK__home-content": "https://home.cctk.ai",
    "APIKEY__docs": "https://docs.apikey.fan/",
    "Nagora__docs": "https://docs.nagora.ai/",
    "Fenno__home": "https://fenno.ai/",
    "PPdog__docs": "https://docs.pp.dog/",
    "Aimzoon__home": "http://aimzoon.com",
    "PPToken__docs": "https://docs.pptoken.cc/",
    "Pateway__docs": "https://docs.pateway.ai/",
    "AIGoCode__docs": "https://docs.aigocode.app/",
    "BmoPlus__home": "https://shop.bmoplus.com/",
    # infrastructure / proxies (outside the AI-plan ranking; kept for completeness)
    "ColaProxy__pricing": "https://colaproxy.com/pricing",
    "Proxy4Free__residential": "https://www.proxy4free.com/pricing/residential/",
    "RapidProxy__residential-pricing": "https://www.rapidproxy.io/residential-proxies/pricing",
    "DuckIP__buy-residential": "https://www.duckip.cn/buy/residential-proxy/",
    "RoxyBrowser__pricing": "https://roxybrowser.com/pricing",
    "Veilx__pricing": "https://veilx.io/pricing/",
    "AxisNow__pricing": "https://www.axisnow.io/pricing",
    "Swiftproxy__pricing": "https://www.swiftproxy.net/pricing",
}


def fetch(url: str, timeout: int = 55):
    req = urllib.request.Request(PROXY + url, headers={"User-Agent": UA, "Accept": "*/*"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read(), round(time.time() - t0, 2), None
    except Exception as e:  # noqa: BLE001
        return None, b"", round(time.time() - t0, 2), repr(e)[:160]


def main():
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("2026-09-20")
    out = pass_dir / "sources" / "pricing"
    out.mkdir(parents=True, exist_ok=True)
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch, u): k for k, u in PAGES.items()}
        for f in cf.as_completed(futs):
            k = futs[f]
            status, body, secs, err = f.result()
            (out / f"{k}.html").write_text(body.decode("utf-8", "replace"), encoding="utf-8")
            print(f"{k:38} http={status} bytes={len(body):>7} {secs:>5}s err={err}")
    print(f"\nwrote {out}")


if __name__ == "__main__":
    sys.exit(main())
