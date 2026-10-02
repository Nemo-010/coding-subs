# coding-subs

Market research on the **cheapest legitimate ways to get large amounts of frontier-level
coding-agent usage by subscription** — model landscape, provider arbitrage, published quotas,
1M-context verification, and heavy-usage economics.

## Research passes

| Date | Report | Scope |
|---|---|---|
| **2026-09-13** | [2026-09-13/README.md](2026-09-13/README.md) | Full pass: 45-model landscape (AA snapshot), 44 access plans across 26 provider groups, workload tests, rankings |
| **2026-09-20** | [2026-09-20/README.md](2026-09-20/README.md) | Re-verification + delta pass: all first-party sources re-fetched, 26 logged changes (Trae repriced upward, Kimi tiers restructured with the weekly window removed, Claude Code limits settled ~17% below the promo level, new Command Code / Devin / Kiro / Factory / Warp / Zed / Replit ladders), every non-USD price normalized at a cited FX rate, and the relay/sponsor "0.03x" market quarantined into a red-flag advisory instead of a ranking |
| **2026-10-02** | [2026-10-02/README.md](2026-10-02/README.md) | Fresh pass twelve days on: every first-party source re-fetched and byte-compared, **four evidence classes** introduced (VERIFIED / DOCUMENTED / MEASURED / THIRD-PARTY), the metered *subscription multipliers* adopted as a class of evidence (SuperGrok 190×, Claude Max 20× 45.3×, ChatGPT $100 10.25×, Muse Code High 9.3×/114×), cost-per-usable-token and hourly-coverage tables, a 34-row free-tier index, a 2026-10-02 Artificial Analysis model snapshot (Opus 5.5, Sonnet 5.5, Gemini 4 Argon, GPT-6.1 Sol, GPT-6 Luna, Grok 4.7), and the two upstream issues (#1 sources, #2 adjusted/real usage) integrated as an evidence-evaluation pass rather than as adopted rankings |

> The fork's earlier 2026-09-20 relay/reseller pass (sub2api + CLIProxyAPI sponsor table) is kept
> as an archive at [2026-09-20/RELAY-MARKET-ADDENDUM.md](2026-09-20/RELAY-MARKET-ADDENDUM.md),
> with its own databases and references, because the canonical pass drew its evidence and its
> enumeration method from it. It is **not** a ranking of the canonical market; see the canonical
> pass's relay advisory.

Each pass directory contains the report (`README.md`), the underlying databases (`data/`),
numbered citations with access dates (`references/`), and raw snapshots of primary sources
(`sources/`).

## Method in one paragraph

Model quality comes from an Artificial Analysis dataset snapshot (Intelligence Index,
Terminal-Bench v4.0, context windows, API prices, modalities). Subscription economics come from
first-party pricing pages and docs wherever possible — fetched and archived in `sources/` on the
research date — with every unverifiable number labeled ESTIMATED or UNKNOWN rather than guessed.
The subscription universe is **first-party coding-agent plans only**: API relays, sponsor
marketplaces and account resellers are excluded from rankings by policy (see the 2026-09-20
advisory) because their discounts are ToS-violating quota resale and their pricing is
advertisement, not a published rate card. Prices in non-USD currencies are normalized at a cited
FX rate with the rate date. Each pass undergoes independent reviews (recorded in
[docs/reviews.md](docs/reviews.md)) before being committed.

## Conventions

- Prices in USD unless marked otherwise; "M tokens" = millions of tokens.
- VERIFIED = read directly from the provider's own current page/docs. DOCUMENTED = the vendor
  publishes the figure in a rate card (self-graded). MEASURED = the vendor's own usage meter was
  ticked and every call priced at public API list, so the figure is an instrument reading, not a
  claim. THIRD-PARTY = reputable secondary source, dated, with its URL. ESTIMATED = derived
  calculation. ADVERTISED = marketing copy. UNKNOWN = not published; never invented.
- A pass states which evidence class every headline number belongs to, and names its own falsifiers.
- Repo layout per pass: `YYYY-MM-DD/{README.md, data/, references/, sources/}`.
- `tools/validate.py` accepts two report shapes: the **classification** shape (2026-09-13,
  2026-09-20) asserts the HIDDEN DEALS / ARBITRAGE / WHAT I WOULD BUY sections, and the **census**
  shape asserts BEST DEAL / what changed / what would falsify it / known gaps instead.
- `tools/parse-aa.py` pulls the Artificial Analysis top list and per-model fields out of a saved
  snapshot, because the site's own dataset endpoint is brotli-encoded.  
- `tools/fetch-firstparty.py` fetches the live pages into a pass's `sources/`; the URL list at the
  top of that file is the pass's source manifest. `tools/sources-manifest.py` writes the same set
  with `http_status`, `bytes` and `sha256` so a later pass can prove what changed. **A URL that
  returned an error is recorded with its status, not deleted** — 2026-10-02's
  `openai-codex-pricing.md` is recorded as HTTP 403 because that page refuses this network.
