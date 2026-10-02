# Coding subscriptions and agent plans — 2026-10-03

**Source-by-source pass.** Every first-party source was fetched serially on 2026-10-03 —
55 URLs, one request each, one file each, no batching and no retrying a failure into a
success. 53 answered; both OpenAI pages returned HTTP 403 and are recorded as such rather
than deleted. The fetch log is `data/fetch-log.json`, the bytes are in `sources/`, and the
per-provider diffs are in [REVERIFY.md](REVERIFY.md).

This pass exists because the previous one was a delta dressed up as research. It is not.
The list below is what a **live page said today**, provider by provider.

## Measured: what a session actually costs

This pass also measured what a real agent loop consumes, so plan quotas can be expressed as
work rather than as units. Full writeup in **[AGENT-COST.md](AGENT-COST.md)**, harness in
`tools/agentlab/`.

Three results, all from a real loop with a real tokenizer:

- **Cost is context × turns.** The identical one-line fix costs a mean **35,950** input
  tokens in a 3,468-token file and **2,066,679** in a 563,166-token file — a **57× spread** on
  a variable no vendor discloses. A price comparison that does not state a context size is
  meaningless. Repeating each size three times showed a further **1.5×–3.6× run-to-run spread**,
  so cost per task here is a distribution with a long tail, not a point estimate.
- **Tool surface decides outcomes.** With a directory-listing tool the agent solved **8/8**
  tasks; without it, **3/8** — and the failures cost *more* than the successes. **71% of
  tokens (23,134 of 32,481) were spent on tasks it never solved.**
- **Credits convert.** Z.ai publishes `credit = (input×6.9 + cached×1.7 + output×24)/10,000`.
  Applying it to the measured workload reproduces the vendor's own published
  208–420M-tokens/month estimate (177.5M at its stated 95% cache), which validates the method.

That turns the plan table into something it has never been: Copilot Pro's 1,500 requests/month
buy **182 measured tasks**; GLM Lite's 10,000 credits/week buy **10 sessions on a 563k-token
file**; OpenCode Go's $60 ceiling buys **407M tokens**.

## BEST DEAL FOUND

**OpenCode Go, $10/month.** The vendor publishes per-model token prices *and* a monthly
dollar ceiling, so the figure is computable without guessing: the ceiling divided by the
blended price is what $10 buys. The cheapest of its open models is **Muse Spark 1.3
Contributor — $0.10/$0.20 per M, $60 ceiling, 480M tokens, $0.0208/M** — closely followed by
MiMo-V2.6-Flash at **$0.0292/M**. Nothing else in this market publishes both halves of that
equation, which is why this row is the only one in the table with a **HIGH** confidence
derived price rather than a vendor claim.

The runner-up depends on what you already have: **Z.ai GLM Coding Lite at $18** carries a
vendor-published credit estimate (208–420M GLM-5.3, 632–1,264M Flash), the largest published
allowance per dollar here — but the two figures come from different baselines and the row
says so.

## What changed on 2026-10-03

Five providers have **new plans the previous table did not have**, all read from the live
page today:

| Provider | New | Read from |
|---|---|---|
| **Cursor** | **Pro+ $60** between Pro $20 and Ultra $200 | the page's own schema.org `Offer` block |
| **Google** | **AI Plus $4.99** (2x); Ultra restated as `from $99.99` (5x) / `$199.99` (20x) | `gemini.google/subscriptions/?hl=en&gl=us` |
| **AWS Kiro** | **Pro+ $40, Pro Max $100, Power $200** — the table had only Pro $20 | schema.org `Offer` block on kiro.dev |
| **Meta Muse** | **Everyday Usage** base tier; the page publishes **no prices at all** | dev.meta.ai subscriptions doc |
| **Cognition Devin** | **Max $200**, marked NEW on the page | devin.ai/pricing |

Two of those are worth naming plainly because they were **invisible to the old table**:
Kiro had *four* missing tiers, not one, and Meta's price — which the previous table carried
as `$15` — **is not published on Meta's own page**. That row is now marked price-unverifiable
rather than repeating a number no first-party source states.

Everything else re-read **confirms** the previous figures: Z.ai's five pages, MiniMax
($22/$55/$132), Command Code ($1/$10/$20/$100/$200), Trae, Factory, Replit, Zed, Amp,
Mistral, DeepSeek, and the GitHub, Anthropic and Warp prices. A page that did not change is
reported as unchanged, not dressed up as a finding.

## Confidence, honestly separated

| Class | Meaning | Rows |
|---|---|---|
| **VERIFIED live** | a first-party page was fetched today and states this | most of the table |
| **CARRIED FORWARD** | the first-party page is unreadable from here (OpenAI, HTTP 403); not re-checked | 2 |
| **UNKNOWN** | no first-party source states it (Meta's three tiers) | 3 |
| **DERIVED** | arithmetic on two published numbers, mix stated | OpenCode ×2 |

## What would falsify this pass

- A first-party page changing a price after 2026-10-03 (prices are read, not subscribed to).
- Reading OpenAI's pricing through a vantage point that is not 403 (a proxy, a different
  region) and finding the two carried rows wrong.
- Meta publishing seat prices, which would turn three UNKNOWN rows into verifiable ones.
- Kiro's schema.org block being stale relative to a checkout page — it is structured data,
  which is stronger than prose but still the vendor's word.

## Known gaps

- **OpenAI is not re-verified.** Two rows are carried forward from 2026-10-02 because both
  `developers.openai.com/codex/pricing.md` and `openai.com/chatgpt/pricing/` return 403 to
  this sandbox. They are labelled, not silently trusted.
- **Google's page is locale-shifted.** Without `gl=us` it served Spanish with no USD
  figures; the prices here are from an explicit US-locale fetch.
- **No plan was subscribed to and no authenticated request was made** in this pass. These
  are list prices read from pages.
- **The anonymous-access probe from 2026-10-02 is not repeated here.** Its result — 1 of 25
  free-tier endpoints answers without a key — still stands.

## Workload test

A working day is ~10 hours. Whether a plan survives it is a question about the **windows**,
not the total, and the vendors answer it differently:

| Plan | Window structure | 10 hrs/day reachable? |
|---|---|---|
| OpenCode Go | 5h = 20 %, weekly = 50 %, monthly = 100 % of a $ ceiling | yes on the ceiling maths, but 5h × 5 = month means the 5h window is the binding constraint, not the day |
| Z.ai GLM | 5h credits + weekly credits, dynamically refreshed | yes; the 5h credit pool refreshes 5h after *consumption*, which is not a fixed daily window |
| MiniMax | 5h rolling + weekly | yes on the same rolling basis |
| Trae / Factory / Warp | monthly usage value | no daily gate; the month is the constraint |
| Copilot | base credits + flex per month | no daily gate |
| Meta Muse | prompts per 5h **and** weekly | the 5h window is binding |

The honest summary is that **no provider in this market publishes a per-day figure**, and
none of these rows should be read as one.
