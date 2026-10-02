# coding-subs — 2026-10-02 pass

**Research date 2026-10-02 (UTC).** Fresh first-party re-fetch of every source the 2026-09-20 pass
used, plus a new class of evidence: *metered* measurements of what a subscription's allowance is
actually worth. This pass also integrates the two open issues in the upstream repository
([#1](https://github.com/talaria0101/coding-subs/issues/1) additional sources,
[#2](https://github.com/talaria0101/coding-subs/issues/2) adjusted/real usage) as an
evidence-evaluation appendix rather than as adopted facts.

Databases: [data/first-party-plans.csv](data/first-party-plans.csv) (58 plans, 28 provider groups),
[data/cost-per-usable-token.csv](data/cost-per-usable-token.csv) (published ceilings converted to
$/M tokens), [data/subscription-multipliers.csv](data/subscription-multipliers.csv) (metered
multipliers), [data/free-tier-index.csv](data/free-tier-index.csv) (34 free surfaces),
[data/models-database.csv](data/models-database.csv) (22 models with a 2026-10-02 AA snapshot).
Citations: [references/references.md](references/references.md). Raw snapshots:
[sources/](sources/). Review: [docs/reviews-2026-10-02.md](../../docs/reviews-2026-10-02.md).

## BEST DEAL FOUND (short answer)

| Question | Answer | Evidence class |
|---|---|---|
| Cheapest large allowance per dollar | **Z.ai GLM Coding Plan Lite — $18/mo, up to 1,264M GLM-5.3-Flash tokens/month off-peak (632M peak-billed).** Campaign extended to 2026-10-07. | DOCUMENTED (first-party credit table) |
| Best measured value per dollar | **SuperGrok — $30/mo buys ≈190× its price in Grok 4.7 API usage at the weekly meter (≈$5,700 list).** | MEASURED (third-party meter study) |
| Best *verified token price* | **OpenCode Go — $10/mo, up to $60/month of list-value usage on open models; MiMo-V2.6-Flash works out to ~$0.0013/M token.** | DOCUMENTED (first-party per-model grid) |
| Best free entry that needs no card | **NVIDIA NIM (40 RPM on 100+ models, incl. DeepSeek V4.1 Flash and GLM-5.3), Gemini API free tier, Groq free plan.** | THIRD-PARTY-VERIFIED (dated) |
| Best free coding agent without a paid plan | **Cline / Aider (BYOK), Kiro Free (50 credits/month), Gemini CLI free tier (1,000 requests/day).** | THIRD-PARTY-VERIFIED (dated) |

The July–September ranking favourite (GLM Lite at the top of *capacity*) now has a serious
competitor that is priced in the same bracket: **OpenCode Go at $10 publishes a per-model dollar
ceiling grid**, which is the only first-party document in this market that lets a reader compute
cost-per-token without assuming a cache-hit rate.

## What changed since 2026-09-20 (12 days)

| Provider | Change | Source |
|---|---|---|
| Z.ai | GLM-5.3-Flash campaign **extended from Sep 20 to Oct 7** (was: ends 2026-09-20). Between 23:00–09:00 SGT, ZCode/AutoClaw use consumes **zero** quota, other agents get **doubled** quota. | [sources/zai-glm53-flash-campaign.md](sources/zai-glm53-flash-campaign.md) |
| Z.ai | **All-day off-peak pricing** (50% credit rate) from **Sep 25 to Oct 7, 2026** — the published "estimated token allowance" table's *maximum* column is now the default for that window. | [sources/zai-glm-coding-plan-overview.md](sources/zai-glm-coding-plan-overview.md) |
| Z.ai | **Team Plan published**: Standard seat 15,000 5h / 66,000 weekly credits, Premium seat 35,000 / 155,000; overage at 10% off API list; **seat price still unpublished** (UNKNOWN). | [sources/zai-teamplan.md](sources/zai-teamplan.md) |
| Anthropic | **Claude Opus 5.5** (2026-09-22) II **57.62** and **Claude Sonnet 5.5** (2026-09-28) II **55.98** — the AA frontier moved up ~4 points in five days. | [sources/aa-models-page.html](sources/aa-models-page.html) |
| Google | **Gemini 4 Argon (high)** at II **52.56** in the AA top list (2026-09-30). | aa-models-page.html |
| OpenAI | **GPT-6.1 Sol** (2026-09-29) II 51.83; **GPT-6 Luna** (2026-09-22) II 38.12 at **$0.10/$0.50** — the cheapest frontier-adjacent model in the table. | aa-models-page.html |
| OpenCode | **OpenCode Go restructured**: now a **per-model monthly dollar ceiling grid** ($15–$240 for Go, up to $240 across Go Plus), with 5h = 20%, weekly = 50%, monthly = 100% of each ceiling. Go Plus ($40/mo) added. | [sources/opencode-go.html](sources/opencode-go.html) |
| Command Code | Deals **reduced**: Go effective usage ~$20 → ~$15; GOAT ~$50 → ~$60 range restated; page now lists "processing fee" per plan. | [sources/commandcode-pricing.html](sources/commandcode-pricing.html) |
| Meta | Muse Code plan names confirmed first-party as **Everyday ($5) / High Usage ($15) / Power ($50)**, with High = 5× and Power = 20× Everyday; **Meta still publishes no prices on the docs page**. | [sources/meta-muse-subscriptions.md](sources/meta-muse-subscriptions.md) |
| MiniMax | Token Plan **unchanged** ($22/$55/$132) and the published quota is still *a usage bar*, not a token figure; Credits overflow at **1,000 credits = $1**. | [sources/minimax-token-plan-pricing.md](sources/minimax-token-plan-pricing.md) |
| Models.dev registry | 225 providers (+3), 8,359 models (+490 in 12 days); new provider ids `bee`, `pareto`, `tempr`. | modelsdev-api.json diff |

Twelve days, and the top of the market moved: **every frontier lab shipped a new flagship**, and
the cheap end of the open-model market got a documented price grid instead of marketing.

## Fresh research: measured subscription multipliers

The upstream issue [#2](https://github.com/talaria0101/coding-subs/issues/2) asks for *adjusted / real*
usage. This pass evaluated the two repos offered there and adopts one class of evidence from them:
**metered multipliers**, where a plan's own usage meter is ticked on purpose and every call is
priced at the vendor's public API rate. That is a stronger claim than "published quota × 4.33 weeks"
because it measures the vendor's own accounting, not its marketing table.

| Plan | Price | Multiplier | Model measured | Class |
|---|---|---|---|---|
| SuperGrok | $30 | **190× ± 21** | Grok 4.7 | MEASURED |
| Muse Code Power (contributor, vs standard API price) | $50 | *137× ± 15* | Spark 1.3 contributor | DERIVED |
| Muse Code High (contributor, vs standard API price) | $15 | **114× ± 12** | Spark 1.3 contributor | MEASURED |
| Claude Max 20x | $200 | **45.3× ± 1.0** | Opus 5.5 | MEASURED |
| Muse Code Power (standard) | $50 | *11.1× ± 0.5* | Spark 1.3 standard | DERIVED |
| ChatGPT Pro $100 (Codex) | $100 | **10.25× ± 0.03** | GPT-6.1 Sol | MEASURED |
| Muse Code High (standard) | $15 | **9.3× ± 0.4** | Spark 1.3 standard | MEASURED |

Full table with method and uncertainty: [data/subscription-multipliers.csv](data/subscription-multipliers.csv).

**What this does to the rankings.** On the 2026-09-20 numbers GLM Lite looked like the best deal in
the market because it publishes the largest *token* table. The metered numbers say that is a
publishing choice, not a generosity one: a $30 SuperGrok buys more Grok 4.7 at list price than the
entire GLM Max plan's published ceiling is worth, and a $15 Muse Code plan measured at ~13B
tokens/week. The honest read is that **capacity tables and meters measure different things**, and
a pass that only has the former should say so.

**What this pass did not establish.** The meter study is by a third party, covers four plans, one
workload each, and was measured on 2026-10-01 through vendor clients whose logs are not in this
repo. It does not measure OpenAI's or Anthropic's *token* ceilings — it measures what one percent of
a week was worth on the day. Treat every row as "for this kind of work, on that day".

## Cost per usable token — the 2026-10-02 table

Published ceilings converted to a single comparable figure. HIGH = first-party published table;
THIRD-PARTY = a study we did not run; UNKNOWN = never published.

| Plan | Price/mo | Ceiling (tokens/mo) | $/M tokens | Confidence |
|---|---|---|---|---|
| GLM Lite (GLM-5.3-Flash, off-peak) | $18 | 1,264M | **$0.014** | HIGH |
| GLM Max (GLM-5.3-Flash, off-peak) | $160 | 17,731M | **$0.009** | HIGH |
| GLM Pro (GLM-5.3-Flash, off-peak) | $72 | 7,598M | $0.009 | HIGH |
| OpenCode Go (MiMo-V2.6-Flash ceiling) | $10 | 7,878M | **$0.0013** | MEDIUM (per-model grid) |
| OpenCode Go Plus (MiMo-V2.6-Flash ceiling) | $40 | 15,756M | $0.0025 | MEDIUM |
| Command Code GOAT (DeepSeek V4.1 Flash allowance) | $10 | 6,211M | $0.0016 | MEDIUM |
| MiniMax Ultra | $132 | 9,800M | $0.013 | THIRD-PARTY |
| MiniMax Max | $55 | 5,100M | $0.011 | THIRD-PARTY |
| MiniMax Plus | $22 | 1,700M | $0.013 | THIRD-PARTY |
| GLM Lite (GLM-5.3, off-peak) | $18 | 420M | $0.043 | HIGH |
| ChatGPT Plus (Codex, GPT-6.1 Sol) | $20 | 870M | $0.023 | THIRD-PARTY |
| Claude Pro (Opus 5.5) | $20 | 3,054M | $0.0066 | THIRD-PARTY |

Two things to read carefully. First, the per-model ceilings on OpenCode Go and Command Code GOAT are
**per model** — a reader gets that ceiling on one model, not the sum, which is why the "best model"
column is named. Second, the third-party Claude and MiniMax token figures are *saturated-use*
back-calculations; using half the allowance doubles the real price.

## Workload test — 52.5M tokens/month (15M in + 37.5M out)

The same workload the 2026-09-20 pass used, repriced against the 2026-10-02 model table. This is
the *list-price* cost of the workload; a plan passes if its published ceiling covers it.

| Model | List cost of 52.5M | Cheapest published plan that covers it |
|---|---|---|
| GPT-6 Luna | $20.25 | ChatGPT Plus ($20, message-metered) |
| GLM-5.3-Flash | $21.00 | GLM Lite ($18, 632M+ tokens) |
| DeepSeek V4.1 Flash | $49.50 | OpenCode Go ($10 holds $60 ceiling on it) |
| Step 5 | $91.80 | OpenCode Go ($15 ceiling) or GLM Lite |
| Gemini 3.8 Flash | $151.88 | GLM Lite ($18, but only via Flash) / Google AI Pro ($19.99) |
| GLM-5.3 | $186.00 | GLM Lite ($18, 208–420M ceiling — **PASS**) |
| Muse Spark 1.3 | $178.12 | Muse Code High ($15) |
| Kimi K3 | $607.50 | none under $50 verified — OpenCode Go's K3 ceiling is $15 of list value |
| Claude Opus 5.5 | $810.00 | Claude Max territory |
| GPT-6 Astra / Fable 5.1 | $2,025.00 | no published allowance covers this at any tier |

## Hourly view (for agent runtimes that are not on 24×7)

A plan ceiling is a monthly number; an agent runtime runs hours. Using one **heavy agent hour =
1M input + 2M output tokens (3M tokens)** as the unit:

| Plan | Ceiling used | Heavy hours/month | Hours/day if spread over 30 days |
|---|---|---|---|
| GLM Lite (Flash, off-peak) | 1,264M | 421 | **14.0 hrs/day** |
| GLM Lite (GLM-5.3, off-peak) | 420M | 140 | 4.7 hrs/day |
| OpenCode Go (MiMo-V2.6-Flash $60 ceiling) | ~$60 of list value | ≈14,700M at that model's price | essentially unbounded by hour |
| MiniMax Plus | 1,700M | 566 | 18.9 hrs/day |
| ChatGPT Plus (GPT-6 Luna) | ≈9.2B | 3,067 | saturating the month |

This is the number the 2026-09-20 pass did not publish: **the cheapest plans in this market cover
a 10-hours-a-day agent, and the expensive ones cover a 10-hours-a-day agent on a frontier model**.
The scarce resource is not hours, it is *which model the hours run on*.

## Free tiers, re-verified

34 free surfaces are indexed in [data/free-tier-index.csv](data/free-tier-index.csv). The ones that
matter for a coding agent, and what the sources actually say:

- **NVIDIA NIM** — 100+ models free at 40 RPM site-wide, no card. A 2026-09-27 re-read shows the
  lineup *rotating*: `deepseek-ai/deepseek-v4.1-flash` and `z-ai/glm-5.3` were **added**, while
  `deepseek-v4-flash-0731`, `deepseek-v4-pro-0813` and **every MiniMax entry were delisted** —
  the model count stayed at 82 while the lineup changed. An unchanged count is not an unchanged
  catalogue.
- **Gemini API free tier** — free models include Gemini 3.8 Flash and Gemma 4, but **Gemini 3.1 Pro
  Preview is paid only**, and Google's own table marks free-tier use as "used to improve our
  products".
- **Groq** — free plan limited to gpt-oss-120b/20b and Qwen3.8 27B; **Llama 3.3 70B left the free
  and developer plans on 2026-08-16**.
- **Mistral** — the old ~1B-tokens/month free API tier is **gone** (discontinued 2026-09-01); what
  remains is $10/month of credits behind the paid plan.
- **GitHub Models was retired on 2026-07-30.** Any list still recommending it is stale.
- **Ollama Cloud's free plan has never published its allowance or its starter model list**, and all
  20 catalog models carry a price. It is listed as cautionary, not as a free tier.
- **Vercel AI Gateway** gives $5/month but **requires a payment method on file**, and buying credits
  permanently voids the monthly free credit.
- **Experiential Labs** was giving away Claude Fable 5.1 and GPT-6 Astra at $0 in/out under a
  ~500-credit/month cap; its own measurements show **72.5% uptime** on the Fable path. Free, and
  not production.

## Where the two issues landed

**Issue #1 (additional sources).** All four suggested repos were fetched, read and kept as dated
snapshots under `sources/thirdparty-*`. Only one of them contributes anything this repo did not
already have, and it contributes a lot: `FeiZhuLulu/real-api-pricing` publishes a
**real-$/M-token table built from saturated-use measurements** for ~100 plans across Claude, ChatGPT,
GLM, MiniMax, Kimi, Cursor, Devin, Factory and more. It is CC-BY-compatible (MIT repo, sources
credited upstream) and its rows are the basis of the third-party column in
[data/cost-per-usable-token.csv](data/cost-per-usable-token.csv). The other three are useful in a
different way — they are *free-tier* catalogues, and the value they add is not pricing but the
**dated-verification discipline**; that discipline is what this pass adopts for
[data/free-tier-index.csv](data/free-tier-index.csv).

**Issue #2 (adjusted/real usage).** `phuryn/experiments` is the source of the metered multipliers
above, and `real-api-pricing` is the source of the saturated-use token figures. This pass adopts
their *numbers* with attribution and, more importantly, adopts their **evidence classes**:
MEASURED (a meter was ticked) is a different and stronger class than DOCUMENTED (a vendor published
a table), and both are different from ADVERTISED. Ranking the market without that distinction is
what produced the "GLM is the best deal" consensus that the meters now contradict.

## What would falsify this pass

- A first-party page showing GLM Lite's ceiling is not usable at the published rate (e.g. the
  campaign ends and the off-peak table is withdrawn on 2026-10-08) — the census above says so
  explicitly with an expiry date.
- A metered repeat on GLM Lite and OpenCode Go on a comparable workload. Until that exists, the
  GLM and OpenCode rows are published-ceiling claims and the SuperGrok/Claude/Muse rows are meter
  claims; they are not the same kind of statement.
- A Command Code page revert: the effective-usage numbers on the 2026-10-02 page are lower than the
  2026-09-20 page, which is itself a falsification of the 09-20 "BEST VALUE" line.

## Known gaps

- Z.ai Team Plan seat **price** is unpublished — a KNOWN UNKNOWN, deliberately not estimated.
- MiniMax's quota is a console bar; no token figure exists to convert.
- Kimi's new membership ladder is JS-paywalled; only the *structure* is first-party.
- Claude Max 5x/20x weekly ratio is still not published by Anthropic, so the Max token rows are
  derived from third-party saturation figures and must not be read as ceilings.
- The meter study covers four plans. SuperGrok, Claude Max, ChatGPT Pro and Muse Code are measured;
  GLM, OpenCode, MiniMax, Command Code, Cursor, Devin and the rest are not.
- No throughput/latency measurement was taken in this pass; every availability figure in the free
  index is quoted from a source, not measured here.
