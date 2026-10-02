#!/usr/bin/env python3
"""Fetch first-party subscription/pricing pages for a coding-subs research pass.

Fetches the live first-party pages listed in PAGES into <pass>/sources/. Deliberately
proxy-free: measurements come from this network, not through anyone else's. Pages that
return gzip/brotli despite no Accept-Encoding are detected by `file`/magic bytes and
should be gunzip-decoded before text extraction (see antigravity snapshots in 2026-09-20).

Usage: python3 tools/fetch-firstparty.py [PASS_DIR]   (default: latest YYYY-MM-DD dir)
"""
import concurrent.futures as cf
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"

# label -> url   (pass 2026-09-20 set; extend per pass)
PAGES = {
    "zai-glm-coding-plan-overview.md": "https://docs.z.ai/devpack/overview.md",
    "zai-glm-coding-plan-faq.md": "https://docs.z.ai/devpack/faq.md",
    "zai-teamplan.md": "https://docs.z.ai/devpack/teamplan.md",
    "zai-plan-update-announcement.md": "https://docs.z.ai/devpack/transition.md",
    "zai-glm53-flash-campaign.md": "https://docs.z.ai/devpack/notice/event-glm-5.3-flash.md",
    "openai-codex-pricing.md": "https://developers.openai.com/codex/pricing.md",
    "anthropic-model-overview-docs.md": "https://docs.claude.com/en/docs/about-claude/models/overview.md",
    "anthropic-pricing-page.html": "https://www.anthropic.com/pricing",
    "anthropic-context-window-paid-plans.html": "https://support.claude.com/en/articles/8606394-how-large-is-the-context-window-on-paid-plans",
    "gemini-api-pricing.html": "https://ai.google.dev/gemini-api/docs/pricing",
    "antigravity-plans-doc.html": "https://antigravity.google/docs/plans/",
    "antigravity-models-doc.html": "https://antigravity.google/docs/models/",
    "google-ai-subscriptions.html": "https://gemini.google/subscriptions/",
    "minimax-token-plan-intro.md": "https://platform.minimax.io/docs/token-plan/intro.md",
    "minimax-token-plan-pricing.md": "https://platform.minimax.io/docs/guides/pricing-token-plan.md",
    "kimi-membership-doc.html": "https://www.kimi.com/code/docs/en/kimi-code/membership.html",
    "kimi-help-membership-overview.html": "https://www.kimi.com/en/help/membership/membership-overview",
    "kimi-api-pricing.md": "https://platform.kimi.ai/docs/pricing/chat.md",
    "github-copilot-plans.html": "https://docs.github.com/en/copilot/get-started/plans",
    "meta-muse-subscriptions.md": "https://dev.meta.ai/docs/muse-code/subscriptions.md",
    "alibaba-coding-plan-doc.html": "https://www.alibabacloud.com/help/en/model-studio/coding-plan",
    "trae-pricing.html": "https://www.trae.ai/pricing",
    "kilo-pricing.html": "https://kilo.ai/pricing",
    "kiro-pricing.html": "https://kiro.dev/pricing/",
    "replit-pricing.html": "https://replit.com/pricing",
    "augment-pricing.html": "https://www.augmentcode.com/pricing",
    "cerebras-code-pricing.html": "https://www.cerebras.ai/code",
    "cursor-pricing.html": "https://cursor.com/pricing",
    "mistral-lechat-pricing.html": "https://mistral.ai/pricing",
    "qoder-pricing.html": "https://qoder.com/pricing",
    "codebuddy.html": "https://www.codebuddy.ai/",
    "commandcode-pricing.html": "https://commandcode.ai/pricing",
    "devin-pricing.html": "https://devin.ai/pricing",
    "zed-pricing.html": "https://zed.dev/pricing",
    "warp-pricing.html": "https://www.warp.dev/pricing",
    "factory-pricing.html": "https://factory.ai/pricing",
    "opencode-zen.html": "https://opencode.ai/zen/",
    "fx-cny-usd.txt": "https://open.er-api.com/v6/latest/USD",
    "aa-models-page.html": "https://artificialanalysis.ai/models",
    "modelsdev-api.json": "https://models.dev/api.json",
    # --- added for the 2026-10-02 pass ---
    "opencode-go.html": "https://opencode.ai/docs/go/",
    "amp-pricing.html": "https://ampcode.com/pricing",
    "jetbrains-ai.html": "https://www.jetbrains.com/ai/",
    "xai-news.html": "https://x.ai/news",
    "alibaba-coding-plan-doc-1002.html": "https://www.alibabacloud.com/help/en/model-studio/coding-plan",
    "qwen-code-readme.md": "https://raw.githubusercontent.com/QwenLM/qwen-code/main/README.md",
    # third-party directories referenced by issues #1/#2 (kept as snapshots, not as first-party evidence)
    "thirdparty-free-llm-api-index.md": "https://raw.githubusercontent.com/robhunter/agentdeals/main/artifacts/free-llm-api-index/README.md",
    "thirdparty-baipiaoji-limits.json": "https://raw.githubusercontent.com/f-tiger/verified-ai-free-tiers/main/limits.json",
    "thirdparty-baipiaoji-limits.md": "https://raw.githubusercontent.com/f-tiger/verified-ai-free-tiers/main/limits.md",
    "thirdparty-awesome-free-llm-api.md": "https://raw.githubusercontent.com/peter123023/awesome-free-llm-api/main/README.en.md",
    "thirdparty-free-llm.md": "https://raw.githubusercontent.com/nejib1/Free-LLM/main/README.md",
    "thirdparty-real-api-pricing-adopted.csv": "https://raw.githubusercontent.com/FeiZhuLulu/real-api-pricing/main/data/adopted.csv",
    "thirdparty-real-api-pricing-readme.md": "https://raw.githubusercontent.com/FeiZhuLulu/real-api-pricing/main/README.md",
    "thirdparty-subscription-multipliers.md": "https://raw.githubusercontent.com/phuryn/experiments/main/subscription-multipliers/README.md",
}


def fetch(out_dir: pathlib.Path, name: str, url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html,text/markdown,application/json,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            data = r.read()
            (out_dir / name).write_bytes(data)
            return name, f"OK {r.status} {len(data)}"
    except Exception as e:  # noqa: BLE001 - record, don't crash the batch
        return name, f"FAIL {type(e).__name__}: {e}"


def main() -> int:
    passes = sorted(p for p in ROOT.iterdir() if p.is_dir() and len(p.name) == 10 and p.name[4] == "-")
    pass_dir = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else passes[-1]
    out = pass_dir / "sources"
    out.mkdir(parents=True, exist_ok=True)
    print(f"fetching {len(PAGES)} pages -> {out}")
    with cf.ThreadPoolExecutor(8) as ex:
        for name, status in ex.map(lambda kv: fetch(out, *kv), PAGES.items()):
            print(f"{status:28s} {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
