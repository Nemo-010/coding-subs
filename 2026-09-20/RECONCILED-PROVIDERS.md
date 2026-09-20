# Reconciled provider study: `Wei-Shaw/sub2api` + `router-for-me/CLIProxyAPI`

**Date 2026-09-20.** Pins: sub2api `19794bc46afb`, CLIProxyAPI
`61fdfc341b96`. This file reconciles the two
gateways: what providers each actually supports, what they have in common, and a
short recommended shortlist per category. Code-grounded surface for sub2api
alone (models.dev, account types) is in [PROVIDER-SUPPORT.md](PROVIDER-SUPPORT.md).

Machine-readable output of the new miner:
[data/providers-sub2api.csv](data/providers-sub2api.csv),
[data/providers-cliproxyapi.csv](data/providers-cliproxyapi.csv),
[data/providers-union.csv](data/providers-union.csv) (plus `.jsonl` evidence).

---

## 1. Why this file exists

The first pass ranked one repo's sponsor table. The second pass (sub2api only)
found ten platforms and a 222-provider registry. This pass adds the second repo
and — more importantly — a **structure-agnostic miner** so neither has to be
hand-read again:

```sh
tools/research-providers.sh OUTDIR NAME=PATH_OR_URL [NAME=PATH_OR_URL ...]
# e.g.
tools/research-providers.sh 2026-09-20/data \
    sub2api=/workspace/sub2api \
    cliproxyapi=https://github.com/router-for-me/CLIProxyAPI
```

The miner (`tools/mine-providers.py`) reads eight independent signals —
provider-like directories, symbolic constants, switch labels, JSON registries,
YAML config, markdown tables, markdown link hosts and a provider vocabulary —
and merges them with a `confidence` column. A repo whose layout changes is still
covered; new names are caught by the vocabulary. `tools/reconcile-providers.py`
merges per-repo lists into `providers-union.csv`.

---

## 2. CLIProxyAPI's provider surface (code-grounded)

CLIProxyAPI is architecturally different from sub2api: it does not resell relay
accounts, it proxies **CLI/subscription credentials** (OAuth) and any
OpenAI-compatible upstream defined in config.

| layer | what it is | evidence |
|---|---|---|
| protocol constants | `gemini`, `gemini-interactions`, `codex`, `claude`, `openai`, `openai-response`, `antigravity`, `interactions` | `internal/constant/constant.go:8-29` |
| auth providers (OAuth) | `antigravity`, `claude`, `codex`, `devin`, `kimi`, `meta`, `vertex`, `xai` (+ `empty`) | `internal/auth/` directory listing |
| model registry tiers | `claude`(16), `gemini`(14), `vertex`(21), `gemini-cli`(7), `aistudio`(16), `codex-free`(4), `codex-team`(6), `codex-plus`(7), `codex-pro`(7), `kimi`(10), `antigravity`(12), `xai`(10), `meta`(5) = **135 models** | `internal/registry/models/models.json`; struct at `internal/registry/model_definitions.go:30-42` |
| extra registries | Devin and Codex client model files | `internal/registry/models/devin_models.json`, `codex_client_models.json` |
| README provider table | Anthropic, Antigravity, Kimi, OpenAI, xAI (5 rows) | `README.md:14-40` |
| sponsor table | 14 rows / 15 hosts | `README.md` Sponsor section |
| unbounded | OpenAI-compatible upstreams + plugins (a plugin may supply an auth *and* a model provider) | `config.example.yaml:100-131`; `internal/pluginhost/adapters.go` |

The README table advertises **5** providers; the code supports **8 auth
providers across 13 registry tiers**. That gap is the same class of error as the
sub2api pass, and the miner now closes it automatically.

---

## 3. The union (miner output)

`providers-union.csv`: **72 providers**, **31 present in both repos**.

By kind:

| kind | count | examples |
|---|---|---|
| first-party model vendors | 22 | openai, anthropic, google, xai, deepseek, kimi, zhipu, minimax, qwen, volcengine, baidu, xiaomi, nvidia, meta |
| OAuth/subscription agents | 13 | claude, codex, gemini, antigravity, kimi, xai, devin, cursor, kiro, trae, opencode, augment, codebuddy |
| aggregators / gateways | 4 | openrouter, perplexity, zenmux, zai |
| media | 1 | seedance/ark |
| relay (sponsor) providers | 18 | hao.ai, codex-everywhere, aiberm, aicodemirror, cubence, packyapi, cctk, pptoken, pp.dog, fenno, pateway, apikey.fun, lanox, nagora, openmodel, etok, aimzoon, aigocode |
| infra (proxies/CDN/payment/accounts) | 14 | bestproxy, rapidproxy, swiftproxy, colaproxy, duckip, proxy4free, roxybrowser, axisnow, veilx, apimart, qiniu, bmoplus, cyberpay, agentmarket |

The 31-in-both are the stable core: `openrouter, anthropic, baidu, deepseek,
google, grok, kimi, minimax, openai, qwen, vertex, xai, xfspark, zhipu, qiniu,
axisnow, apimart, bestproxy, rapidproxy, swiftproxy, apikey, fenno, pateway,
antigravity, claude, codex, gemini, kiro, opencode, trae` (plus `fenno` covering
FennoAI).

---

## 4. Cross-repo reconciliation of the relay market

The same vendors sponsor both projects, which lets the two sponsor pages be
checked against each other. Discrepancies found:

| vendor | sub2api README says | CLIProxyAPI README says | verdict |
|---|---|---|---|
| RapidProxy | residential **$0.65/GB** | residential **$0.55/GB** | same vendor, two prices — at least one sponsor page is stale; neither is fetch-verified |
| Bestproxy | no price | **$0.5/GB**, $3/IP static, $67/day unlimited | CLIProxyAPI page is more specific |
| Swiftproxy | no price | **$0.7/GB** | CLIProxyAPI page is more specific |
| PatewayAI | "top-ups from 60% off", $3 trial | "Economy mode from **5% of official**" | framing differs; 5% is the stronger claim |
| APIMart | GPT-Image-2 from $0.006/image | same | agree |
| FennoAI | $50 credit for **$1.99** | same | agree |
| Qiniu | 150+ models, 12M/3M free tokens | same | agree |

New AI-relay vendors only in CLIProxyAPI (not in the sub2api table): **Aiberm**
("85–90% off Claude, 90% off GPT, 80% off Grok"), **AICodeMirror** ("Claude 38%,
Codex 2%, Gemini 9% of original price"), **Cubence**, **PackyCode**, and
**FluxA + Baidu AgenticPlan** ("Baidu Qianfan TokenPlan at 60% of standard").

Cross-repo price claims were fetched for reachability only. All six CLIProxyAPI
sponsor endpoints answered HTTP 200 through the reverse proxy; the OAuth
subscription vendors (Aiberm, PackyPay, AICodeMirror pricing) render client-side,
so **their prices could not be read from static HTML** and stay `ADVERTISED`.
Cubence's `/pricing` page does serve a static model table (Base $10/$50,
$1/$5, $5/$25 — i.e. first-party-shaped rates), captured in
`sources/cliproxyapi/`.

---

## 5. Recommended shortlist (top 3 per category)

Grades: **V** = a price page was fetched and read; **A** = sponsor copy only;
**U** = not published/readable. "Reliable" here means billing transparency, not
account safety or delivered-model identity.

### Best deal overall
1. **hao.ai — 0.15× official, published per-model card** (V) — the only
   fully checkable discount found across both repos.
2. **FennoAI — $50 coding-plan credit for $1.99** (A, in both repos) — best
   headline value, but one-time and subscription-shaped.
3. **Cubence — model table at first-party base rates** (V listing) — least
   aggressive discount, highest disclosure.

### Cheapest
1. **CodexEverywhere — 0.03× Plus Pool** (A, self-declared unstable).
2. **AICodeMirror — Codex at 2% of official** (A) — cheapest specific claim,
   entirely unverified.
3. **Aiberm — Claude/GPT/Grok at 10–15% of official** (A).

### Best free entry
1. **FennoAI — $50 credit for $1.99** (A).
2. **Qiniu — 12M enterprise / 3M developer free tokens** (A, both repos).
3. **CodexEverywhere — $20 trial** (A).

### Most "reliable" (transparency, not uptime)
1. **Qiniu (02567.HK)** (A) — listed company, largest catalogue claim (150+).
2. **Cubence** (V listing) — publishes per-model base rates.
3. **PatewayAI** (A) — official-channel claim plus contracts/invoicing.

---

## 6. What this pass did NOT establish

1. **Any price read from a JS-rendered page.** Aiberm/PackyAPI/AICodeMirror
   pricing is client-side; their claims remain `ADVERTISED`.
2. **Fulfilment or model authenticity** for any cheap rate.
3. **Plan prices for the 21 coding-plan products** in models.dev (the registry
   carries no plan price).
4. **Uptime.** Reachability only (six endpoints, one probe each).
5. **That the miner is complete.** It is heuristic. `--min-confidence high`
   narrows to code-declared providers; the default keeps vocabulary hits from
   provider-relevant files. Anything mentioned only in an image or a login wall
   is invisible to it.

## 7. Reproduce

```sh
sh tools/research-providers.sh 2026-09-20/data \
    sub2api=/workspace/sub2api cliproxyapi=/workspace/CLIProxyAPI
python3 tools/validate.py 2026-09-20
```

The miner needs no dependencies beyond Python 3.8 and `git` (when given a URL).
