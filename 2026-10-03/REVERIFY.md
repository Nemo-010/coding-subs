# Source-by-source re-verification — 2026-10-03

Every first-party source was fetched **serially, one at a time**, on 2026-10-03: 55 URLs,
53 clean, 2 refused (both OpenAI, HTTP 403 to this vantage point). The fetch log with
http / bytes / ms / sha256 per source is `data/fetch-log.json`; the raw bytes are in
`sources/`. `tools/fetch-all-2026-10-03.py` is the fetcher, `tools/extract-2026-10-03.py`
the per-provider extraction and `tools/compare-2026-10-03.py` the old-vs-new comparison.

This file is the record of **what each provider's own page says today versus what the
2026-10-02 table claimed**. Where a page changed, the row changed. Where a page confirms
the old row, that is stated as a confirmation, not padded out as news.

## Drift found — new plans that did not exist in the previous table

| Provider | What the live page says now | What the 2026-10-02 table had |
|---|---|---|
| **Cursor** | `Hobby $0 / Pro $20 / Pro+ $60 / Ultra $200 / Teams $40 per user` (read from the page's own schema.org `Offer` block) | Pro $20 and Ultra $200 only — **Pro+ $60 was missing** |
| **Google** | `AI Plus $4.99` (2x) / `AI Pro $19.99` (4x) / `AI Ultra from $99.99` (5x) and `$199.99` (20x) | Plus tier absent; Ultra shown as flat $100/$200 |
| **AWS Kiro** | `Free $0 / Pro $20 / Pro+ $40 / Pro Max $100 / Power $200` (schema.org `Offer` block) | **only "Kiro Pro $20"** — four tiers missing |
| **Meta Muse Code** | **three** plans: `Everyday Usage` (10-50 prompts/5h), `High Usage` (5x), `Power Usage` (20x); **no prices published on the page at all** | only "Muse Code High Usage $15"; the base tier and the price provenance are both unstated |
| **Cognition Devin** | `Pro $20` (frontier models incl. "SpaceXAI"), `Max $200` (new), `Teams $80 + $40/dev seat` | Pro/Max/Teams present; Max's "new" marker and the frontier-model list are new |

## Drift found — corrections to figures the table stated

| Provider | Live figure | Table had | Nature |
|---|---|---|---|
| **Google AI Pro** | `$19.99/mo` (US locale) | `$19.99` | confirmed — but the earlier pass fetched a **Spanish-locale** page (see vantage note) |
| **Anthropic Pro** | `$17/mo annual ($200 up front) / $20 monthly` | `20 (17 annual)` | **confirmed exactly** |
| **Anthropic Max** | `From $100` (5x), 20x at `$200` | `$100` / `$200` | confirmed; "from $100" framing is new |
| **GitHub Copilot** | `Pro $10 (base 1,000) / Pro+ $39 (base 3,900) / Max $100 (base 10,000)` | same prices; table also carried flex-credit totals | prices confirmed; the live page states **base** credits, not base+flex |
| **Z.ai** | `Lite 2,000/10,000 · Pro 12,000/60,000 · Max 28,000/140,000`; `from $18/mo` | identical | **confirmed** |
| **Z.ai Team** | `Standard 15,000/66,000 · Premium 35,000/155,000` | identical | **confirmed**; seat price still not published |
| **MiniMax** | `Plus $22 / Max $55 / Ultra $132`; H3/voice excluded | identical | **confirmed exactly** |
| **xAI** | `$100/$20/$6/$25` tokens and API rates present | SuperGrok ladder | prices present; **SuperGrok subscription tiers still not on a first-party price page** |
| **DeepSeek** | `V4.1-Flash off-peak $0.15/$0.60, peak $0.30/$1.20`; V4-Pro and V4-Flash-Vision-Exp listed | same | **confirmed**; two new model slugs on the page |
| **Command Code** | `Go $1 / GOAT $10 / Pro $20 / Max 10x $100 / Max 20x $200`; credits `$10/$70/$80/$150/$300` | identical | **confirmed** |
| **Trae** | `Free $0 / Pro $20 / Pro+ $60 / Ultra $200` | identical | **confirmed** |
| **Warp** | `Build $20 (1,500 credits) / Max $200 (18,000 credits)` | Build $20, Max $200 | prices confirmed; **credit counts are new detail** |
| **Factory** | `Pro $20 / Plus $100 / Max $200` | identical | **confirmed** |
| **Replit** | `Core $20 / $18 annual` | `20 (18 annual)` | **confirmed** |
| **Zed** | `Pro $10 incl. $5 tokens; Business $30/seat` | Pro $10, $5 tokens | confirmed; Business tier exists |
| **Amp** | `Individual $20, 45,000 orb-minutes; Hobby free` | same | **confirmed** |
| **Mistral** | `Pro $14.99; $10/mo API credits` | `14.99` | **confirmed** |

## Sources that confirm the previous pass rather than change it

Z.ai (all five pages), MiniMax, Command Code, Trae, Factory, Replit, Zed, Amp, Mistral,
DeepSeek, Warp's prices, GitHub's prices, Anthropic's prices. Reading a page and finding it
unchanged is the most common outcome of this pass and is reported as such.

## What this pass could not establish

- **OpenAI is unreadable from here.** `developers.openai.com/codex/pricing.md` and
  `openai.com/chatgpt/pricing/` both return **HTTP 403** to this sandbox. The two OpenAI
  rows (Codex in ChatGPT Plus / Pro) are therefore **carried forward from 2026-10-02
  without re-verification**, and this file says so rather than implying a check that did
  not happen.
- **Google serves a locale-shifted page** without an explicit `gl=us`. The first fetch
  returned Spanish and no USD figures. A second fetch with `?hl=en&gl=us` gave the real
  prices, which are the ones used. This is a vantage-point artefact, not vendor behaviour.
- **x.ai/news returned 200** this time (it was 403 on 2026-10-02), but the SuperGrok
  subscription ladder still is not on a first-party *price* page — the API rates are.
- **No authenticated plan was tested.** Prices are list prices read from pages.

## Counts

- Sources fetched: **55** (53 OK, 2 × HTTP 403)
- Providers re-verified against a live first-party page: **26 of 28**
- Providers not re-verifiable from this sandbox: **2** (OpenAI ×2 rows — 403)
- Rows changed as a result: **5 new-plan rows added** (Cursor Pro+, Google AI Plus, Kiro
  Pro+/Max/Power, Meta Everyday, Devin Max), **1 correction** (Meta Muse: price withdrawn
  as unverifiable, tiers restated)
