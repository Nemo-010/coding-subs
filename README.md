# coding-subs

Market research on the **cheapest legitimate ways to get large amounts of frontier-level
coding-agent usage by subscription** — model landscape, provider arbitrage, published quotas,
1M-context verification, and heavy-usage economics.

## Research passes

| Date | Report | Scope |
|---|---|---|
| **2026-09-13** | [2026-09-13/README.md](2026-09-13/README.md) | Full pass: 45-model landscape (AA snapshot), 44 access plans across 26 provider groups, workload tests, rankings |
| **2026-09-20** | [2026-09-20/README.md](2026-09-20/README.md) | Relay/provider pass over `Wei-Shaw/sub2api` **and** `router-for-me/CLIProxyAPI`: sponsor markets ranked by cheapest published plans. Provider-support surface (first-class platforms, account types, the 222-provider `models.dev` registry) in [PROVIDER-SUPPORT.md](2026-09-20/PROVIDER-SUPPORT.md); reconciled union of both repos (72 providers) in [RECONCILED-PROVIDERS.md](2026-09-20/RECONCILED-PROVIDERS.md) |

Each pass directory contains the report (`README.md`), the underlying databases (`data/`),
numbered citations with access dates (`references/`), and raw snapshots of primary sources
(`sources/`).

## Method in one paragraph

Model quality comes from an Artificial Analysis dataset snapshot (Intelligence Index,
Terminal-Bench v4.0, context windows, API prices, modalities). Subscription economics come from
first-party pricing pages and docs wherever possible — fetched and archived in `sources/` on the
research date — with every unverifiable number labeled ESTIMATED or UNKNOWN rather than guessed.
The 2026-09-20 relay pass applies the same rule to a different universe: the providers advertised
in a third-party project's README, where sponsor copy is treated as advertisement and only the
provider's own published rate card is VERIFIED. Each pass undergoes independent reviews
(recorded in [docs/reviews.md](docs/reviews.md) for 2026-09-13 and
[docs/reviews-2026-09-20.md](docs/reviews-2026-09-20.md) for 2026-09-20) before being committed.

## Conventions

- Prices in USD unless marked otherwise; "M tokens" = millions of tokens.
- VERIFIED = read directly from the provider's own current page/docs. THIRD-PARTY = reputable
  secondary source. ESTIMATED = derived calculation. UNKNOWN = not published; never invented.
- Repo layout per pass: `YYYY-MM-DD/{README.md, data/, references/, sources/}`.
