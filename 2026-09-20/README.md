# sub2api Provider & Relay Market — Cheapest Plans, Ranked by Evidence

**Research date: 2026-09-20 (UTC).** Subject commit: `Wei-Shaw/sub2api` at
`19794bc46afb` (README sponsor table + tracker mined 2026-09-20T04:45Z). Databases:
[data/providers-database.csv](data/providers-database.csv) (26 advertised providers),
[data/rate-cards.csv](data/rate-cards.csv) (25 published token prices),
[data/subscription-plans.csv](data/subscription-plans.csv) (10 flat/promo plans),
[data/reachability.json](data/reachability.json) (3-round endpoint probe). Numbered
citations: [references/references.md](references/references.md). Raw snapshots:
[sources/](sources/).

> Level of access note: this pass reads **public** pages only. Where a provider prices
> behind a login, the value is reported `UNKNOWN`, never inferred from the advertisement.

---

## ⚠ Scope correction (added after review)

**The tables in this README rank the 26 README sponsor rows, which is a sponsorship
list, not sub2api's provider surface.** sub2api's actual provider support is much wider:
ten first-class platforms, six account types (including a BYO-base-url `upstream` type),
and the **models.dev registry it fetches — 222 providers, 7,868 models**. The full
code-grounded study is in **[PROVIDER-SUPPORT.md](PROVIDER-SUPPORT.md)**, with
[data/modelsdev-providers.csv](data/modelsdev-providers.csv),
[data/cheapest-per-model.csv](data/cheapest-per-model.csv) and
[data/subscription-plan-providers.csv](data/subscription-plan-providers.csv).
Read that file for anything about "which providers sub2api supports"; read this README
only for the sponsor-market pricing.

---

---

## ⛔ What this pass did NOT establish

Read this before the ranking. It is the honest half of the document.

| not established | why it matters |
| --- | --- |
| **Actual delivered model identity** | Nothing here proves the model behind a key is the model named. The subject's own tracker is full of "降智" (intelligence-degradation) reports (issues #6871, #7202, #6957; see [references](references/references.md) §30), and CodexEverywhere itself says it **suspended its Grok free pool because xAI reduced model intelligence for free-tier accounts** (source 6). Priced cheaply ≠ served faithfully. |
| **Real throughput / cache-hit behaviour** | Every published rate card assumes cache behaviour. CodexEverywhere documents "cache hit rate is low during streaming" on its Gemini/Antigravity beta (source 6). No latency or cache measurement was taken here beyond endpoint reachability. |
| **Sustained uptime** | The only reliability number taken is a **3-round reachability probe through a third-party reverse proxy** (see below). It measures whether a page answered, not whether the gateway stayed up. |
| **Prices behind login** | 9 of 17 AI providers publish no public rate card. Their `UNKNOWN` is a real gap, not a rounding to "cheap". |
| **Exchange-rate comparability of CNY plans** | AIGoCode and Qiniu price in CNY; no conversion is applied in the rankings. Their *credit multiples* are currency-independent; their dollar comparisons are not. |
| **Whether any of this survives an account ban** | The subject project's own notice says using it "may violate the terms of service of Anthropic and other upstream providers". Every "reliable" verdict below is about billing and catalogue transparency, **not** about account safety. |

⚠ **The reachability probe was taken through `api.rv.pkgforge.dev`, not from the
provider's own network.** The status is meaningful; the milliseconds are the proxy's,
not the provider's.

⚠ **How many claims a previous revision got wrong:** this is revision 1, so the honest
number is *unknown*. The deep-review log records 20 passes and the fixes they forced;
read [docs/reviews-2026-09-20.md](../docs/reviews-2026-09-20.md) before trusting a
number. Assume more remain.

---

## The question, and what would falsify the pass

> **Which of the providers advertised in `Wei-Shaw/sub2api`'s README sell frontier-model
> access most cheaply, on published evidence, and which of those are also transparent
> and reachable?**

This pass would be abandoned if: (a) no provider published a checkable rate card, making
"cheapest" a pure advertisement ranking; or (b) the advertised discount and the published
rate card disagreed for every provider, meaning the sponsor copy is decorative. Neither
happened — **five providers publish a token rate card** (CodexEverywhere, hao.ai, LanoX,
OpenModel, CCTK), and for those the copy and the card mostly
agree — but the pass **is** downgraded to "advertisement ranking" for the 9 providers that
publish nothing.

---

## BEST DEAL FOUND (concise answer)

| Field | Value |
| --- | --- |
| **BEST DEAL FOUND** | **hao.ai — published per-model rate card at 0.15× official** |
| **EVIDENCE GRADE** | **VERIFIED** — public catalogue prices each shown beside the official reference |
| **CHEAPEST FRONTIER RATE** | **GPT-6 Astra input $1.50 / output $7.50 per 1M** (official $10 / $50) = **0.15×** |
| **ALSO AT 0.15×** | GPT-5.6 Sol ($0.60/$3.00 vs $4/$20), GPT-5.6 Terra ($0.30/$1.80 vs $2/$12), Grok 4.6 ($0.30/$0.90 vs $2/$6) |
| **CONDITIONS** | 20-model catalogue, USD, cache read/write priced separately, publication snapshot 2026-09-20 |
| **WHY IT BEATS THE HEADLINE CHEAPEST (0.03×)** | CodexEverywhere's 0.03× pool is **cheaper but self-declared unstable** ("Pro Pool is a backup for when Plus Pool is unstable"); hao.ai's 0.15× is a normal catalogue with no such admission |
| **WHY IT IS NOT A RECOMMENDATION TO TRUST BLINDLY** | Cheap resale of subscription quotas is the exact market the subject's own tracker shows degrading; hao.ai does not publish uptime or model-provenance guarantees |
| **CONFIDENCE** | **HIGH** on the published prices; **LOW** on delivered model identity and uptime — neither was measured |

---

## How this market is shaped (60-second orientation)

- **The universe is the subject's sponsor table, not a standard.** `Wei-Shaw/sub2api` lists
  **26 sponsored links** in its README table at `19794bc46afb`. Sponsorship is a paid
  placement; inclusion is not a quality signal. **Nine of the 26 are not AI providers at
  all** (proxies: Bestproxy, Proxy4Free, RapidProxy, Swiftproxy, DuckIP, ColaProxy; CDN:
  Veilx, AxisNow; anti-detect browser: RoxyBrowser) and are tabulated here for completeness
  but excluded from the AI-plan ranking.
- **Most of the "relays" are the same software.** Seven of the advertised sites carry a
  live sub2api `window.__APP_CONFIG__` (CCTK.AI, APIKEY.FUN, CodexEverywhere, Nagora,
  PPToken, PP.dog, FennoAI), and an eighth (Aimzoon) serves a sub2api shell — so half the
  AI list runs the subject project's own panel. The README is, in part, an advertisement
  page for instances of its own product.
- **The cheap end is a quota-resale market.** The ultra-low multiples (0.03×–0.3×) are not
  the labs' own pricing; they are resale of consumer subscription pools (Codex Plus/Pro,
  Claude Max/Kiro, Gemini Antigravity). Their economics are the same as the coding-subscription
  arbitrage documented in the [2026-09-13 coding-subs pass](../../2026-09-13/README.md),
  with the risk layered on.
- **Two pricing shapes exist and they are not comparable:** a **per-model multiple of
  official** (hao.ai, LanoX, CodexEverywhere, OpenModel, CCTK) and a **flat 4-week
  subscription with credit** (AIGoCode, Qiniu). Ranking them in one column would be a
  category error; they are ranked separately below.

---

## RANKING 1 — cheapest token rates (verified cards first, advertisements after)

**Part A — providers with a published, checkable rate card (VERIFIED).** Ranked by the
lowest multiple of official list price actually printed on their own page. `UNKNOWN`
elsewhere means no public card existed on 2026-09-20.

| # | Provider | Cheapest published pool | Printed price (GPT-6 Astra in/out per 1M) | Multiple | Evidence | Caveat |
|---|---|---|---|---|---|---|
| 1 | **CodexEverywhere** | Codex Plus Pool | $0.30 / $1.50 | **0.03×** | VERIFIED (source 6) | Provider: Plus Pool unstable; Pro Pool is the backup (0.05×) |
| 2 | **hao.ai** | default catalogue | $1.50 / $7.50 | **0.15×** | VERIFIED (source 15) | No uptime/provenance published |
| 3 | **LanoX** | default ("1 : 0.167") | $1.67 / $8.35 | **0.167×** | VERIFIED (source 14) | Claims 99.9% channel availability, unmeasured |
| 4 | **OpenModel** | catalogue, "up to 60% OFF" | n/a on Astra; Claude Fable 5 $4/$20 (0.40×) | **0.40×** | VERIFIED (source 2) | "No platform fee" claim; catalogue not independently audited |
| 5 | **CCTK.AI** | GPT-Pro group | $6.00 / $30.00 (0.60× for GPT) | **0.6× GPT / 2.1× Claude** | VERIFIED (source 1) | Claude group is **2.1× official — dearer than official** |

**Part B — advertisement-only (ADVERTISED), deliberately below every verified row.** No
public card existed; the only evidence is the sponsor copy in the subject's README.

| Provider | Claimed multiple | Sponsor's own arithmetic |
|---|---|---|
| **PP.dog** | 0.03× | "0.03x, just 0.35% of official" — 0.03× is 3%, not 0.35% (source 17) |
| **APIKEY.FUN** | 0.07× | "as low as 7% of the original rate" (source 4) |
| **PPToken** | 0.16× | "0.16x … roughly 2.2% of official" — 0.16× is 16%, not 2.2% (source 9) |
| ETok, Nagora, Aimzoon, FennoAI, Pateway, BmoPlus | UNKNOWN | no public card; behind login/checkout |

### The misdirection worth naming

The **cheapest headline number is not the best deal**. Three separate mechanisms push a
reader toward 0.03× and away from what they want:

1. **The 0.03× pool is unstable by the seller's own words** (source 6). You are buying a
   lottery, not a rate.
2. **The two 0.03× advertisements are arithmetically wrong.** PP.dog's "0.03× combined rate,
   just 0.35% of official" (source 17) and PPToken's "0.16×, roughly 2.2% of official"
   (source 9) each state two numbers that cannot both be true. An advertisement that
   cannot do its own multiplication is not evidence of cheapness.
3. **"Cheap" on one group can hide "dear" on another.** CCTK advertises "a fraction of the
   official cost" yet its published Claude group multiplier is **×2.1** (source 1). The
   advertised fraction applies to the GPT-Pro group (0.6×), not to Claude, which is what
   most coding-agent users actually burn.
4. **The advertisement and the rate card can disagree about the same provider.** The
   subject's README advertises APIMart's GPT-Image-2 "from $0.006 per image, 160+ images
   per dollar", while APIMart's own model page lists **$0.0085 before 20% off** (source 16).
   ColaProxy's advert says "$0.3/GB" while its own pricing page says **$1.6/GB** (source
   26). Sponsor copy is not a price.

The winning explanation (per-model, published, side-by-side rate cards) is less exciting
than a 0.03× headline, which is exactly why the headline is the losing answer.

---

## RANKING 2 — cheapest flat subscription plans

| # | Provider | Plan | Price | What you get | Effective shape | Evidence |
|---|---|---|---|---|---|---|
| 1 | **AIGoCode** | Pro | **CNY 399 / 4 weeks** | **$440 credit**, $110 refreshed every 7 days | ~8× face value *if* credit bills at official rates (UNVERIFIED assumption) | VERIFIED price (source 5) |
| 2 | **AIGoCode** | Max | CNY 899 / 4 weeks | $1,040 credit, $260/7d | as above | VERIFIED (source 5) |
| 3 | **AIGoCode** | Ultra | CNY 1,799 / 4 weeks | $2,120 credit, $530/7d | as above | VERIFIED (source 5) |
| 4 | **Qiniu AI** | Enterprise S | CNY 2,999/mo (list 4,284; 7折扣) | ~1.07B credits/mo, 16 models (DeepSeek/Kimi/GLM/MiniMax), OpenAI+Anthropic API | Enterprise contract, listed company | VERIFIED (source 12) |
| 5 | **Qiniu AI** | Enterprise M | CNY 4,999/mo | ~2.08B credits/mo | as above | VERIFIED (source 12) |
| 6 | **Qiniu AI** | Enterprise B | CNY 9,999/mo | ~5.00B credits/mo; annual from 4折扣 | as above | VERIFIED (source 12) |
| — | **BmoPlus** | account resale | UNKNOWN | "10% of official GPT subscription price (90% OFF)" | resale of accounts, not a metered plan | ADVERTISED (source 7) |

⚠ **AIGoCode's 8× face value is an ESTIMATE and it is load-bearing.** The page guarantees
"$440 credit"; it does **not** publish the per-model rate at which that credit is spent. If
the internal rate is inflated, the real multiple is smaller. Treat "~8×" as a hypothesis to
test at checkout, not a measured value.

⚠ **Qiniu's credits are not dollars.** Base unit is `0.004 CNY / K tokens`, and models
carry a price coefficient (`刊例价 ÷ 0.004`), so a credit buys a model-dependent number of
tokens — not a fixed dollar amount (source 12).

---

## THE CATEGORIES

### Best "free" (trial or free tier) — biggest no-risk entry

| Rank | Provider | What is actually free | Evidence |
|---|---|---|---|
| 1 | **LanoX** | NVIDIA models listed "free"; new-user trial tokens; "500+ free models" | ADVERTISED (source 14) |
| 2 | **Qiniu AI** | 3M tokens (developers) / 12M (enterprise) on registration | ADVERTISED (source 12) |
| 3 | **CodexEverywhere** | **$20 free trial**, stated in its own docs | VERIFIED (source 6) |
| 4 | **Pateway** | $1 on signup + $3 on first purchase (up to $66 per transaction in bonuses) | VERIFIED (source 8) |
| 5 | **FennoAI** | $50 of Coding Plan credit for $1.99 (not free, but near-free) | ADVERTISED (source 13) |
| 6 | **APIKEY.FUN / AIGoCode** | up to 5% off recharges / 10% bonus credit — a discount, not a free tier | ADVERTISED (sources 4, 5) |

⚠ There is **no genuine ongoing free frontier tier** in this list. Every "free" row is a
one-off trial or a marketing credit. The subject project's README copy calling things
"free" is the same class of claim as "0.03×".

### Best "cheap" (lowest cost to run real volume)

1. **CodexEverywhere** — lowest published multiple (0.03× Plus / 0.045× Kiro / 0.06×
   Antigravity), with the seller's own stability caveats. Cheapest, least dependable.
2. **hao.ai** — 0.15× across GPT-6 Astra, GPT-5.6 Sol/Terra, Grok 4.6; per-model card.
3. **LanoX** — 0.167× average, 83.3% off ChatGPT/Gemini, 70.1% off Claude Code; published
   side-by-side with official.
4. **APIKEY.FUN (0.07×) / PPToken (0.16×) / PP.dog (0.03×)** — advertised only; placement
   below the verified rows is the whole point.
5. **OpenModel (0.40×)** and **CCTK GPT-Pro (0.6×)** — cheap-*ish* but verifiable and
   operationally serious; the "buy boring" option.

### Best "reliable" (transparency, legal surface, operational maturity)

| Rank | Provider | Reliability evidence | What it is still not |
|---|---|---|---|
| 1 | **Qiniu AI** | Listed company (HKEX 02567.HK); enterprise contracts/invoicing; 150+ models; 1.69M customers claimed | Not frontier-cheap; last-gen models in plan |
| 2 | **CCTK.AI** | Full ToS/usage-policy/supported-regions pages; SLA section with a **99.9% target**; named upstreams (AWS Bedrock, Google Vertex); explicit group multipliers | Headline page states **98.9% platform uptime** — the target and the actual differ; Claude group is 2.1× |
| 3 | **OpenModel** | "no platform fee"; production-grade SLA claim; automatic failover; 48-model published catalogue | SLA is self-declared; not independently observed |
| 4 | **LanoX** | **99.9% channel availability** claim; "official direct-connect fallback"; per-model official comparison | Claim unmeasured here |
| 5 | **Pateway** | "100% sourced from official providers"; token-level billing; invoicing for enterprise | Rate itself is ~1.0× — reliability bought with no discount |

⚠ **Reliability here is a *paper* property.** No provider's uptime was observed beyond
3 reachability rounds. The subject's tracker (68 issues mentioning 中转站 and 115 comments)
describes repeated relay failures, and a prior `pptoken.org` outage that commenters
resolved as a datacenter power fault rather than an exit scam (#2946). Read that history as
the base rate.

### Best "deal" (cheap × verifiable × usable)

1. **Overall: hao.ai at 0.15× with a published per-model card.**
2. **Cheapest-but-caveated: CodexEverywhere 0.03× Plus Pool** — only if you can tolerate
   the seller's own "unstable" label.
3. **Flat-plan: Qiniu Enterprise S (CNY 2,999/mo, ~1.07B credits)** for multi-model teams.
4. **Image/video: APIMart** — GPT Image 2 at $0.0085/image, 20% off, pay-as-you-go (source 16).
5. **Reliability with a discount: OpenModel at 0.40×** — the price of sleeping at night.

---

## 1M-context and multimodal reality check

Advertised "1M context" is a **model** property, and the relay's rate card rarely states
its own harness cap. What was actually published on 2026-09-20:

| Provider | Model-level 1M claimed | Relay-level caveat published | Multimodal |
|---|---|---|---|
| hao.ai | yes (GPT-6 Astra, Fable 5.1, Opus 5, Sol, Terra) | none | vision / PDF / function flags listed per model |
| LanoX | yes | long-context tier >272K billed at **2×** (e.g. Astra $3.34/$12.525) | per-model flags |
| CodexEverywhere | yes | "GPT models charge 1.5×–2× above long context (272K-1M)" | GPT/Claude/Gemini listed; cache-write billed 1h=2×, 5m=1.25× |
| OpenModel | yes | long-context billing emerges from the catalogue, not stated in the card | text/image/PDF inputs |
| CCTK.AI | yes | none; publishes the multiplier formula | vision via upstream |

⚠ **No provider in this set documents a first-party coding-agent 1M guarantee.** Only the
labs themselves did that in the [2026-09-13 pass](../../2026-09-13/README.md). A relay
passing a 1M model through a harness is not the same claim.

---

## Arbitrage: what the discount is actually made of

| Route | Advertised | Underlying mechanism | Risk |
|---|---|---|---|
| Codex Plus Pool @0.03× | 3% of OpenAI | resale of Codex consumer quotas | seller says unstable |
| Claude via Kiro @0.045× | 4.5% of Anthropic | AWS Kiro quota resale | "some system prompt" differences noted by seller |
| hao.ai 0.15× / LanoX 0.167× | ~15–17% | resale/pooling of consumer subscriptions | model-identity risk |
| AIGoCode ¥399→$440 | ~8× face | credit at unknown internal rate | rate unpublished |
| Qiniu Enterprise | 5–7折扣 (30–50% off list) | volume wholesale from model vendors | last-gen catalogue |
| Pateway / OpenModel | 1.0× / 0.40× with no markup | catalogue resale, margin from volume | not an arbitrage |

The **only** sustainable arbitrage in this table is volume wholesale (Qiniu) and
catalogue resale at thin margin (OpenModel). Everything at 0.03×–0.17× is a consumer-quota
resale, which is precisely the category the subject's own tracker shows degrading under
load and under upstream anti-abuse changes.

---

## Reachability measurement (taken 2026-09-20, 3 rounds, via reverse proxy)

25 of 26 advertised endpoints answered HTTP 200 in all 3 rounds.
`Swiftproxy` returned **HTTP 403 in all 3 rounds through the proxy** — that is a block on
the observation route, **not** evidence the service is down, and it is recorded as
`UNKNOWN`, not as a failure. Full results and the script:
[data/reachability.json](data/reachability.json), [tools/probe-uptime.py](../tools/probe-uptime.py).

⚠ **What this does not show:** uptime, latency, throughput, or whether the *API* endpoint
behind the marketing page works. `aimzoon.com` answered with a 798-byte shell titled
"Sub2API - AI API Gateway" — reachable is not provisioned.

---

## Provenance

| Source | Commit / revision | Depth reached |
|---|---|---|
| `Wei-Shaw/sub2api` | `19794bc46afb` | README sponsor table read; full tracker mined (7,290 issues/PRs, 12,260 comments, 467 review comments, 51 releases, 53 tags); public settings endpoint probed on each sub2api instance; no code modified |
| `Azathothas/TEMPLATE` methodology | `03be49c2a109` | `docs/methodology/research.md` read in full (750 lines) |
| `talaria0101/coding-subs` layout | `8a229936ce7d` | pass layout, validator style and review format reused |
| Each provider's public pages | live 2026-09-20 | landing page + `__APP_CONFIG__` + pricing/docs route where public; snapshotted in `sources/` |

## Known gaps

- 9 of 17 AI providers publish no public price; their ranking is `UNKNOWN`, not omitted.
- `Swiftproxy` pricing could not be reached (403 on two attempts, two routes).
- `ETok` model pages returned 404; `Pateway`/`APIKEY.FUN`/`PP.dog` docs subdomains answered
  530/404, so only the landing pages were captured.
- No throughput, cache-hit, or model-identity test was run — the subject's own tracker
  supplies the warning, not a measurement.
- The sponsor table is a live page; it changed at least once before this commit
  (`pptoken.org` was renamed off the README after #2946). Re-verify membership before use.
- `docs/reviews-2026-09-20.md` records what the review passes forced; assume further
  errors remain.

---

## Route the reader by budget

| a reader with | reads |
|---|---|
| two minutes | this banner, **BEST DEAL FOUND**, and the two rankings |
| ten minutes | **What this pass did NOT establish**, the categories, and the known gaps |
| the decision to make | the arbitrage table, then the reviews |
| a reason to distrust this | `docs/reviews-2026-09-20.md`, then `sources/`, then re-run `tools/` |
