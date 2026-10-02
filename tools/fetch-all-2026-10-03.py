#!/usr/bin/env python3
"""Fetch EVERY first-party source for a pass, one at a time, recording http/bytes/sha256.

This is deliberately serial and deliberately dumb: one URL, one request, one file,
one line of the log. A source that fails is recorded as failed and not retried into
success, because a 403 is a fact about the vantage point and deleting it hides that.

Usage: python3 tools/fetch-all-2026-10-03.py PASS_DIR
"""
import hashlib
import json
import pathlib
import sys
import time
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/126.0.0.0 Safari/537.36")

# label -> url.  Ordered: first-party vendor pages, then issue-source repos, then FRX.
SOURCES = [
    # ---- Z.ai (6 plan rows) ----
    ("zai-overview.md", "https://docs.z.ai/devpack/overview.md"),
    ("zai-faq.md", "https://docs.z.ai/devpack/faq.md"),
    ("zai-teamplan.md", "https://docs.z.ai/devpack/teamplan.md"),
    ("zai-transition.md", "https://docs.z.ai/devpack/transition.md"),
    ("zai-flash-campaign.md", "https://docs.z.ai/devpack/notice/event-glm-5.3-flash.md"),
    ("zai-llms-index.txt", "https://docs.z.ai/llms.txt"),
    # ---- MiniMax (3 rows) ----
    ("minimax-token-plan-intro.md", "https://platform.minimax.io/docs/token-plan/intro.md"),
    ("minimax-token-plan-pricing.md", "https://platform.minimax.io/docs/guides/pricing-token-plan.md"),
    # ---- Moonshot / Kimi ----
    ("kimi-membership.html", "https://www.kimi.com/code/docs/en/kimi-code/membership.html"),
    ("kimi-help-membership.html", "https://www.kimi.com/en/help/membership/membership-overview"),
    ("kimi-api-pricing.md", "https://platform.kimi.ai/docs/pricing/chat.md"),
    # ---- Meta Muse ----
    ("meta-muse-subscriptions.md", "https://dev.meta.ai/docs/muse-code/subscriptions.md"),
    # ---- OpenAI ----
    ("openai-codex-pricing.md", "https://developers.openai.com/codex/pricing.md"),
    ("openai-chatgpt-pricing.html", "https://openai.com/chatgpt/pricing/"),
    # ---- Anthropic ----
    ("anthropic-pricing.html", "https://www.anthropic.com/pricing"),
    ("anthropic-models.md", "https://docs.claude.com/en/docs/about-claude/models/overview.md"),
    ("anthropic-context-paid.html", "https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-plans"),
    # ---- Google ----
    ("google-gemini-api-pricing.html", "https://ai.google.dev/gemini-api/docs/pricing"),
    ("google-ai-subscriptions.html", "https://gemini.google/subscriptions/"),
    ("antigravity-plans.html", "https://antigravity.google/docs/plans/"),
    ("antigravity-models.html", "https://antigravity.google/docs/models/"),
    # ---- GitHub ----
    ("github-copilot-plans.html", "https://docs.github.com/en/copilot/get-started/plans"),
    # ---- Alibaba ----
    ("alibaba-coding-plan.html", "https://www.alibabacloud.com/help/en/model-studio/coding-plan"),
    # ---- ByteDance Trae ----
    ("trae-pricing.html", "https://www.trae.ai/pricing"),
    # ---- Kilo ----
    ("kilo-pricing.html", "https://kilo.ai/pricing"),
    # ---- Cline ----
    ("cline-docs.html", "https://docs.cline.bot/getting-started/installing-cline"),
    # ---- OpenCode ----
    ("opencode-go.html", "https://opencode.ai/docs/go/"),
    ("opencode-zen.html", "https://opencode.ai/zen/"),
    # ---- Cursor ----
    ("cursor-pricing.html", "https://cursor.com/pricing"),
    # ---- Cognition / Devin / Windsurf ----
    ("devin-pricing.html", "https://devin.ai/pricing"),
    ("windsurf-pricing.html", "https://windsurf.com/pricing"),
    # ---- AWS Kiro ----
    ("kiro-pricing.html", "https://kiro.dev/pricing/"),
    # ---- Replit ----
    ("replit-pricing.html", "https://replit.com/pricing"),
    # ---- Augment ----
    ("augment-pricing.html", "https://www.augmentcode.com/pricing"),
    # ---- Mistral ----
    ("mistral-pricing.html", "https://mistral.ai/pricing"),
    # ---- Command Code ----
    ("commandcode-pricing.html", "https://commandcode.ai/pricing"),
    # ---- Factory ----
    ("factory-pricing.html", "https://factory.ai/pricing"),
    # ---- Zed ----
    ("zed-pricing.html", "https://zed.dev/pricing"),
    # ---- Warp ----
    ("warp-pricing.html", "https://www.warp.dev/pricing"),
    # ---- Amp ----
    ("amp-pricing.html", "https://ampcode.com/pricing"),
    # ---- JetBrains ----
    ("jetbrains-ai.html", "https://www.jetbrains.com/ai/"),
    # ---- xAI ----
    ("xai-news.html", "https://x.ai/news"),
    ("xai-grok-pricing.html", "https://x.ai/api"),
    # ---- DeepSeek ----
    ("deepseek-pricing.html", "https://api-docs.deepseek.com/quick_start/pricing"),
    # ---- Qwen ----
    ("qwen-code-readme.md", "https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md"),
    # ---- models.dev aggregate ----
    ("models-dev-api.json", "https://models.dev/api.json"),
    # ---- FX ----
    ("fx-usd.json", "https://open.er-api.com/v6/latest/USD"),
    # ---- issue #1 sources ----
    ("issue1-awesome-free-llm-api.md", "https://raw.githubusercontent.com/peter123023/awesome-free-llm-api/main/README.en.md"),
    ("issue1-verified-ai-free-tiers-limits.json", "https://raw.githubusercontent.com/f-tiger/verified-ai-free-tiers/main/limits.json"),
    ("issue1-verified-ai-free-tiers-limits.md", "https://raw.githubusercontent.com/f-tiger/verified-ai-free-tiers/main/limits.md"),
    ("issue1-free-llm.md", "https://raw.githubusercontent.com/nejib1/Free-LLM/main/README.md"),
    ("issue1-agentdeals-index.md", "https://raw.githubusercontent.com/robhunter/agentdeals/main/artifacts/free-llm-api-index/README.md"),
    # ---- issue #2 sources ----
    ("issue2-subscription-multipliers.md", "https://raw.githubusercontent.com/phuryn/experiments/main/subscription-multipliers/README.md"),
    ("issue2-real-api-pricing.md", "https://raw.githubusercontent.com/FeiZhuLulu/real-api-pricing/main/README.md"),
    ("issue2-real-api-pricing-adopted.csv", "https://raw.githubusercontent.com/FeiZhuLulu/real-api-pricing/main/data/adopted.csv"),
]

def fetch(label, url, outdir, timeout=40):
    req = urllib.request.Request(url, headers={
        "User-Agent": UA,
        "Accept": "text/html,application/xhtml+xml,application/json,text/plain,*/*",
        "Accept-Language": "en-US,en;q=0.9",
    })
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            ms = round((time.time() - t0) * 1000)
            (outdir / label).write_bytes(raw)
            return {"label": label, "url": url, "http": r.status, "bytes": len(raw),
                    "ms": ms, "sha256": hashlib.sha256(raw).hexdigest(), "error": None}
    except urllib.error.HTTPError as e:
        ms = round((time.time() - t0) * 1000)
        body = b""
        try:
            body = e.read(20000)
        except Exception:
            pass
        (outdir / (label + ".error")).write_bytes(body)
        return {"label": label, "url": url, "http": e.code, "bytes": len(body),
                "ms": ms, "sha256": hashlib.sha256(body).hexdigest(), "error": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        return {"label": label, "url": url, "http": None, "bytes": 0, "ms": round((time.time()-t0)*1000),
                "sha256": None, "error": type(e).__name__}

def main():
    pass_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "2026-10-03"
    outdir = pass_dir / "sources"
    outdir.mkdir(parents=True, exist_ok=True)
    log = []
    print(f"fetching {len(SOURCES)} sources serially into {outdir}")
    for i, (label, url) in enumerate(SOURCES, 1):
        r = fetch(label, url, outdir)
        log.append(r)
        mark = "ok " if r["error"] is None else "ERR"
        size = f"{r['bytes']:>9,}" if r["bytes"] else "        -"
        print(f"  {i:>2}/{len(SOURCES)} {mark} {r['http'] or '-':>4} {size}B {r['ms']:>6}ms  {label}")
    (pass_dir / "data" / "fetch-log.json").write_text(json.dumps(log, indent=2))
    ok = sum(1 for r in log if r["error"] is None)
    print(f"\n{ok}/{len(SOURCES)} fetched clean")
    return 0

if __name__ == "__main__":
    sys.exit(main())
