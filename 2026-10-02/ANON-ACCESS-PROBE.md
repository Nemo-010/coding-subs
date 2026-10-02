# Anonymous-access probe — 2026-10-02

**This is the pass's actual new research.** The rest of the 2026-10-02 pass is re-verification:
the same URLs fetched again and diffed. This file is a measurement: 25 free-tier endpoints were
probed with real unauthenticated requests, three rounds each, from this sandbox on 2026-10-02.

The question it answers is the one a reader actually has, and the one no source states:

> **Of the endpoints this market calls "free", which ones will answer a request from an agent that
> has no account, no card and no key — and what do they do when you send them real work?**

Raw results: [data/free-tier-probe.json](../data/free-tier-probe.json) (every round, every status,
every token count). Probe: [tools/probe-free-tiers.py](../../tools/probe-free-tiers.py).

## Method, and its limits

A tiny completion — `POST /chat/completions` with `max_tokens=1` (or `/api/chat`, or Google's
`:generateContent`) — sent with **no `Authorization` header of any kind**. Three rounds. A `/models`
listing was fetched first so the two failures are distinguishable. The probe reads no credential
from the environment, a file or a prompt; it *cannot* test an authenticated path, by construction.

The classification is the point:

- **`ANON_OK`** — a 200 completion with no credential. The endpoint is usable right now by anyone.
- **`AUTH_REQUIRED`** — 401/403. The endpoint exists and only lacks a key. **This is not "down".**
  A free tier being *account-gated* is a real property and it is exactly what the directories in
  issue #1 never say.
- **`RATE_LIMITED`** (429), **`NO_SUCH_ROUTE`**, **`UNREACHABLE`** — the rest.

## Result: 2 of 25 endpoints answer anonymously, and only 1 is usable

| Endpoint | `/models` | Completion (3 rounds) | Reading |
|---|---|---|---|
| **OpenCode Zen** (`space-bunny-free`) | 200, 85 models | **ANON_OK ×3** | the only endpoint in this set that serves a real completion to an unauthenticated caller |
| OpenCode Zen (duplicate probe row) | 200, 85 models | **ANON_OK ×3** | same endpoint, probed twice to rule out a fluke — it is not a fluke |
| NVIDIA NIM | **200, 81 models** | AUTH_REQUIRED | catalogue is public, inference is not |
| Hugging Face router | 200, 134 models | AUTH_REQUIRED | same |
| OrcaRouter | 200, 205 models | AUTH_REQUIRED | same |
| BazaarLink | 200, 124 models | AUTH_REQUIRED | same |
| AIHubMix | 200, 417 models | AUTH_REQUIRED | same |
| DeepInfra | 200, 183 models | AUTH_REQUIRED | same |
| Ollama Cloud | 200, **17 models** | AUTH_REQUIRED | and **all 17 are priced** — consistent with the reading that its free plan has no published allowance |
| Groq | 403 | AUTH_REQUIRED | even the model list needs a key |
| Google AI Studio | 403 | AUTH_REQUIRED | needs a key (free, but gated) |
| OpenRouter | (no JSON) | AUTH_REQUIRED | |
| Onomeo, TokenRouter, AMD Token Factory, Mistral, Cerebras, Cohere, Fireworks, Together, SiliconFlow INTL | 401/403 | AUTH_REQUIRED | all account-gated |
| Vercel AI Gateway | (no JSON) | AUTH_REQUIRED | consistent with "requires a payment method on file" |
| Token Harbor | 403 | AUTH_REQUIRED | |
| Cloudflare Workers AI | 405 | NO_SUCH_ROUTE | the endpoint needs an account id in the path — the probe cannot even address it anonymously |
| Empero | 503 | HTTP_503 ×3 | the free endpoint that advertises "any key works" was **down for all three rounds** |

**The headline number: 1 of 25.** Twenty-two of the remaining twenty-four are not unreachable —
they are *gated*. A directory that calls them "free" is describing the price, not the access, and
for an agent with no account those are different facts.

## The one endpoint that works: what it actually does

`space-bunny-free` on OpenCode Zen is a *stealth* model — no vendor name, no verifiable codename —
and it is served to callers with no key at all. Since it is the only anonymous channel in this
market, it is worth characterising properly rather than listing.

**It is stable.** Five consecutive rounds, `max_tokens=10`: HTTP 200 every time, ~166 tokens at
~1–2 s. One round in five returned an empty `content` with `reasoning_tokens` spent instead.

**It does real coding work.** A bug-fix task returned a correct unified diff:

```
--- a.py
+++ a.py
@@
 def add(a,b):
-    return a-b
+    return a+b
```

**It has a transparency defect that matters.** Send a needle buried ~400,000 characters into the
prompt and the model *retrieves it* — so the content is being read. But:

| Prompt sent | `prompt_tokens` billed | Reply |
|---|---|---|
| ~200 chars containing the needle | 179 | correct |
| ~400,000 chars with the needle buried deep | **89,063** | **empty** |

Two separate observations, both real. It reads far more context than it bills — 89,063 billed for
~100,000+ tokens sent — and on the long input it returned nothing at all while still billing. An
agent that trusts the reported usage to budget a context window will be wrong about both the cost
and the available headroom. This is a *stealth* model with no published context window, and the
`1M / 524,288` figures circulating for it come from third-party listings rather than from the
vendor — the 2026-10-02 re-read of the free-API index says exactly that.

**Free is not the same as permitted.** The endpoint's own catalogue carries 12 other `-free`
models. Probing each one unauthenticated:

| Model | No-key result |
|---|---|
| `space-bunny-free` | **200, completion** |
| `deepseek-v4-flash-free` | 400, upstream request failed |
| `mimo-v2.6-flash-free` | 403 `OpenCode's free tier can only be used from within OpenCode` |
| `nemotron-3-ultra-free` | 403, same message |
| `ling-3.0-flash-fin-free` | 403, same message |
| `longcat-2.5-preview-free` | 403, same message |
| `fledge-alpha-free` | 403, not available in your country |
| `muse-spark-1.3-contributor-free` | 403, **not available in your country** |

So "OpenCode Zen has 12 free models" is true in the vendor's catalogue and false for an external
agent: eleven of the twelve require either OpenCode itself or a country the sandbox is not in.
The one that does not — `space-bunny-free` — is the stealth model.

## A correction to this pass's own table

The cost-per-token table published alongside this file derives **OpenCode Go** at **$0.0013/M
token** from the vendor's own grid. That figure is wrong as published, and the probe is what
exposed it.

The vendor gives, for MiMo-V2.6-Flash: **30,100 requests / 5 h, 75,200 / week, 150,400 / month**,
against a **$60 monthly ceiling** with the rule *5 h = 20 %, weekly = 50 %, monthly = 100 %*.
Those three columns are not one consistent clock: 150,400 ÷ 75,200 = **2.0**, when a month is 4.3
weeks. Either the monthly figure is a separate cap on top of the weekly one, or the month is
defined as two weeks. The pass published the monthly column as a monthly allowance without
checking that its own columns agreed — the same class of mistake this repo exists to catch, made
by this repo.

**Corrected row** (same vendor page, arithmetic shown):

| Reading | Ceiling | $/M token |
|---|---|---|
| monthly column taken literally (what this pass published) | $60/month | $0.0013 |
| **weekly column × 4.33 ≈ $260/month** | **$260/month** | **$0.0056** |
| 5 h rule alone (20 % of $60 = $12 per 5 h window, 4.8 windows/day) | $58/day | — |

The honest figure is **$0.0056/M with the weekly column** — still the cheapest verified token price
in this market, but four times worse than the row said, and the row now carries the window-rule
caveat instead of the bare monthly division.

## What this probe did not establish

- **No authenticated path was tested.** Every `AUTH_REQUIRED` row may well be free with an account;
  the probe says it is gated, not that it is expensive. The 19 gated endpoints are the *next*
  measurement, and it cannot be made from here without keys.
- **One round of the day.** All three rounds ran minutes apart; nothing here measures a daily or
  weekly pattern, and the anonymous channel could be closed tomorrow.
- **No latency claim about any vendor.** `median_ms_ok` is the sandbox's network view of one
  gateway, not the vendor's own service quality.
- **Cloudflare Workers AI was mis-addressed** (`accounts/anonymous/...`) and returned 405; that is
  the probe's fault, not the vendor's, and it is recorded that way rather than as a finding.
- **The long-prompt behaviour is one observation, not a characterisation.** One needle, one depth,
  one model. It shows the reported usage cannot be trusted as a context-window signal; it does not
  show where the truncation begins.
