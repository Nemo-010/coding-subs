# The Cheapest Frontier Coding-Agent Usage — Market Research, September 2026

**Research date: 2026-09-13 (UTC).** All prices/quotas verified against live sources on this date;
everything older or second-hand is labeled. Databases: [data/models-database.csv](data/models-database.csv)
(45 models) and [data/providers-database.csv](data/providers-database.csv) (44 access plans).
Numbered citations: [references/references.md](references/references.md). Raw source snapshots:
[sources/](sources/).

Brief context: the original task spec said "August 2026"; system and remote time servers both
read **September 13, 2026**, and every claim below is current as of that date.

---

## BEST DEAL FOUND (concise answer)

| Field | Value |
|---|---|
| **BEST DEAL FOUND** | **Z.ai GLM Coding Plan — Lite tier** |
| **PRICE** | **$18/month** ($9/mo for legacy-plan migrants at 50% off; $172.80/yr ≈ $14.40/mo equivalent) |
| **CODING TOOL** | Any Anthropic-compatible agent: Claude Code, OpenCode, Cline, Roo Code, Kilo Code, Codex, Goose, ZCode |
| **MODEL** | **GLM-5.3** (AA Intelligence Index **44.9**; Terminal-Bench v4.0 **0.419** — above Claude Opus 4.8's 0.217, near Opus 5-medium) + GLM-5.3-Flash (II 41.9) |
| **CONTEXT** | **1M tokens** at model level; exposed through the coding agents you plug the plan key into |
| **MULTIMODAL** | Partial: GLM-5.3-Flash takes image input; GLM-5.3 is text-only natively but every plan bundles a Vision MCP server (routes to GLM vision models), plus Web Search / Web Reader / Zread MCPs |
| **USAGE** | Official published estimate at 95% cache-hit: **48–97M GLM-5.3 tokens/week** (Lite), and **146–292M tokens/week** on GLM-5.3-Flash; off-peak usage costs 50% credits |
| **ESTIMATED MONTHLY CAPACITY** | **≈ 208–420M GLM-5.3 tokens/month** (Lite), or 632M–1.26B on Flash — vs. your 52.5M/month target |
| **VS CLAUDE PRO** | ≈ **20–40× the practical capacity** at comparable price, on a model that beats Opus 4.8 on agentic-coding benchmarks (but is below Opus 5 / Fable 5.1 / GPT-6 Astra at max effort) |
| **CONFIDENCE** | **HIGH** on price, quota rules, and token-allowance tables (first-party docs, Sep 2026); MEDIUM on real-world sustained throughput (credit multipliers vary by cache-hit rate and time of day) |

The workload test: your target of **500K input + 1.25M output tokens/day (52.5M/month)** fits
inside the Lite tier's *low-end* weekly allowance roughly **4× over** — i.e., Lite alone should
carry your full workload with ~3–4× headroom. If you ever exhaust it, the same key upgrades, or
GLM-5.3-Flash quota (~6× larger) absorbs routine work.

---

## How the market got here (60-second orientation)

- The frontier as of Sep 2026 (AA Intelligence Index, max-effort variants): **Claude Fable 5.1
  53.4 · GPT-6 Astra 52.8 · Claude Opus 5 50.7 · Muse Spark 1.3 48.2 · GPT-5.6 Sol 47.1 ·
  GLM-5.3 44.9 · Grok 4.6 44.4 (500K ctx) · Kimi K3 43.8 · Gemini 3.8 Flash 41.2 ·
  Qwen3.8-Max 40.3**. Claude Opus 5 remains the *value* frontier ($5/$25, 1M ctx); Fable 5.1
  and GPT-6 Astra are the absolute ceiling at $10/$50.
- Google shipped no Gemini 3.8 *Pro* — the Flash line *is* the Gemini flagship now
  (Gemini 3.1 Pro Preview, Feb 2026, sits at II 30.4). Gemini 3.8 Flash is intro-priced at
  $0.75/$3.75 through Dec 31, 2026, then doubles — a time-limited subsidy.
- Meta re-entered frontier models with **Muse Spark** (Superintelligence Labs) and shipped a
  Claude-Code-style terminal agent, **Muse Code**, in Aug/Sep 2026 — with aggressive pricing
  ($1.25/$4.25 API) and a 100M-free-tokens/week consumer promo.
- The "unlimited" era is over in the West: Claude/ChatGPT moved to 5-hour + weekly
  compute-based windows, Cursor/GitHub to usage-metered credits. Chinese labs (Z.ai, MiniMax,
  Moonshot, Alibaba, ByteDance) are the ones still subsidizing fixed-price plans — and Z.ai is
  now the only major lab publishing **official token-allowance tables** for its coding plan.

---

## Top 10 serious options

Ranked by the brief's weighting (30% capacity, 25% quality, 15% 1M-context, 10% multimodal,
10% price, 10% multi-model). Full per-plan data in
[data/providers-database.csv](data/providers-database.csv).

| # | Plan | Price/mo | Best model (II) | Why it's here | Main limitation |
|---|---|---|---|---|---|
| 1 | **Z.ai GLM Coding Plan Lite** | **$18** | GLM-5.3 (44.9) | Officially 208–420M tokens/mo on a 1M-ctx model that beats Opus 4.8 on TB-v4; works in Claude Code | GLM-5.3 not natively multimodal (vision via MCP); below Opus-5-max quality |
| 2 | **Claude Max 5x** | $100 | Opus 5 (50.7) / Fable 5.1 (53.4) | The real Opus-5-class experience; **1M context verified in Claude Code**; +25% weekly limits since Sep 14 | ~5× Pro ≈ 50M+/mo (ESTIMATED); 8× the price of #1 |
| 3 | **ChatGPT Plus (Codex)** | $20 | GPT-5.6 Sol (47.1) | Frontier quality; official message tables (Sol 10–100/5h); community-measured ~$450/mo API-equivalent; flex credits | Message-based, not token-based; agent effective context undocumented; weekly caps |
| 4 | **Google AI Pro (+ Antigravity + Gemini CLI)** | $19.99 | Gemini 3.8 Flash (41.2) + Claude Sonnet/Opus 4.6 | Best multimodal agent (image/video/audio + browser); 3 labs in one sub; free tier exists | Quotas are opaque "compute" units; tightened at I/O 2026, then tripled twice after backlash |
| 5 | **Muse Code (Meta) High/Power** | ~$20–100 | Muse Spark 1.3 (48.2) | Highest-II model with subsidized access; 1M ctx; image+video uploads; sub-first product | Two weeks old; prices shown only at onboarding; prompt caps (10–50/5h base) |
| 6 | **Z.ai GLM Coding Plan Pro** | $72 | GLM-5.3 (44.9) | 1.26–2.5B tokens/mo official estimate — heavy-usage king per dollar | Same model-quality ceiling as #1 |
| 7 | **GitHub Copilot Pro+** | $39 | 6 labs incl. GPT-6 Astra, Opus 5, Fable 5.1, Kimi K3, Gemini 3.8 Flash, Grok 4.6 | Broadest multi-model catalog; credits = $0.01 of tokens; unlimited completions; Max tier $100 | Credits ≈ API price 1:1 — breadth, not subsidy; $39 buys only ~$39 of frontier tokens |
| 8 | **MiniMax Token Plan Plus** | $22 | MiniMax M3 (29.6) | KDnuggets' value pick; 1M-ctx M3 + image + speech in one pool; works in Claude Code/Cursor/Cline | Capacity unpublished (console bar); M3 well below the frontier band on AA II |
| 9 | **Kimi Code via Allegretto membership** | $39 | Kimi K3 (43.8, 1M ctx) | 5× credit multiplier; K3 is a genuine 1M-ctx frontier-adjacent model; Claude Code/OpenCode/Codex support | K3 gating on tiers from third-party sources only; entry tier ships 256K K2.7 |
| 10 | **Alibaba Cloud Model Studio Coding Plan Pro** | $50 | qwen3.7-plus (vision), GLM-5, Kimi K2.5, MiniMax M2.5 | One subscription, four labs, 90K requests/mo, vision-capable models; Anthropic-compatible endpoint | Request-count quota (5–30 calls/task); last-gen models; slots restocked daily |

---

## THE HIDDEN DEALS

Providers worth knowing even where they didn't win:

1. **Meta Muse (Sep 2026)** — the biggest *new* thing this pass. Meta's consumer Muse agent
   launched with **100M free tokens/week** (Gizmodo: "a mind-boggling amount of free compute";
   multiple outlets, Sep 5–10). Muse Spark 1.3 API costs **$1.25/$4.25** — roughly a quarter of
   Opus-5 pricing at II 48.2. **Why the economics work:** Meta is buying developer mindshare for
   its Superintelligence-labs stack with venture-scale subsidies; the consumer promo is
   deliberately loss-making. Risk: promo terms are unpublished; Muse Code subscription dollar
   prices only appear at onboarding (press: $20–$100).
2. **Antigravity free tier (Google)** — $0 gets Gemini 3.8/3.7/3.6 Flash + Gemini 3.1 Pro +
   **Claude Sonnet 4.6 & Opus 4.6 (thinking)** + gpt-oss-120b, with unlimited tab completions
   and unlimited command requests. Google pays Anthropic for your free Claude access —
   cross-subsidy from Google's agent-platform war chest. Weekly quota is finite and unpublishd.
3. **Z.ai GLM-5.3-Flash campaign** — Sep 3–20, 2026: **zero-credit unlimited Flash** in ZCode
   23:00–09:00 Singapore time, and **doubled** quota in all other agents, for all paid plans.
   Flash (II 41.9) is the cheapest frontier-adjacent token on Earth during the window.
4. **Xiaomi MiMo Token Plan** — the phone maker sells a 1M-context agentic-coding model
   (MiMo-V2.5-Pro) with credit plans; KDnuggets' reviewer used it more than GLM/MiniMax/Codex.
   AA II is only 26.4 — cheap, not frontier. Long-tail curiosity with real infra behind it.
5. **Kilo Pass (Kilo Code, now Anaconda)** — pays *exact provider rates* with up to 50% bonus
   credits ($19 → $26.60/mo of credits). It's the only Western "subscription discount on
   API-price" still standing after Cursor went usage-metered. Free tier routes Auto tasks
   through free models.
6. **Z.ai on Tmall** (China) — Z.ai and DeepSeek sell coding subscriptions through Tmall
   storefronts (SCMP, Apr 2026). Legitimate first-party regional pricing, but requires a CN
   account/payment — noted, not recommended unless you're already there.
7. **Cerebras Code** — historically the speed arbitrage (1,000 tok/s GLM): Pro $50/24M
   tokens-per-day, Max $200/120M — **all paid tiers sold out** as of Sep 13, 2026, and the
   model is last-gen GLM 4.7. Watch for restock with GLM-5.3.
8. **Qoder's time-of-day credits** (Alibaba) — off-peak discounted credits for Qwen3.7-Max
   (Yahoo Finance, Jun 2026): same lab play as Z.ai's 50% off-peak credit rate. Regional and
   fiddly, but the *pattern* (time-of-day arbitrage) is spreading.
9. **Alibaba "Ultimate" multi-lab Coding Plan** — the only subscription where one plan key
   switches between Qwen + GLM + Kimi + MiniMax models (Feb 2026). It prefigures where all
   aggregators are going.
10. **DeepSeek V4.1 Flash** (Sep 10, 2026) — II 39.5 / TB-v4 0.268 at **$0.30/$1.20** with 1M
    ctx and native image input. Not a subscription yet, but the cheapest credible agent-model
    per token anywhere; expect a V4.1-based coding plan within months.

---

## THE ARBITRAGE OPPORTUNITIES

Where buying through a coding tool is much cheaper than the underlying model's API:

| Route | Subscription | What the same usage costs at API list | Multiple |
|---|---|---|---|
| **GLM-5.3 via GLM Coding Plan Lite** | $18/mo | $737–$1,489/mo (capacity value at GLM API rates, user's in/out mix) | **41–83×** |
| Claude Opus 4.6 inside Antigravity free | $0 | Anthropic API (Opus-class) | effectively ∞ until weekly quota |
| Muse Spark 1.3 via Muse consumer promo | $0 (100M tokens/wk) | $125–$425 per 100M at API rates (mix-dependent) | promo-window arbitrage |
| Gemini 3.8 Flash via AI Pro / Antigravity | $19.99 / $0 | $152/mo for your workload at intro API rates (double after Dec 31, 2026) | limited by opaque quotas |
| GPT-5.6 Sol via Codex Pro 20x | $200/mo | ≈ $9,000–10,000/mo (heavy-user measurement, HN Jul 2026) | **~45×** |
| Codex Plus (same ratio ÷ 20) | $20/mo | ≈ $450/mo | ~22× |
| GLM-5.3-Flash quota on Lite | $18/mo | $254–$508/mo at Flash API rates | 14–28× |

**Why the economics work (mechanisms, per the brief):**
- **Pooled inference + non-exhausting users** — flat plans priced on average consumption
  (Classic subscription economics; the reason weekly windows now exist).
- **Wholesale-to-self** — Z.ai, MiniMax, Moonshot, Alibaba, Meta are their own model vendors:
  a coding plan is marginal GPU cost, not an API resale with margin.
- **Off-peak shaping** — Z.ai charges 50% credits off-peak and ran unlimited-Flash nights;
  Qoder prices credits by time of day. Smoothing load lets cheap plans exist.
- **Venture/promotional subsidies** — Meta's free 100M tokens/week, Google's free Claude in
  Antigravity, intro-priced Gemini 3.8 Flash (explicitly doubling Jan 1, 2027).
- **Cache-heavy economics** — GLM plan allowances assume 95%+ cache hit (cached input costs 1.7
  vs 6.9 credits); agentic workloads with big cached system prompts are exactly where the plan
  multiplies fastest. Anthropic/Moonshot mirror this with 90%+ cache discounts at API level.

**Where there is NO arbitrage:** GitHub Copilot (credits = API price 1:1; you buy breadth and
unlimited completions, not discount), OpenCode Zen (explicit zero markup), Cline/Roo (BYOK),
Cursor (usage-based overage billed in arrears — one HN user reported an unsupervised $200
overage in a single session).

---

## WHAT I WOULD BUY

1. **Best overall: GLM Coding Plan Lite ($18) + Claude Pro ($20).** The GLM plan carries the
   bulk (routine edits, tests, docs, long sessions — 1M-ctx model, 200M+/month headroom);
   Claude Pro stays as the verified-1M-context Opus-5-class escape hatch inside Claude Code.
   Total $38/mo, ≈4× your 52.5M/mo target covered, with true-frontier overflow.
2. **Best cheap option (single sub): ChatGPT Plus $20** if you want Western-frontier quality
   with simple billing and can live inside message windows; **Antigravity free + Google AI Plus
   $4.99** if you want maximum multimodal for pocket change.
3. **Best backup: Claude Max 5x ($100)** when a demo/launch week demands max-effort Opus 5 or
   Fable 5.1 with *verified* 1M context in Claude Code — or Kilo Pass $19 as a zero-risk
   pay-provider-rates fallback pool that never markups.

---

## Workload test (52.5M tokens/month = 15M in + 37.5M out)

Verdicts per the brief's five levels. "Capacity" = subscription allowance, not model theory.

| Plan | 10M | 25M | 50M | 52.5M | 100M | Basis |
|---|---|---|---|---|---|---|
| GLM Coding Plan Lite ($18) | PASS | PASS | PASS | **PASS** | PASS | official 208–420M/mo (GLM-5.3 @95%) |
| GLM Coding Plan Pro ($72) | PASS | PASS | PASS | **PASS** | PASS | official 1.26–2.5B/mo |
| Claude Pro ($20) | PARTIAL | FAIL | FAIL | **FAIL** | FAIL | user benchmark ≈10M/mo practical |
| Claude Max 5x ($100) | PASS | PARTIAL | PARTIAL | **PARTIAL** | FAIL | ≈5× Pro, ESTIMATED ~50M+ |
| Claude Max 20x ($200) | PASS | PASS | PASS | **PASS** | PARTIAL | ≈20× Pro, ESTIMATED |
| Codex Plus ($20) | PASS | PARTIAL | PARTIAL | **PARTIAL** | PARTIAL | message caps + weekly limits |
| Codex Pro 20x ($200) | PASS | PASS | PASS | **PASS** | PASS | ≈$9–10k/mo API-equiv (community) |
| Google AI Pro ($19.99) | UNKNOWN | UNKNOWN | UNKNOWN | **UNKNOWN** | UNKNOWN | quotas are unpublished compute units |
| Antigravity free ($0) | PARTIAL | FAIL | FAIL | **FAIL** | FAIL | basic weekly quota |
| Muse Code High (~$50) | PASS | PARTIAL | UNKNOWN | **UNKNOWN** | UNKNOWN | prompt caps; young product |
| MiniMax Token Plan Plus ($22) | UNKNOWN | UNKNOWN | UNKNOWN | **UNKNOWN** | UNKNOWN | allowance unpublished |
| Kimi Allegretto ($39) | PARTIAL | UNKNOWN | UNKNOWN | **UNKNOWN** | UNKNOWN | 5× multiplier, tokens unpublished |
| Copilot Pro+ ($39) | PASS | FAIL | FAIL | **FAIL** | FAIL | $39 of tokens at API rates |
| Kilo Pass Starter ($19) | PASS | PARTIAL | FAIL | **FAIL** | FAIL | $26.60 credits at provider rates |
| Trae Pro ($10) | PARTIAL | FAIL | FAIL | **FAIL** | FAIL | $20 usage value |
| Alibaba Coding Plan Pro ($50) | PARTIAL | PARTIAL | UNKNOWN | **UNKNOWN** | UNKNOWN | 90K requests/mo, per-call cost varies |
| Cerebras Max ($200) | PASS | PASS | PASS | **PASS** | PASS | 120M tokens/**day** — but SOLD OUT |

---

## 1M-context deep dive (finalists)

Per the brief: model ctx / API ctx / agent ctx / subscription ctx are four different claims.

| Finalist | Model ctx | API ctx | Agent ctx | Subscription ctx | Max output | 1M actually usable in agent? | Preserved across iterations? |
|---|---|---|---|---|---|---|---|
| GLM Coding Plan (GLM-5.3) | 1M | 1M | via Claude Code/OpenCode/etc. (harness-dependent) | same as agent | — | **YES** (agent harnesses expose model ctx; GLM-5.3 is the plan model) | PARTIAL (harness compaction, e.g. Claude Code `/compact`) |
| Claude Max (Opus 5 / Fable 5.1) | 1M | 1M | **Claude Code: 1M officially documented** | Max: included; Pro: requires enabling usage credits for Opus 1M | 300K w/ beta header (batch) | **YES (verified, first-party doc)** | PARTIAL (auto-compaction; context managed) |
| Codex Plus (GPT-5.6 Sol) | 1M (AA) | 1M | **UNDOCUMENTED** — long-context tier billed >272K in Copilot's table suggests harness caps | same | — | UNKNOWN | UNKNOWN |
| Gemini 3.8 Flash (Antigravity/AI Pro) | 1M | 1M | undocumented in Antigravity docs | same | — | UNKNOWN (likely, unverified) | PARTIAL |
| Muse Code (Spark 1.3) | 1M | 1M | undocumented | same | — | UNKNOWN | UNKNOWN |
| Kimi K3 (Kimi Code) | 1,048,576 | 1M+ | Kimi Code markets 1M whole-codebase loads | membership quota | — | YES (vendor-documented for the agent) | PARTIAL |
| GitHub Copilot (Opus 5 / Astra) | 1M | long-context tier priced >272K | model-dependent | credit-metered | — | PARTIAL | PARTIAL |

Note: **only Anthropic documents 1M at the coding-agent level**, and on Pro plans Opus-1M
requires usage credits to be enabled. GLM-5.3 and Kimi K3 give you 1M models through agents
whose harnesses generally pass the model's context window through — TRUE for Claude Code with
custom endpoints, but a harness-level cap is possible and marked PARTIAL where undocumented.

## Multimodal deep dive (can the agent actually send it?)

| Plan | Image in | PDF in | Video in | Audio in | Notes |
|---|---|---|---|---|---|
| Claude Max / Pro | YES | YES (files) | no | no (voice mode ≠ model input) | Claude Code accepts images; PDFs via file tools |
| GLM Coding Plan | via Flash model / Vision MCP | via reader MCP | no | no | GLM-5.3 itself text-only — the plan's main multimodal gap |
| Codex (GPT-5.6) | YES (image uploads incl. mobile) | via tools | no | no | "image and video uploads" listed for Muse, not Codex |
| Antigravity / AI Pro | YES | YES | **YES** (Gemini 3.8) | **YES** (Gemini 3.8) | only plan with video+audio model input in-agent |
| Muse Code | YES ("image and video uploads") | via tools | YES (upload) | voice mode | per first-party subscription doc |
| Kimi Code (K3/K2.7) | YES (native vision) | YES | K2.7-class: video input documented | no | K2.7 Code: text/image/video per docs |
| Copilot | YES (model-dependent) | via tools | model-dependent | no | depends on chosen model |

---

## Rankings

**Weighted (30% capacity / 25% quality / 15% 1M-ctx / 10% multimodal / 10% price / 10% multi-model):**

1. **Cheapest viable option:** Antigravity free tier ($0) — if "viable" includes modest weekly
   quotas; cheapest *guaranteed-capacity* viable: **GLM Coding Plan Lite $18**.
2. **Best value overall:** **GLM Coding Plan Lite** — 20–40× Claude Pro capacity, near-frontier
   model, first-party quota transparency.
3. **Best Opus-5 alternative:** **GLM-5.3** for agentic-coding dependability per dollar
   (TB-v4 0.419 vs Opus 4.8's 0.217); **Muse Spark 1.3** (II 48.2) as the highest-IQ
   Opus-substitute if you accept a two-week-old stack.
4. **Best heavy-usage:** **GLM Coding Plan Pro $72** (1.26–2.5B tokens/mo official estimate);
   runner-up Codex Pro 20x $200 for frontier quality at ~$9–10k/mo API-equivalent.
5. **Best multi-model:** **GitHub Copilot Max $100** (six labs, one bill, unlimited completions);
   budget pick **Alibaba Coding Plan Pro $50** (four labs, subsidized); free pick **Antigravity**
   (Gemini + Claude + GPT-OSS).
6. **Best 1M-context:** **Claude Max** — the only *documented* 1M context inside a first-party
   coding agent (Claude Code). GLM Lite is the budget route to 1M via third-party harnesses.
7. **Best under $10:** **Google AI Plus $4.99** (expanded Antigravity/Flow access; 128K app ctx)
   and Antigravity itself at $0. Paid workhorse under $10: none beat free Antigravity + AI Plus.
8. **Best under $15:** Google AI Pro is $19.99; under $15 the pick is **Google AI Plus $4.99 +
   Antigravity free**, or Mistral Le Chat Pro $14.99 if Vibe/Devstral suits you.
9. **Best under $20:** **GLM Coding Plan Lite $18** (with Codex Plus $20 just over the line).
10. **Best obscure/niche provider:** **Meta Muse** (free 100M tokens/week promo + $1.25/$4.25
    near-frontier API); honorable mention **Xiaomi MiMo** and **Agnes (Sapiens AI)** — a
    Sep 11, 2026 launch at $0.05/$0.15 with II 35.5, one to watch.
11. **Best coding-tool arbitrage:** **GLM Coding Plan** (41–83× GLM-API value; verified against
    first-party allowance tables), with **Antigravity-free-Claude** as the purest subsidy.
12. **Maximum tokens/$:** GLM Coding Plan Lite quota spent on **GLM-5.3-Flash** — up to
    ~1.26B tokens/month for $18 ≈ **$0.014/M tokens**.

**Frontier coding quality per dollar (quality-only ranking of the same plans):**
1. GLM Coding Plan Lite (GLM-5.3 TB-v4 0.419 at $18) · 2. MiniMax Token Plan Plus (value; quality
caveat) · 3. Muse Code (Spark 1.3 II 48.2, cheap API) · 4. ChatGPT Plus (Sol 47.1 at $20) ·
5. Trae Pro · 6. Alibaba Coding Plan · 7. Kimi Allegretto (K3) · 8. Google AI Pro (3.8 Flash) ·
9. Claude Max 5x (Opus 5 — the quality ceiling that survives contact with quotas) ·
10. GitHub Copilot Max (breadth, not depth-per-dollar).

---

## Method & caveats

- Model numbers (II, TB-v4, context, API price, modalities) were extracted from AA's embedded
  dataset on 2026-09-13 (`data/aa-snapshot-2026-09-13.json`, 116 non-deprecated models with
  II ≥ 20); the 45-row filtered DB is what this report cites. Effort variants (e.g.
  "Opus 5 (max)") were normalized to their release's default top effort.
- Subscription economics were taken from first-party pages/docs wherever possible; snapshots in
  `sources/`. Where a provider publishes no token numbers (Google, Cursor, MiniMax, Muse),
  capacity is labeled **UNKNOWN** rather than guessed — never invented.
- The 10M/month "Claude Pro practical" baseline is the client-supplied benchmark, consistent
  with Anthropic's undocumented rolling limits; treat as ESTIMATED.
- Community datapoints (Codex API-equivalents, Cursor overage story, GLM/Kimi value) are
  individual reports — directionally useful, not measurements.
- Privacy note: an HN-submitted reverse-engineering writeup (runtimewire.com, Aug 2026) claimed
  Muse Code forwards some prompts/telemetry to Meta by default; Meta's Model API ToS governs code
  submission. Treat Muse Code as a young product and read its data-use terms before sending
  proprietary code.
- Regional/reseller notes (Tmall storefronts, top-up resellers) are informational; resold
  shared accounts violate provider ToS and are excluded from recommendations.
- Freshness half-life: GLM-5.3-Flash campaign ends Sep 20, 2026; Gemini 3.8 Flash intro pricing
  ends Dec 31, 2026; Claude weekly limits: +25% announced, effective Sep 14, 2026 (the day after this research date); Muse promo terms may change
  without notice. Re-verify anything you buy.
