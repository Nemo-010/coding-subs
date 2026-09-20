#!/usr/bin/env python3
"""Fetch each sub2api sponsor/partner site through the pkgforge reverse proxy.

Question this answers: for every provider advertised in the Wei-Shaw/sub2api
README, which sites are live, what frontend do they run, and what public
configuration do they expose (registration, payment, subscription, model plaza,
custom endpoints)?

Usage: python3 tools/fetch-sources.py [PASS_DIR] [--only NAME]
Writes raw HTML under PASS_DIR/sources/sites/ and a JSON summary under
PASS_DIR/sources/sites/index.json. Nothing here is a measurement of price;
it is the primary capture every price claim must resolve against.
"""
import concurrent.futures as cf
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

PROXY = "https://api.rv.pkgforge.dev/"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# name -> base URL (advertised target; affiliate/ref params stripped)
SITES = {
    "CCTK.AI": "https://cctk.ai/",
    "OpenModel": "https://www.openmodel.ai/",
    "ETok": "https://etok.ai/",
    "APIKEY.FUN": "https://apikey.fan/",
    "AIGoCode": "https://aigocode.com/",
    "CodexEverywhere": "https://codex-everywhere.com/",
    "BmoPlus": "https://shop.bmoplus.com/",
    "Pateway": "https://pateway.ai/",
    "PPToken": "https://api.pptoken.cc/",
    "Aimzoon": "http://aimzoon.com/",
    "Nagora": "https://nagora.ai/",
    "QiniuAI": "https://www.qiniu.com/",
    "FennoAI": "https://api.fenno.ai/",
    "LanoX": "https://lanox.ai/",
    "hao.ai": "https://hao.ai/",
    "APIMart": "https://go.apimart.ai/",
    "PP.dog": "https://pp.dog/",
    "Bestproxy": "https://bestproxy.com/",
    "Veilx": "https://veilx.io/",
    "RoxyBrowser": "https://roxybrowser.com/",
    "Proxy4Free": "https://www.proxy4free.com/",
    "RapidProxy": "https://www.rapidproxy.io/",
    "Swiftproxy": "https://www.swiftproxy.net/",
    "DuckIP": "https://www.duckip.cn/",
    "AxisNow": "https://www.axisnow.io/",
    "ColaProxy": "https://colaproxy.com/",
}


def fetch(url: str, timeout: int = 55):
    req = urllib.request.Request(PROXY + url, headers={"User-Agent": UA, "Accept": "*/*"})
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            body = r.read()
            return r.status, body, round(time.time() - t0, 2), None
    except Exception as e:  # noqa: BLE001
        return None, b"", round(time.time() - t0, 2), repr(e)[:200]


def parse_config(html: str):
    m = re.search(r"window\.__APP_CONFIG__=(\{.*?\});?</script>", html, re.S)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except Exception:  # noqa: BLE001
        return {"_parse_error": True}


def title(html: str):
    m = re.search(r"<title[^>]*>(.*?)</title>", html, re.S | re.I)
    return re.sub(r"\s+", " ", m.group(1)).strip() if m else ""


def main():
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 and not sys.argv[1].startswith("-") else Path("2026-09-20")
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1]
    out = pass_dir / "sources" / "sites"
    out.mkdir(parents=True, exist_ok=True)
    names = [only] if only else list(SITES)
    summary = {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch, SITES[n]): n for n in names}
        for f in cf.as_completed(futs):
            n = futs[f]
            status, body, secs, err = f.result()
            html = body.decode("utf-8", "replace")
            cfg = parse_config(html)
            rec = {
                "url": SITES[n],
                "http": status,
                "bytes": len(body),
                "seconds": secs,
                "error": err,
                "title": title(html),
                "frontend": None,
                "config": None,
            }
            if cfg:
                keys = ["site_name", "site_subtitle", "registration_enabled", "email_verify_enabled",
                        "payment_enabled", "subscription_enabled", "available_channels_enabled",
                        "model_plaza_enabled", "model_plaza_require_auth", "affiliate_enabled",
                        "risk_control_enabled", "custom_endpoints", "custom_menus", "version",
                        "backend_mode_enabled", "balance_payment_disabled", "invitation_code_required"]
                rec["config"] = {k: cfg.get(k) for k in keys}
                rec["frontend"] = "sub2api" if "available_channels_enabled" in cfg else "other"
            (out / f"{re.sub(r'[^A-Za-z0-9._-]', '_', n)}.html").write_text(html, encoding="utf-8")
            summary[n] = rec
            print(f"{n:16} http={status} bytes={len(body):>7} {secs:>5}s fe={rec['frontend']} title={rec['title'][:60]!r} err={err}")
    (out / "index.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nwrote {out/'index.json'}")


if __name__ == "__main__":
    sys.exit(main())
