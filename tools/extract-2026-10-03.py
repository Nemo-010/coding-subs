#!/usr/bin/env python3
"""Provider-by-provider extraction from the 2026-10-03 fetched pages.

One block per provider. Each reads only the page it names and prints what it found.
Comparison against the previous pass is deliberately a SEPARATE script, so an
extraction bug cannot hide behind a comparison that was written to match it.
"""
import html
import pathlib
import re

SRC = pathlib.Path("2026-10-03/sources")

def text(name):
    p = SRC / name
    if not p.is_file():
        return ""
    t = p.read_bytes().decode("utf-8", errors="replace")
    if "<" in t[:2000]:
        t = re.sub(r"<script[^>]*>.*?</script>", " ", t, flags=re.S)
        t = re.sub(r"<style[^>]*>.*?</style>", " ", t, flags=re.S)
        t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))

def prices(t, n=14):
    return ", ".join(list(dict.fromkeys(re.findall(r"\$\s?\d+(?:\.\d+)?", t)))[:n])

def grab(t, pat):
    m = re.search(pat, t, re.I)
    return m.group(0).strip() if m else None

def show(title, d):
    print(f"\n=== {title}")
    for k, v in d.items():
        print(f"  {' ' if v else '!'} {k:32} {v}")

z = text("zai-overview.md") + text("zai-faq.md") + text("zai-teamplan.md")
show("Z.ai GLM Coding Plan", {
    "all prices": prices(z, 10),
    "team seats": grab(z, r"Standard[^|]{0,40}\|[^|]{0,40}\|[^|]{0,40}"),
    "legacy/migration": grab(z, r"(?:legacy|migration|transition)[^.]{0,140}"),
})

m = text("minimax-token-plan-intro.md") + text("minimax-token-plan-pricing.md")
show("MiniMax Token Plan", {
    "prices": prices(m, 8),
    "credit tiers": grab(m, r"(?:Plus|Max|Ultra)[^|]{0,120}"),
})

k = text("kimi-membership.html") + text("kimi-help-membership.html")
show("Moonshot Kimi Code", {
    "prices": prices(k, 12),
    "ladder": grab(k, r"(?:Starter|Basic|Standard|Advanced|Pro|Max)[^|]{0,140}"),
})

mu = text("meta-muse-subscriptions.md")
show("Meta Muse Code", {
    "prices": prices(mu, 12),
    "plans": grab(mu, r"(?:Free|Everyday|High Usage|Power Usage|Contributor)[^.]{0,140}"),
})

show("Anthropic", {"Pro/Max": grab(text("anthropic-pricing.html"), r"(?:Claude )?Pro[^.]{0,60}\$\s?\d+(?:\.\d+)?"),
                   "prices": prices(text("anthropic-pricing.html"), 14)})

g = text("google-ai-subscriptions.html")
show("Google AI subscriptions", {"Pro": grab(g, r"AI Pro[^.]{0,60}\$\s?\d+(?:\.\d+)?"),
                                "Ultra": grab(g, r"Ultra[^.]{0,80}\$\s?\d+(?:\.\d+)?"),
                                "prices": prices(g, 12)})

gh = text("github-copilot-plans.html")
show("GitHub Copilot", {"tiers": grab(gh, r"Copilot (?:Free|Pro\+?|Business|Enterprise|Max)[^.]{0,60}\$\s?\d+(?:\.\d+)?"),
                        "prices": prices(gh, 10),
                        "credits": grab(gh, r"\d[\d,]*\s*(?:premium requests|credits)[^.]{0,60}")})

show("Alibaba Model Studio Coding Plan", {"prices": prices(text("alibaba-coding-plan.html"), 10),
                                          "requests": grab(text("alibaba-coding-plan.html"), r"\d[\d,]*\s*requests[^.]{0,60}")})

t = text("trae-pricing.html")
show("ByteDance Trae", {"prices": prices(t, 14), "tiers": grab(t, r"(?:Free|Pro\+|Pro|Ultra)[^.]{0,100}")})

c = text("cursor-pricing.html")
show("Cursor", {"prices": prices(c, 14), "tiers": grab(c, r"(?:Hobby|Pro|Ultra|Teams)[^.]{0,90}")})

d = text("devin-pricing.html")
show("Cognition Devin", {"prices": prices(d, 14), "ACU": grab(d, r"ACU[^.]{0,90}")})

ki = text("kiro-pricing.html")
show("AWS Kiro", {"prices": prices(ki, 12), "credits": grab(ki, r"\d[\d,]*\s*credits[^.]{0,60}")})

show("Replit", {"prices": prices(text("replit-pricing.html"), 12),
                "Core": grab(text("replit-pricing.html"), r"Core[^.]{0,80}\$\s?\d+")})
show("Augment", {"prices": prices(text("augment-pricing.html"), 12),
                 "tiers": grab(text("augment-pricing.html"), r"(?:Cosmos|Indie|Standard)[^.]{0,90}")})
show("Mistral", {"prices": prices(text("mistral-pricing.html"), 12),
                 "Pro": grab(text("mistral-pricing.html"), r"Pro[^.]{0,80}\$\s?\d+")})
show("Factory Droid", {"prices": prices(text("factory-pricing.html"), 14),
                       "tiers": grab(text("factory-pricing.html"), r"(?:Pro|Plus|Max)[^.]{0,90}")})
show("Zed", {"prices": prices(text("zed-pricing.html"), 12),
             "Pro": grab(text("zed-pricing.html"), r"Pro[^.]{0,80}\$\s?\d+")})
show("Warp", {"prices": prices(text("warp-pricing.html"), 12),
              "Build": grab(text("warp-pricing.html"), r"Build[^.]{0,80}\$\s?\d+")})
show("Amp (Sourcegraph)", {"prices": prices(text("amp-pricing.html"), 12),
                           "orbs": grab(text("amp-pricing.html"), r"orb[^.]{0,90}")})
show("JetBrains AI", {"prices": prices(text("jetbrains-ai.html"), 12),
                      "credits": grab(text("jetbrains-ai.html"), r"credits?[^.]{0,80}")})
x = text("xai-news.html") + text("xai-grok-pricing.html")
show("xAI", {"prices": prices(x, 14), "SuperGrok": grab(x, r"SuperGrok[^.]{0,100}")})
show("DeepSeek API", {"models": ", ".join(list(dict.fromkeys(re.findall(r"deepseek-[a-z0-9.\-]+", text("deepseek-pricing.html"), re.I)))[:8]),
                      "prices": prices(text("deepseek-pricing.html"), 16)})
oc = text("opencode-go.html")
show("OpenCode Go", {"Go": grab(oc, r"Go\s*\$\s?\d+\s*/\s*month"), "Go Plus": grab(oc, r"Go Plus\s*\$\s?\d+\s*/\s*month"),
                     "window rule": grab(oc, r"5-hour[^.]{0,80}")})
cc = text("commandcode-pricing.html")
show("Command Code", {"prices": ", ".join(list(dict.fromkeys(re.findall(r"\$\s?\d+\s*/\s*month", cc)))[:8]),
                      "credits": ", ".join(list(dict.fromkeys(re.findall(r"\$\s?\d+\s+in credits", cc)))[:8])})
