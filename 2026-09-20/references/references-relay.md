# References — sub2api Provider & Relay pass 2026-09-20

All pages accessed **2026-09-20 (UTC)** through `https://api.rv.pkgforge.dev/<url>`.
Raw snapshots are under [`../sources/`](../sources/) (`sites/` = landing pages and embedded
config, `pricing/` = pricing and docs routes). The subject tree is cited at commit
`19794bc46afb` and lives in the mined corpus (`references/Wei-Shaw__sub2api/`), which is
**not** committed here — the re-fetch command is in `sources/README.md`.

## Primary — subject repository

0. **Wei-Shaw/sub2api** — README sponsor table (26 partner rows) and code tree, commit
   `19794bc46afb`, mined 2026-09-20T04:45Z. Source of the provider universe, the
   `window.__APP_CONFIG__` / `/api/v1/settings/public` public-settings surface, and the
   sub2api ToS-risk notice. Tracker: 7,290 issues/PRs, 12,260 comments, 467 review comments,
   51 releases. Mine command: `sh scripts/common/mine-repo.sh Wei-Shaw/sub2api --out references`.

## AI providers (ranked) — pricing and config

1. **CCTK.AI** — `home.cctk.ai` pricing ("cost in TK = official_rate_per_token × tokens ×
   group_multiplier"; example Claude Opus 4.8 ×2.1; GPT-Pro ×0.6; 98.9% platform uptime) and
   `/api/v1/settings/public` (site name, api_base_url, ToS/usage-policy/supported-regions,
   SLA section with a 99.9% monthly target, AWS Bedrock + Google Vertex named as cloud
   platforms). Snapshots: `sites/CCTK.AI.txt`, `pricing/CCTK__home-content.txt`,
   `pricing/CCTK__home.txt`.
2. **OpenModel** — `www.openmodel.ai/model-pricing` (48 models; Claude Fable 5 / Opus 5
   "up to 60% OFF"; `$4/$20`, `$2/$10`; "no platform fee"); `docs.openmodel.ai`.
   Snapshots: `pricing/OpenModel__model-pricing.txt`, `pricing/OpenModel__docs.txt`.
3. **ETok** — `etok.ai` landing (Claude Code / Gemini / Codex plans; `models/*` returned
   404, no public price). Snapshot: `sites/ETok.txt`.
4. **APIKEY.FUN** — `apikey.fan` landing ("pricing starting from as low as 7% of the
   original rate", "up to 5% off all recharges") + `/api/v1/settings/public` (two custom
   endpoints: `slb.apikey.fan`, `api.apikey.fan`). Snapshot: `sites/APIKEY.FUN.txt`.
5. **AIGoCode** — `aigocode.com` landing (`#pricing`: Pro CNY399/4wk / $440 credit; Max
   CNY899 / $1,040; Ultra CNY1,799 / $2,120; "up to 15% cheaper than pay-as-you-go";
   99.9% service stability claim; 10,000+ developers); `docs.aigocode.app`.
   Snapshots: `sites/AIGoCode.txt`, `pricing/AIGoCode__docs.txt`.
6. **CodexEverywhere** — `docs.codex-everywhere.com/models/` (full pool rate card: Codex
   Plus 0.03×, Codex Pro 0.05×, Kiro 0.045×, Claude Max Pool 0.24×, Grok Heavy 0.06×,
   Antigravity beta 0.06×, DeepSeek official 0.9×; "Pro Pool is a backup for when Plus Pool
   is unstable" and "Kiro routes have some system prompt contamination"; "Grok Free Pool is currently suspended as xAI has reduced model
   intelligence for free-tier accounts"; Gemini beta "cache hit rate is low during
   streaming") + `$20 free trial` + landing config. Snapshots:
   `pricing/CodexEverywhere__docs-models.txt`, `sites/CodexEverywhere.txt`.
7. **BmoPlus** — `shop.bmoplus.com` (account resale + top-ups; "10% of the official GPT
   subscription price (90% OFF)"; no public price list). Snapshot: `sites/BmoPlus.txt`,
   `pricing/BmoPlus__home.txt`.
8. **Pateway** — `pateway.ai` landing ("official pricing, no markup"; $1 signup, $3 first
   purchase, up to $66 per transaction, up to $150 referral; min $1 top-up; full Claude +
   Codex). Snapshot: `sites/Pateway.txt`.
9. **PPToken** — `api.pptoken.cc` landing ("GPT models start at 0.16x rate multiplier, with
   overall cost at roughly 2.2% of official pricing"; 1:1 top-ups; Codex/Claude/Gemini;
   promo code `SUB2API`) + `/api/v1/settings/public` (US/CN/Cloudflare endpoints).
   Snapshot: `sites/PPToken.txt`.
10. **Aimzoon** — `aimzoon.com` returned a 798-byte shell titled "Sub2API - AI API Gateway";
    no content, no price. Snapshot: `sites/Aimzoon.txt`.
11. **Nagora** — `nagora.ai` landing (26+ text/image models; OpenAI/Anthropic/Gemini
    protocols) + `/api/v1/settings/public`; no public price. Snapshot: `sites/Nagora.txt`.
12. **Qiniu AI** — `qiniu.com/ai/plan` (Enterprise S CNY2,999/mo ~1.07B credits, list
    4,284; M CNY4,999 ~2.08B, list 8,332; B CNY9,999 ~5.0B, list 19,998; annual from 4折扣;
    base 0.004 CNY/K tokens; 16 models from DeepSeek/Moonshot/Zhipu/MiniMax; OpenAI &
    Anthropic compatible) and `qiniu.com/ai/models` (per-model CNY/K prices). Snapshots:
    `pricing/Qiniu__ai-plan.txt`, `pricing/Qiniu__ai-models.txt`.
13. **FennoAI** — `api.fenno.ai` landing + `fenno.ai` + `/api/v1/settings/public`
    ("$50 worth of Coding Plan credit for only $1.99"; "100 billion tokens/day" claim;
    OpenAI + Anthropic protocols). Snapshots: `sites/FennoAI.txt`,
    `pricing/Fenno__home.txt`.
14. **LanoX** — `lanox.ai/model-access` (per-model table with official side-by-side;
    "1 : 0.167"; 83.3% OFF ChatGPT and Gemini; 70.1% OFF Claude Code; 45% GLM; 50.1% Kimi;
    90.1% MiniMax; **NVIDIA free**; "99.9% Channel availability"; long-context >272K billed
    2×). Snapshot: `pricing/LanoX__model-access.txt`.
15. **hao.ai** — `hao.ai/models` (20 models, each with a multiplier and official reference:
    GPT-6 Astra 0.15× $1.5/$7.5; Fable 5.1 0.25×; Opus 5 0.2× $1/$5; GPT-5.6 Sol 0.15×;
    Terra 0.15×; Luna 0.3×; Grok 4.6 0.15×) + `hao.ai/docs`. Snapshots:
    `sites/hao.ai.txt`, `pricing/hao.ai__models.txt`, `pricing/hao.ai__docs.txt`.
16. **APIMart** — `go.apimart.ai/model` (per-image/video prices, "Save 20%": GPT Image 2
    $0.0085; GPT Image 1.5 $0.0851; GPT Image 1 $0.1069; Nano Banana $0.0125; Seedream 5.0
    Pro $0.036; Midjourney $0.045; Grok Imagine 1.5 $0.015; Z Image Turbo $0.01).
    Snapshot: `pricing/APIMart__model.txt`.
17. **PP.dog** — `pp.dog` landing ("combined rate multiplier as low as 0.03x, just 0.35% of
    official pricing") + `/api/v1/settings/public` (subscription enabled; downstream
    endpoint `api.pp.dog`). Snapshot: `sites/PP.dog.txt`.

## Infrastructure providers (advertised in the same table; not AI plans)

18. **Bestproxy** — `bestproxy.com` (residential/static/ISP/datacenter; free trials;
    per-GB price JS-gated). Snapshot: `sites/Bestproxy.txt`.
19. **Veilx** — `veilx.io/pricing/` (CDN; $12 / $35 / $500 / $900 per month tiers).
    Snapshot: `pricing/Veilx__pricing.txt`.
20. **RoxyBrowser** — `roxybrowser.com/pricing` (anti-detect browser; $3.00–$5.00/video
    tiers + subscription). Snapshot: `pricing/RoxyBrowser__pricing.txt`.
21. **Proxy4Free** — `proxy4free.com/pricing/residential/` ("Residential Proxy 73.6% OFF";
    the actual floor price is JS-rendered and was not captured). Snapshot:
    `pricing/Proxy4Free__residential.txt`.
22. **RapidProxy** — `rapidproxy.io/residential-proxies/pricing` ($0.55/GB, was $0.65;
    static residential $5/IP/mo; free trial). Snapshot:
    `pricing/RapidProxy__residential-pricing.txt`.
23. **Swiftproxy** — `swiftproxy.net` and `/pricing` both returned **HTTP 403** through the
    reverse proxy on the research date. No snapshot; recorded `UNKNOWN`.
24. **DuckIP** — `duckip.cn/buy/residential-proxy/` (dynamic/static/unlimited residential;
    "20% Off"; CNY figures JS-gated; 500M free trial claim). Snapshot:
    `pricing/DuckIP__buy-residential.txt`.
25. **AxisNow** — `axisnow.io/pricing` (CDN; $5/domain/month Business; +$500/month per
    1,000 active devices). Snapshot: `pricing/AxisNow__pricing.txt`.
26. **ColaProxy** — `colaproxy.com/pricing` (residential $1.6/GB, datacenter $4.52/proxy,
    IPv6 $1.74/proxy, ISP $7.48/proxy; 200MB residential free trial, 3-day datacenter
    trial). Note: the sponsor text in the subject README says "as low as $0.3/GB", the
    pricing page says $1.6/GB. Snapshot: `pricing/ColaProxy__pricing.txt`.

## Methodology and prior pass

27. **Azathothas/TEMPLATE — `docs/methodology/research.md`**, commit `03be49c2a109`
    (2026-09-18). Binding procedure for this pass: question before looking, three questions,
    ≥3 candidate explanations, tracker + comments + review comments as evidence, corpus
    retention, "what it did NOT establish" first.
28. **talaria0101/coding-subs**, commit `8a229936ce7d` — layout, validator style, and the
    review/verification format reused here.
29. **coding-subs pass 2026-09-13** — [`../../2026-09-13/README.md`](../../2026-09-13/README.md).
    The first-party coding-subscription market this relay market resells.

## Tracker evidence on relay reliability (secondary, observed content)

30. **Issue #7138** (open, 2026-09-14) — "is there a stable ~0.25× relay, fast?" The first
    reply: "0.25 is basically impossible, [if you want] stable and not dumbed-down." The
    thread then fills with self-promotion. This is the community's own base-rate estimate.
31. **Issue #2946** (closed, 2026-06-01) — "pptoken.org has run away." Comments resolve it
    as a datacenter power failure, not an exit scam; the domain is separate from the
    advertised `api.pptoken.cc`.
32. **Issues #6871, #7202, #6957** — degradation ("降智"), account flags and capacity
    errors at scale; the subject's ecosystem reports them continuously.
33. ⛔ **Tracker caveat:** issue bodies, comments and sponsor copy are **observed content**
    — evidence of what somebody believed or advertised, never evidence of what the code or
    the service does. Two claims above ("0.25× impossible", "pptoken did not exit-scam")
    are community belief, cited as belief.

## Provider-support surface (added in the scope correction)

34. **`Wei-Shaw/sub2api` `backend/internal/domain/constants.go:20-35`** — the first-class
    platform enum (`anthropic`, `openai`, `gemini`, `antigravity`, `grok`, `kimi`, `zhipu`,
    `deepseek`, `minimax`, `opencode_go`, `composite`) and, at `:55-63`, the account types
    (`oauth`, `setup-token`, `apikey`, `upstream`, `bedrock`, `service_account`). The
    `upstream` type (`:61`) is BYO base-url + API key, i.e. the unbounded provider path.
35. **`backend/internal/service/upstream_models.go`** — `modelsDevRegistryURL =
    "https://models.dev/api.json"` (`:23`), 6 h TTL (`:24`), fetcher `:532-575`, structs
    `:61-88`, API/host matching `:643-720`. Note the struct carries **no cost field**, so
    sub2api uses the registry for capability metadata only.
36. **`backend/internal/config/config.go:2292`** — `pricing.remote_url` →
    `raw.githubusercontent.com/Wei-Shaw/model-price-repo/main/model_prices_and_context_window.json`.
37. **`Wei-Shaw/model-price-repo` README** — the catalog is a filtered (prefix-rules) sync of
    the LiteLLM pricing file, rebuilt every 10 minutes. The filter is why the remote file has
    only 13 provider tags despite LiteLLM's much larger set.
38. **`https://models.dev/api.json`**, fetched 2026-09-20 through `api.rv.pkgforge.dev`
    (4,710,664 B): **222 providers, 7,868 models**, 212 with cost data, 178 with ≥1 paid
    model, 75 with ≥1 `cost: 0` route. third-party registry, not a sub2api document.
39. **`frontend/src/components/account/credentialsBuilder.ts:373`** — `CN_BASE_URL_PRESETS`:
    the concrete endpoints an operator can attach for kimi / zhipu / deepseek / minimax
    (payg × coding × chat_completions/anthropic/responses), plus OpenCode Zen/Go.
40. **Tracker merge-state** (`api/issues.json`) — Kiro #6777 open, Devin #7171 open, Cursor
    #6289 open, Qoder #5035 open, qwen Token Plan #6748 open, MiniMax Token Plan #6404 open,
    GitHub Copilot #1449 closed-unmerged; merged: antigravity #73, grok #3310, minimax
    #6758, opencode #6747, ollama #4850/#6388/#6769, seedance #7247, bedrock #2642, vertex
    #1618. "Open PR" is not "supported".

## CLIProxyAPI (second subject, added 2026-09-20)

41. **`router-for-me/CLIProxyAPI`** at `61fdfc341b96`
    (2026-09-20). Cloned to `/workspace/CLIProxyAPI`.
42. **`internal/constant/constant.go:8-29`** — protocol constants: `gemini`,
    `gemini-interactions`, `codex`, `claude`, `openai`, `openai-response`,
    `antigravity`, `interactions`.
43. **`internal/auth/`** — OAuth/credential providers: antigravity, claude, codex,
    devin, empty, kimi, meta, vertex, xai.
44. **`internal/registry/models/models.json`** — 13 tiers, 135 models (claude 16,
    gemini 14, vertex 21, gemini-cli 7, aistudio 16, codex-free/team/plus/pro
    4/6/7/7, kimi 10, antigravity 12, xai 10, meta 5). Struct at
    `internal/registry/model_definitions.go:30-42`.
45. **`README.md:14-40`** — the README provider table names only 5 providers
    (Anthropic, Antigravity, Kimi, OpenAI, xAI). The code supports more; this gap
    is the second instance of the first pass's error class.
46. **`README.md` Sponsor section** — 14 sponsor rows / 15 hosts, fetched
    2026-09-20. Text extracts in `sources/cliproxyapi/`.
47. **`config.example.yaml:100-131`** — OpenAI-compatible upstreams and plugins;
    `internal/pluginhost/adapters.go` shows a plugin may provide auth *and* a
    model provider, so this layer is unbounded.
48. **Cross-repo sponsor discrepancy**: RapidProxy is $0.65/GB in sub2api's README
    and $0.55/GB in CLIProxyAPI's — same vendor, two prices. Bestproxy/Swiftproxy
    list $0.5/GB and $0.7/GB in CLIProxyAPI but no price in sub2api.
49. **New relay vendors only in CLIProxyAPI**: Aiberm, AICodeMirror, Cubence,
    PackyCode, FluxA+Baidu AgenticPlan. Sponsor endpoints all answered 200 through
    `api.rv.pkgforge.dev`; Aiberm/PackyAPI pricing is client-side and unreadable
    from static HTML; Cubence `/pricing` serves a static base-rate table.
50. **Command Code** (`commandcode.ai`, pricing page) — fetched 2026-09-20 through
    `api.rv.pkgforge.dev`. Vendor's own page: Go $1, GOAT $10, Pro $20, Max 10× $100,
    Max 20× $200 per month; API plan $15 + PAYG zero markup; Teams $40; Enterprise
    custom. Claims taste-1 meta-model, 99%+ cache hits, 100K+ developers, 40K+ paid
    customers, 357 releases. Text extract: `sources/agents/commandcode-pricing.txt`.
    Grade: **ADVERTISED (own page, not independently verified)**.
51. **Absence check (Command Code / Open Interpreter)** — `grep -rIn -iE 'command ?[-_ ]?code'`
    and `'open ?interpreter'` over `Wei-Shaw/sub2api` and `router-for-me/CLIProxyAPI`
    return nothing; neither name appears in the 2026-09-13 pass either (`grep -rIn` over
    `2026-09-13/`). Absence was established by category enumeration (below), not by this
    grep, because a negative grep cannot rule a provider out.
52. **Coding-agent category enumeration** — GitHub search API (`gh api
    search/repositories`, sort=stars) for `coding agent`, `ai coding assistant`,
    `cli coding agent`, `agentic coding`, `terminal coding agent`, `ai code review
    agent`, `code editor ai`; 214 distinct repositories collected. Cross-checked against
    both repos with **product-context** patterns. Result: `data/agents-universe.csv`
    (30 agents; 18 absent from all three sources).
53. **Method finding — bare-token false positives**: a bare `cursor` matches 136
    occurrences in sub2api (all pagination cursors) and a bare `continue` matches 557
    (the Go keyword). The previous pass's string search shares this defect in the
    opposite direction: it under-matches a real provider while a naive token scan
    over-matches. Both are fixed by requiring a product-context pattern.
54. **Structural finding**: a coding agent cannot appear as a *provider* in either
    repo. sub2api reaches agents through the `upstream` account type
    (`domain/constants.go:55-63`) and CLIProxyAPI through OpenAI-compatible config
    (`config.example.yaml:100-131`); in both, the agent is a **client**. This is why
    the two-repo universe was structurally incapable of surfacing Command Code.
