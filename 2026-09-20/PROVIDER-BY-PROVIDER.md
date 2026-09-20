# Provider-by-provider study: all four universes

**Date 2026-09-20.** Pins: `Wei-Shaw/sub2api` `19794bc46afb`,
`router-for-me/CLIProxyAPI` `61fdfc341b96`, `talaria0101/coding-subs`
`8a229936ce7d` (the 2026-09-13 pass).

This file exists because the earlier relay pass asked the wrong question. It
searched three artifacts for the literal string `command code`, found nothing,
and reported absence. That is a **find-the-string** method: it can confirm a
provider that somebody already named, and it can never rule one out. The
correct method is to **enumerate the category and then check each member**, which
is what this file does.

The concrete failure it corrects: **Command Code** (`commandcode.ai`) — a coding
agent for open models, shipping 357 releases, claiming 100K+ developers and 40K+
paid customers, with a published subscription ladder — appears in **none** of
sub2api, CLIProxyAPI, or the 2026-09-13 pass. **Open Interpreter** is absent
too. The root cause is structural, and worth stating plainly: the two repos are
*gateways*, so a coding agent reaches them only as a **client**, never as an
upstream provider; and the 2026-09-13 pass enumerated **coding plans** from a
fixed reading list that never queried the agent market. Neither source could
have surfaced Command Code by construction.

---

## 1. Universe A — `Wei-Shaw/sub2api` (gateway)

Three distinct layers, only the first two code-grounded.

### 1.1 First-class platforms (11)
From `backend/internal/domain/constants.go:20-35`:

| platform | note |
|---|---|
| `anthropic` | |
| `openai` | |
| `gemini` | |
| `antigravity` | Google Antigravity |
| `grok` | xAI |
| `kimi` | Moonshot (OpenAI-compatible via gateway) |
| `zhipu` | GLM (bigmodel) |
| `deepseek` | |
| `minimax` | |
| `opencode_go` | OpenCode; account modes `zen` (PAYG) / `go` (subscription) |
| `composite` | routing pseudo-platform |

### 1.2 Account types (6)
`constants.go:55-63`: `oauth`, `setup-token`, `apikey`, `upstream` (BYO base URL),
`bedrock` (SigV4), `service_account` (Vertex). The `upstream` type is why an
OpenAI- or Anthropic-compatible vendor such as Command Code's API plan is
proxyable without a code change.

### 1.3 Sponsors (26 commercial providers)
Read from `README.md` §Sponsors. These are **advertisements**, not verified rate
cards; only a provider's own published card is VERIFIED.

| provider | host | grade |
|---|---|---|
| CCTK.AI | cctk.ai | ADVERTISED |
| OpenModel | openmodel.ai | ADVERTISED |
| ETok | etok.ai | ADVERTISED |
| APIKEY.FUN | apikey.fan | ADVERTISED |
| AIGoCode | aigocode.com | ADVERTISED |
| CodexEverywhere | codex-everywhere.com | ADVERTISED |
| BmoPlus | shop.bmoplus.com | ADVERTISED |
| Pateway | pateway.ai | ADVERTISED |
| PPToken | api.pptoken.cc | ADVERTISED |
| Aimzoon | aimzoon.com | ADVERTISED |
| Nagora | nagora.ai | ADVERTISED |
| Qiniu AI | qiniu.com (02567.HK) | ADVERTISED |
| FennoAI | api.fenno.ai | ADVERTISED |
| LanoX | lanox.ai | ADVERTISED |
| hao.ai | hao.ai | ADVERTISED |
| APIMart | apimart.ai | ADVERTISED |
| PP.dog | pp.dog | ADVERTISED |
| Bestproxy | bestproxy.com | ADVERTISED |
| Veilx | veilx.io | ADVERTISED |
| RoxyBrowser | roxybrowser.com | ADVERTISED |
| Proxy4Free | proxy4free.com | ADVERTISED |
| RapidProxy | rapidproxy | ADVERTISED |
| Swiftproxy | swiftproxy | ADVERTISED |
| DuckIP | duckip | ADVERTISED |
| AxisNow | axisnow | ADVERTISED |
| ColaProxy | colaproxy | ADVERTISED |

### 1.4 Registry (capability only, not a sub2api feature)
`models.dev` fetched 2026-09-20: **222 providers / 7,868 models**. The
`modelsDevModel` struct in sub2api carries **no cost field**
(`service/upstream_models.go:23`), so cost rankings derived from the registry
are analysis of the registry, not of sub2api. See
[data/modelsdev-providers.csv](data/modelsdev-providers.csv).

---

## 2. Universe B — `router-for-me/CLIProxyAPI` (gateway)

### 2.1 Protocol constants
`internal/constant/constant.go:8-29`: `gemini`, `gemini-interactions`, `codex`,
`claude`, `openai`, `openai-response`, `antigravity`, `interactions`.

### 2.2 Auth providers (8 + `empty`)
Directory `internal/auth/`: `antigravity`, `claude`, `codex`, `devin`, `kimi`,
`meta`, `vertex`, `xai` (+ `empty` placeholder). The README advertises only
**5** — Anthropic, Antigravity, Kimi, OpenAI, xAI — so the code supports 8.

### 2.3 Model registry
`internal/registry/models/models.json`: 13 tiers / **135 models** (`claude` 16,
`gemini` 14, `vertex` 21, `gemini-cli` 7, `aistudio` 16, `codex-free` 4,
`codex-team` 6, `codex-plus` 7, `codex-pro` 7, `kimi` 10, `antigravity` 12,
`xai` 10, `meta` 5).

### 2.4 Sponsors (7)
`README.md` §Sponsor: **PackyCode, AICodeMirror, APIKEY.FUN, Qiniu Cloud AI,
Cubence, APIMart, Aiberm**. Supporters (not sponsors): FluxA & Baidu AI Cloud,
Kimi.

---

## 3. Universe C — talaria's 2026-09-13 pass (26 groups / 44 plans)

| group | plans | price range (USD/mo) |
|---|---|---|
| Z.ai | GLM Coding Plan Lite / Pro / Max | 18 / 72 / 160 |
| MiniMax | Token Plan Plus / Max / Ultra | 22 / 55 / 132 |
| Moonshot AI | Kimi Code Moderato / Allegretto / Allegro / Vivace | 19 / 39 / 99 / 199 |
| Meta | Muse Code (3 tiers); Muse consumer promo | ~20–100; 0–20 |
| OpenAI | Codex in ChatGPT Plus / Pro | 20 / 100 / 200 |
| Anthropic | Claude Pro / Max 5× / Max 20× | 20 / 100 / 200 |
| Google | Antigravity free; AI Pro; AI Ultra 5× / 20× | 0 / 19.99 / 100 / 200 |
| GitHub | Copilot Pro / Pro+ / Max | 10 / 39 / 100 |
| Alibaba Cloud | Model Studio Coding Plan Pro | 50 |
| ByteDance | Trae Lite / Pro | 3 / 10 |
| Kilo Code (Anaconda) | Kilo Pass Starter | 19 |
| Cline | open source | 0 |
| Roo Code | Roo / Roomote | 0+ |
| OpenCode | OpenCode + Zen | 0 + PAYG |
| Cursor | Cursor Pro / Ultra | 20 / 200 |
| Windsurf→Cognition | Devin Desktop (ex-Windsurf) | UNKNOWN |
| Cognition | Devin (team) | UNKNOWN |
| AWS | Kiro Pro | 20 |
| Replit | Replit Core | 20 |
| Augment | Augment Standard | 20 |
| Mistral | Le Chat Pro + Vibe | 14.99 |
| Abacus.AI | ChatLLM Teams | 10 |
| Tencent | CodeBuddy | UNKNOWN |
| Sino-agg | Alibaba iFlow CLI | 0 |
| Proxy | Z.ai on Tmall | RMB |
| Resellers | third-party top-up resellers | varies |

---

## 4. Universe D — the agent/harness market (the gap)

This is the universe that neither repo could contain (agents are clients to a
gateway) and that the 2026-09-13 pass did not query. Machine-readable:
[data/agents-universe.csv](data/agents-universe.csv). Cross-check used
**product-context patterns**, not bare tokens — a bare `cursor` matches 136
pagination cursors in sub2api, and a bare `continue` matches the Go keyword 557
times, which is precisely how the earlier pass fooled itself.

### 4.1 The missed leader — Command Code
Own pricing page, fetched 2026-09-20 → [sources/agents/commandcode-pricing.txt](sources/agents/commandcode-pricing.txt).
**VERIFIED (vendor's own page); not independently verified.**

| plan | price/mo | monthly credits | claimed usage with deals | request volume |
|---|---|---|---|---|
| Go | $1 | $10 | up to ~$20 | ~15K |
| GOAT | $10 | $70 | up to ~$100 | ~75K |
| Pro | $20 | $80 | up to ~$80 (+premium models) | ~100K |
| Max 10× | $100 | $150 | up to ~$300 | ~219K |
| Max 20× | $200 | $300 | up to ~$600 | ~437K |
| API plan | $15 + PAYG | — | zero markup | OpenAI/Anthropic endpoints |
| Teams | $40 | pooled | — | ~35K |
| Enterprise | custom | — | — | — |

Product claims (ADVERTISED, unverified): "best coding agent for open models",
taste-1 meta-model, 99%+ cache-hit rates, tool-call repairs, "zero markup" on
top-ups via the API plan. Notable structural fact: **open-source models route
globally (US/EU/Singapore); commercial models are hosted by Anthropic, OpenAI,
Google and Azure.** Pricing is sold only direct, no resellers.

### 4.2 Every other agent, checked

| product | in sub2api | in CLIProxyAPI | in 2026-09-13 | monetization |
|---|---|---|---|---|
| Command Code | no | no | **no** | subscription $1–$200 + API $15 |
| Open Interpreter | no | no | **no** | open source, BYOK |
| OpenCode | yes | yes | yes | Zen PAYG / Go subscription |
| Claude Code | yes | yes | yes | bundled with Claude Pro/Max |
| Codex CLI | yes | yes | yes | bundled with ChatGPT |
| Gemini CLI | yes | yes | yes | free + Google AI Pro |
| Cline | partial | yes | yes | BYOK / ClinePass |
| Roo Code | no | yes | yes | BYOK |
| Kilo Code | no | no | yes | Kilo Pass $19 |
| Cursor | no | no | yes | Pro $20 / Ultra $200 |
| Kiro | yes | yes | yes | Pro $20 |
| Trae | no | yes | yes | Lite $3 / Pro $10 |
| Augment Code | no | yes | yes | Standard $20 |
| CodeBuddy | yes | yes | yes | credits (UNKNOWN) |
| Devin / Windsurf | no | yes | yes | UNKNOWN 2026 tiers |
| Muse Code | no | yes | yes | ~$20–$100 |
| Aider | no | no | **no** | open source, BYOK |
| Continue | no | no | **no** | open source, BYOK |
| Goose | no | no | **no** | open source, BYOK |
| Charm Crush | no | no | **no** | open source, BYOK |
| Amp | no | partial | **no** | free + PAYG (UNKNOWN) |
| Factory Droid | no | yes | **no** | subscription (UNKNOWN) |
| OpenHands | no | partial | **no** | open source, BYOK |
| Plandex | no | no | **no** | open source, BYOK |
| Tabby | no | no | **no** | self-host / BYOK |
| Zed | no | partial | **no** | free + subscription |
| Warp | no | no | **no** | subscription |
| Qwen Code | no | no | **no** | free with Qwen account |
| CodeWhale | no | no | **no** | open source, BYOK |
| DeepSeek-Reasonix | no | no | **no** | BYOK |
| Qoder | no | no | partial | time-of-day credits |
| Pochi / Codebuff / Sweep | no | no | **no** | UNKNOWN / PAYG |

---

## 5. Reconciliation

| universe | members |
|---|---|
| sub2api platforms | 11 |
| sub2api sponsors | 26 |
| CLIProxyAPI auth providers | 8 |
| CLIProxyAPI sponsors | 7 |
| talaria 2026-09-13 groups | 26 |
| **agent/harness market** | **30 checked; 18 absent from all three sources** |

The provider union of the two repos remains 72
([data/providers-union.csv](data/providers-union.csv)); this file adds the
agent market as a fourth, disjoint universe, and flags the 18 agents that no
source contained — **Command Code and Open Interpreter first among them.**

---

## 6. What this did NOT establish

- Command Code's prices and usage claims are its **own** published page, read
  once on 2026-09-20. No token was served, no invoice seen. The "zero markup",
  "up to 2×/5× effective usage" and "99%+ cache hit" are advertising.
- The agent cross-check distinguishes **present as a supported client** from
  **absent**. A `partial` entry means one product-context hit, not a supported
  integration.
- The 2026-09-13 price/plan rows are unchanged from that pass and carry its
  labels (VERIFIED / MIXED / UNKNOWN) — this file re-presents, it does not
  re-verify them.
- This is a category enumeration, not a census: an agent with no GitHub presence,
  no vendor page and no mention in any source would still be missed. The method
  is strictly better than a string search; it is not exhaustive.
