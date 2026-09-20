# sub2api provider-support surface (correction to the first pass)

## Why this file exists

The first version of this pass ranked the **26 rows of the README sponsor table**
and presented that as "the provider universe". That was wrong. The sponsor table
is who pays for the project. The provider surface the code actually supports is
much larger, and it lives in three places the first pass never opened:

1. the platform/account-type registries in `backend/internal/domain/constants.go` and
   the per-platform services;
2. the **models.dev** registry that `upstream_models.go` fetches to attach model
   metadata to `upstream` (BYO base-url) accounts — 222 providers, 7,868 models;
3. the remote pricing catalog (`Wei-Shaw/model-price-repo`), a filtered LiteLLM dump.

Everything below is at the pinned commit `19794bc46afb` (2026-09-20) unless stated.
Evidence is file:line against that commit. Data files in `data/`.

---

## 1. What sub2api "supports", precisely

### 1.1 First-class platforms (code enum)

`backend/internal/domain/constants.go:20-35` defines exactly these, and the request
router, schedulers, quota windows and billing branches key off them:

| platform | value | note |
|---|---|---|
| Anthropic | `anthropic` | |
| OpenAI | `openai` | |
| Gemini | `gemini` | native |
| Antigravity | `antigravity` | added #73, merged 2025-12-29 |
| Grok / xAI | `grok` | added #3310, merged 2026-06-26 |
| Kimi (Moonshot) | `kimi` | payg + Coding Plan |
| Zhipu GLM | `zhipu` | payg + Coding Plan |
| DeepSeek | `deepseek` | payg + coding |
| MiniMax | `minimax` | added #6758, merged 2026-09-08 |
| OpenCode | `opencode_go` | Zen/Go, added #6747, merged 2026-09-11 |
| Composite | `composite` | routing group, not an upstream |

`backend/internal/domain/constants.go:55-63` defines the account types, which are the
other half of the surface:

`oauth`, `setup-token`, `apikey`, **`upstream`** (BYO base-url + API key),
`bedrock` (AWS SigV4), `service_account` (Vertex AI).

The `upstream` type is the unbounded one. Any OpenAI- or Anthropic-compatible
endpoint can be attached (`domain/constants.go:61`; custom base URL in
`service/account.go:2478`). This is what makes "hundreds of providers" true rather
than rhetorical.

### 1.2 Platforms reached through the pricing catalog

`backend/internal/config/config.go:2292` sets

```
pricing.remote_url = https://raw.githubusercontent.com/Wei-Shaw/model-price-repo/main/model_prices_and_context_window.json
```

The bundled fallback `backend/resources/model-pricing/model_prices_and_context_window.json`
has 244 entries across 13 provider tags; the remote file (fetched 2026-09-20, 285,937 B)
has the same 13 tags: openai, anthropic, gemini, vertex_ai-language-models,
vertex_ai-embedding-models, bedrock, xai, deepseek, moonshot, volcengine, zhipu,
minimax, text-completion-openai. The upstream of that repo is LiteLLM, which carries
far more; Wei-Shaw's repo filters it.

### 1.3 The models.dev registry (the actual "hundreds")

`backend/internal/service/upstream_models.go:23`

```go
modelsDevRegistryURL = "https://models.dev/api.json"
modelsDevRegistryTTL = 6 * time.Hour
```

Fetched at `:532-575`, parsed into `modelsDevProvider`/`modelsDevModel` (`:61-88`), and
matched to an account by API URL or known host at `:643-720`. Its whole purpose is to
enrich a BYO-upstream account's model list with capability metadata (reasoning options,
modalities, context/output limits) that the vendor's own `/models` endpoint omits.

Fetched live on 2026-09-20 (`https://models.dev/api.json`, 4,710,664 B):

- **222 providers**
- **7,868 models**
- 212 providers carry at least one `cost` object
- 178 have at least one strictly paid model
- **75 carry at least one `cost: 0` route** (free tier or subscription-plan route)

`data/modelsdev-providers.csv` is the full 222-row table; `data/cheapest-per-model.csv`
ranks the paid listings; `data/subscription-plan-providers.csv` lists the 75 plan/free
routes.

> Caveat that matters: `cost: 0` in models.dev means *that provider does not bill per
> token on that route*. It does **not** mean the plan is free. models.dev carries no
> plan price. The 21 providers whose id contains `coding-plan`/`token-plan` are
> subscription products; their monthly price is not in this dataset.

### 1.4 Vendors named in the tracker but NOT first-class at the pinned commit

Checking merge state, these are open PRs, not shipped support:

| vendor | PR | state |
|---|---|---|
| Kiro (Amazon Q) | #6777 | open (only a legacy `PlatformKiro` test constant exists) |
| Devin (Cognition) | #7171 | open |
| Cursor | #6289 | open |
| Qoder | #5035 | open |
| Alibaba Token Plan / qwen | #6748 | open |
| MiniMax Token Plan full | #6404 | open (basic MiniMax #6758 is merged) |
| GitHub Copilot | #1449 | closed, never merged |

Vendors that ARE in the pinned tree and merged: Ollama Cloud (#4850, #6388, #6769),
Seedance / Volcengine Ark (`service/seedance.go`, #7247), AWS Bedrock (#2642),
Vertex AI (#1618), Grok media/image/video (`service/grok_media.go`).

---

## 2. What the sponsor table really is

- 26 `<tr>` rows in `README.md` at the pinned commit; the live `main` README on
  2026-09-20 is byte-identical in the sponsor section (26 hosts, no additions/removals).
- 17 rows are AI API/relay providers, 9 are proxy/CDN/browser infra.
- `assets/partners/logos/` holds **32** files, i.e. **6 orphaned logos** with no
  sponsor row in any of README.md / README_CN.md / README_JA.md: `ctok.png`,
  `fastaitoken.jpg`, `pincc-logo.png`, `poixe.png`, `runapi.png`, `silkapi.png`.
  Their domains are unverified (the clone is shallow, so no git history).

So the sponsor list is 26, not the provider universe, and it is *not even the complete
list of past sponsors* — it undercounts the project's own asset directory.

---

## 3. Rankings that follow from the real surface

### 3.1 Cheapest paid listing per reference model

From `data/cheapest-per-model.csv` (USD per 1M tokens, paid routes only, top of each
list). Full lists in the CSV.

| model | cheapest listing | in | out | vs first-party |
|---|---|---|---|---|
| claude-sonnet-4-6 | Xpersona | 0.90 | 5.55 | ~0.37x of Anthropic's 3/15 |
| claude-opus-5 | (parity floor) | 5.00 | 25.00 | 1.00x |
| gpt-6-astra | Ofox | 8.00 | 40.00 | 0.80x of OpenAI's 10/50 |
| gpt-5.5 | UnoRouter | 0.19 | 1.13 | ~0.03x |
| gemini-3-pro | Poe | 1.60 | 9.60 | ~0.8x of 2/12 |
| grok-4.6 | many at parity | 2.00 | 6.00 | 1.00x |
| qwen3.7-max | Merge Gateway | 0.83 | 2.48 | below 1.25/3.75 median |

The dominant finding is **parity**: of the 40 providers listing Claude Sonnet 4.6, the
overwhelming majority price at exactly Anthropic's 3/15. The registry is mostly
official-price reseller gateways. The cheap tail exists (Xpersona, Ofox, UnoRouter) but
is a minority and, unlike the relay table, carries no independent fulfilment evidence.

### 3.2 Subscription/plan routes

75 providers expose at least one `cost: 0` route. The largest are NVIDIA NIM (101
models), Kenari (59), OpenCode Zen (32), Alibaba Token Plan (28 x2 regions), Kilo (26),
GitLab (25), SCNet Token Plan (19), Alibaba Coding Plan (10), Volcengine Ark (10),
Tencent Coding Plan (8), Z.AI Coding Plan (7), MiniMax Coding Plan (7 x2 regions),
Xiaomi Token Plan (7 x3 regions), Kimi For Coding (4 x2 regions), Zhipu AI Coding Plan (4).

`data/subscription-plan-providers.csv` has the endpoint for each, which is what an
operator would paste into an `upstream` account. This is the actionable version of
"cheapest plans": it tells you *which routes are plan-backed and where their base URL
is*, not what the plan costs.

---

## 4. What this analysis did NOT establish

Stated first, per methodology:

1. **Plan prices.** models.dev has none. Ranking the 21 coding-plan products by price
   requires fetching each vendor's pricing page; not done here.
2. **Fulfilment / model authenticity** of the below-parity listings. A cheap `cost`
   field is a claim in a third-party registry, not a served-token verification.
3. **That sub2api itself uses the registry's prices.** It does not: the `modelsDevModel`
   struct (`upstream_models.go:68-76`) has no cost field. The cost ranking is my
   analysis of the registry, not a sub2api feature.
4. **Kiro/Devin/Cursor/Qoder support.** Open PRs, absent from the pinned tree.
5. **The 6 orphan logos' domains.** No referenced URL; clone is shallow.
6. **Any provider not in models.dev and not in the sponsor table.** The `upstream`
   account type accepts them, so the true count is unbounded and unenumerable from the
   repo alone.

## 5. Reproduce

```sh
curl -s https://api.rv.pkgforge.dev/https://models.dev/api.json -o modelsdev.json
python3 -c 'import json;d=json.load(open("modelsdev.json"));print(len(d),sum(len(v["models"]) for v in d.values()))'
```

Re-fetch of the sponsor table and the remote pricing catalog is in `sources/README.md`.
