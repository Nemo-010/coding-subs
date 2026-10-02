# References — 2026-10-02 pass

All first-party pages were fetched on **2026-10-02 (UTC)** directly from this network (no reverse
proxy) and are stored verbatim under [`../sources/`](../sources/). Third-party datasets referenced
by upstream issues #1 and #2 are stored there too, prefixed `thirdparty-`, and are cited as
THIRD-PARTY evidence — a dated snapshot of someone else's reading, never a first-party rate card.

## First-party — model landscape

1. **Artificial Analysis model list** — `artificialanalysis.ai/models`, fetched 2026-10-02. Source
   of every `aa_intelligence_index`, `release_date`, `context_window_tokens` and cost-per-task
   figure in `data/models-database.csv`. The page embeds a top-list chart (10 entries with II,
   release date and weighted cost per Intelligence Index task) and a per-model object carrying
   `intelligenceIndex`, `contextWindowTokens`, `isOpenWeights`, `cacheHitPrice`, `cacheWritePrice`,
   `terminalBenchScience`, `scicode`, `hle`, `mmmuPro` and the model-routing charts. Snapshot:
   `aa-models-page.html`. New in this pass: Claude Opus 5.5 (2026-09-22, II 57.62), Claude Sonnet 5.5
   (2026-09-28, II 55.98), Gemini 4 Argon (2026-09-30, II 52.56), GPT-6.1 Sol (2026-09-29, II 51.83),
   GPT-6 Luna (2026-09-22, II 38.12), Grok 4.7 (2026-09-21, II 46.45), MiMo-V2.6-Pro (2026-09-21,
   II 46.32), Step 5 Preview (2026-09-18, II 43.73).
2. **models.dev registry** — `models.dev/api.json`, fetched 2026-10-02: **225 providers, 8,359
   models** (2026-09-20: 222 / 7,869). Provider ids `bee`, `pareto` and `tempr` are new.
   Snapshot: `modelsdev-api.json`.
3. **FX** — `open.er-api.com/v6/latest/USD` fetched 2026-10-02: **1 USD = 6.714553 CNY**
   (2026-09-20: 6.718405). Snapshot: `fx-cny-usd.txt`.

## First-party — subscriptions

4. **Z.ai GLM Coding Plan overview** — `docs.z.ai/devpack/overview.md`, fetched 2026-10-02. Credit
   tables (Lite 2,000/10,000; Pro 12,000/60,000; Max 28,000/140,000), the credit formula with
   per-model multipliers (GLM-5.3: input 6.9 / cached 1.7 / output 24; GLM-5.3-Flash: 2.3 / 0.56 /
   8), the estimated token allowance table by cache-hit rate (95/96/98%), and the off-peak rule
   (**50% of the standard credit rate; peak is Mon–Fri 14:00–18:00 SGT**). Snapshot:
   `zai-glm-coding-plan-overview.md`.
5. **Z.ai GLM-5.3-Flash campaign** — `docs.z.ai/devpack/notice/event-glm-5.3-flash.md`, fetched
   2026-10-02. **Campaign extended from 2026-09-20 to 2026-10-07**; 23:00–09:00 daily; ZCode and
   AutoClaw consume **zero** quota, other agents get **double**. Snapshot:
   `zai-glm53-flash-campaign.md`.
6. **Z.ai Team Plan** — `docs.z.ai/devpack/teamplan.md`, fetched 2026-10-02. Standard seat
   15,000/66,000 credits, Premium seat 35,000/155,000; on-demand overage at **10% off the model API
   list price**; data not used for training by default; Premium adds priority at peak. **Seat price
   is not published** — recorded as UNKNOWN. Snapshot: `zai-teamplan.md`.
7. **Z.ai legacy migration notice** — `docs.z.ai/devpack/transition.md`, fetched 2026-10-02.
   Publication date 2026-04-21: legacy (no-weekly-window) plans migrated from 2026-04-30, two
   complimentary months, then **50% off the latest discounted price** for three months (Lite
   $18→$9, Pro $72→$36, Max $160→$80 monthly). Snapshot: `zai-plan-update-announcement.md`.
8. **MiniMax Token Plan pricing** — `platform.minimax.io/docs/guides/pricing-token-plan.md`,
   fetched 2026-10-02. Plus $22 / Max $55 / Ultra $132, 5-hour rolling plus weekly windows, 3–4 /
   4–5 / 6–7 concurrent agents, shared quota across text/image/speech, H3 and voice-clone excluded,
   **Credits 1,000 = $1** at PAYG list. Snapshot: `minimax-token-plan-pricing.md`.
9. **MiniMax Token Plan overview** — `platform.minimax.io/docs/token-plan/intro.md`, fetched
   2026-10-02: quota is a **console usage bar**, subscription key is separate from the PAYG key,
   overflow options are Credits, upgrade, PAYG or waiting. Snapshot: `minimax-token-plan-intro.md`.
10. **Meta Muse Code subscriptions** — `dev.meta.ai/docs/muse-code/subscriptions.md`, fetched
    2026-10-02. First-party confirmation of the three tiers: **Everyday Usage**, **High Usage (5×)**,
    **Power Usage (20×)**; Everyday sends **10–50 prompts every 5 hours**; subscription works only
    through the Muse Code CLI on a Meta Model API account. **No prices on this page** — plan prices
    are THIRD-PARTY corroborated. Snapshot: `meta-muse-subscriptions.md`.
11. **OpenCode Go** — `opencode.ai/docs/go/`, fetched 2026-10-02. Two plans (**Go $10, Go Plus
    $40**), a **per-model monthly dollar ceiling grid** (GLM-5.3-Flash $60/$180, GLM-5.3 $15/$120,
    Kimi K3 $15/$60, MiMo-V2.6-Flash $60/$120, Muse Spark Contributor $60/$120, Qwen3.8 Max
    $15/$60, DeepSeek V4.1 Flash $60/$120, Grok 4.7 $15/$60, GPT-6 Luna $15/$60, …), window rules
    (**5h = 20%, weekly = 50%, monthly = 100%** of each model's ceiling), per-model token prices,
    validated clients (Claude Code, Codex, ZCode, Pi, jcode, Kilo Code CLI) and a "known problematic
    clients" list. Snapshot: `opencode-go.html`.
12. **Kimi API pricing** — `platform.kimi.ai/docs/pricing/chat.md`, fetched 2026-10-02: kimi-k3 at
    $3.00 input / $0.30 cached / $15.00 output per M tokens with 1,048,576-token context; K2-series
    table follows. Snapshot: `kimi-api-pricing.md`.
13. **Kimi membership docs** — `kimi.com/code/docs/en/kimi-code/membership.html` and
    `kimi.com/en/help/membership/membership-overview`, fetched 2026-10-02. Snapshot:
    `kimi-membership-doc.html`, `kimi-help-membership-overview.html`.
14. **Command Code pricing** — `commandcode.ai/pricing`, fetched 2026-10-02. Go $1 (+processing
    fee) with **$10 credits / "up to ~$15 usage with deals"** (was ~$20 on 2026-09-20); GOAT $10 /
    $70 credits / ~$100 with deals; Pro $20 / $80; Max 10× $100 / $150; Max 20× $200 / $300;
    Teams **$40** (was absent); API plan $15. Per-model allowances now name GPT-5.6 Sol $70, GLM-5.2
    $70, Tencent Hy3 $70, Qwen3.8 27B $70, DeepSeek V4.1 Flash $60. Snapshot:
    `commandcode-pricing.html`.
15. **GitHub Copilot plans** — `docs.github.com/en/copilot/get-started/plans`, fetched 2026-10-02:
    Free (AI-credit allowance, Auto only), Pro $10 (1,000 base + 500 flex), Pro+ $39 (3,900 + 3,100),
    **Max $100 (10,000 + 10,000)**, Business $19 (1,900), Enterprise $39 (3,900). Snapshot:
    `github-copilot-plans.html`.
16. **Cursor pricing** — `cursor.com/pricing`, fetched 2026-10-02. Public page still shows only
    **Individual $20 and Teams $40**; Ultra and the quota figures remain behind JS.
    Snapshot: `cursor-pricing.html`.
17. **Kiro pricing** — `kiro.dev/pricing/`, fetched 2026-10-02: Free $0 / 50 credits, Pro $20 /
    1,000, Pro+ $40 / 2,000, Pro Max $100 / 5,000, Power $200 / 10,000; add-on credits.
    Snapshot: `kiro-pricing.html`.
18. **Devin pricing** — `devin.ai/pricing`, fetched 2026-10-02: Free / Pro $20 / Max $200, Teams
    $80 base + $40 per full dev seat. Snapshot: `devin-pricing.html`.
19. **Trae pricing** — `trae.ai/pricing`, fetched 2026-10-02: Free $0 (Auto only, limited),
    Pro $20 ($20 usage, 10 concurrent cloud tasks), Pro+ $60 ($60 usage, 15 tasks), Ultra $200
    ($200 usage, 20 tasks); Free tier now lists **5,000 completions/month**.
    Snapshot: `trae-pricing.html`.
20. **Factory pricing** — `factory.ai/pricing`, fetched 2026-10-02: Droid Pro $20 / Plus $100 /
    Max $200; teams $60/mo plus $40/mo per seat. Snapshot: `factory-pricing.html`.
21. **Amp pricing** — `ampcode.com/pricing`, fetched 2026-10-02: Individual $20/mo with 45,000
    orb-minutes; free tier is BYO-subscription or BYOK. Snapshot: `amp-pricing.html`.
22. **JetBrains AI** — `jetbrains.com/ai/`, fetched 2026-10-02: AI Credits (1 credit = $1), Free
    3 credits/30 days, Pro $10 = 10 credits, Ultimate $30 = 35 credits. Snapshot: `jetbrains-ai.html`.
23. **xAI news** — `x.ai/news`, fetched 2026-10-02. Snapshot: `xai-news.html`.
24. **Alibaba Model Studio Coding Plan** — `alibabacloud.com/help/en/model-studio/coding-plan`,
    fetched 2026-10-02: 6,000 requests / 5h, 45,000 / week, 90,000 / month; Lite retired.
    Snapshot: `alibaba-coding-plan-doc.html`.
25. **Qwen Code README** — `github.com/QwenLM/qwen-code`, fetched 2026-10-02: free tier via a Qwen
    account; the README now adds a Privacy section covering the Chrome extension and Browser Use
    data handling. Snapshot: `qwen-code-readme.md`.
26. **Remaining first-party pages**, all fetched 2026-10-02 and byte-compared against their
    2026-09-20 snapshots (all but one changed): Kilo, Replit, Augment, Cerebras, Mistral, Qoder,
    CodeBuddy, Zed, Warp, OpenCode Zen, Anthropic pricing and model docs, Claude context-window
    support article, Google AI subscriptions, Gemini API pricing, Antigravity plans and models,
    Kimi API and membership pages. Files: `kilo-pricing.html`, `replit-pricing.html`,
    `augment-pricing.html`, `cerebras-code-pricing.html`, `mistral-lechat-pricing.html`,
    `qoder-pricing.html`, `codebuddy.html`, `zed-pricing.html`, `warp-pricing.html`,
    `opencode-zen.html`, `anthropic-pricing-page.html`, `anthropic-model-overview-docs.md`,
    `anthropic-context-window-paid-plans.html`, `google-ai-subscriptions.html`,
    `gemini-api-pricing.html`, `antigravity-plans-doc.html`, `antigravity-models-doc.html`.
27. **OpenAI Codex pricing** — `developers.openai.com/codex/pricing.md` returned **HTTP 403** to
    this network on 2026-10-02. The Codex allowance figures in this pass are therefore THIRD-PARTY
    (the meter study) or carried forward from 2026-09-20 with that label. The failure is recorded
    rather than papered over.

## Third-party — issue #1 sources (all fetched 2026-10-02)

28. **agentdeals `free-llm-api-index`** — `robhunter/agentdeals`, 31 AI/LLM API records each with
    a `Record verified` date, the vendor page read, the terms quoted and a rating
    (`stable`/`caution`/`risky`/`ended`/`unrated` + reason). Snapshot:
    `thirdparty-free-llm-api-index.md`. Used as the model for
    `data/free-tier-index.csv`'s dated-verification columns, and as the source of the current
    Cerebras, Cohere, Cloudflare, Mistral, NVIDIA, xAI and GitHub-Models-retired readings.
29. **`f-tiger/verified-ai-free-tiers`** — `limits.json` (131 verified entries of 221 listed tools,
    each with a quota, a "what happens at the wall" note, an official source and a check date) and
    `limits.md`. Snapshots: `thirdparty-baipiaoji-limits.json`, `thirdparty-baipiaoji-limits.md`.
    Source of the dated Kiro Free, Codex-free, Gemini CLI, Antigravity/Copilot Free, Cursor Hobby,
    Trae Free, Qoder, Cline, Aider, Bolt.new, Lovable, Replit Starter and CodeBuddy entries.
    Its own discipline — publish a figure only when a vendor page states it, with the date, and
    print why when it does not — is the reason those rows carry dates here.
30. **`peter123023/awesome-free-llm-api`** — `README.en.md`, snapshot
    `thirdparty-awesome-free-llm-api.md`. Channel-first free-API catalogue with per-entry
    re-verification notes. Source of the Vercel AI Gateway ($5/month free tier, payment method
    required, buying credits voids it), OpenRouter free-lineup count (17 `:free`, down from 21),
    OpenCode Zen (11 `-free` of 84 models), OrcaRouter, Onomeo, Token Harbor, BazaarLink, Empero,
    AIHubMix, AMD Token Factory, Experiential Labs and the B.AI free-tier shutdown (2026-09-16).
31. **`nejib1/Free-LLM`** — `README.md`, snapshot `thirdparty-free-llm.md`: 120+ free models across
    41 providers, credit-card transparency per provider, and per-tool configuration guides for
    Claude Code, Cursor and Codex CLI. Used as a cross-check on card-required status.
32. **`FeiZhuLulu/real-api-pricing`** — `data/adopted.csv` (318 plan × model rows with a `real_usd_per_mtok`,
    a confidence of high/medium/low, a source and an explicit `decision_note`), plus its `README.md`
    and `SOURCES.md`. Snapshots: `thirdparty-real-api-pricing-adopted.csv`, the README and its
    licence notice (MIT for the project's own work; the upstream `awesome-coding-plan` dataset it
    builds on is CC BY 4.0, credited to its author by name as its licence requires). Source of the
    Page 12 third-party rows: Claude Pro/Max, ChatGPT Plus/Pro, MiniMax Token Plan, GLM legacy
    prices, Cursor, Devin, Factory, Ollama Cloud and the GLM/Step/MiMo Chinese-market tiers.
33. **`phuryn/experiments` — subscription-multipliers** — snapshot
    `thirdparty-subscription-multipliers.md`. The metered multipliers in
    `data/subscription-multipliers.csv` are this work: a plan's own weekly meter
    (`rate_limit_event.seven_day.utilization`, `rate_limits.primary.used_percent`,
    `creditUsagePercent`, MSP `usage/read.weekly.usedPercent`) ticked on purpose, every model call
    in the run priced at the vendor's public API list price, floor/ceiling brackets per step and a
    whole-run bracket for the uncertainty. Measured 2026-10-01: SuperGrok 190× ± 21, Claude Max
    20× 45.3× ± 1.0, ChatGPT $100 10.25× ± 0.03, Muse Code High 9.3× ± 0.4 standard and 114× ± 12
    contributor against standard API prices. Its caveats are carried into this pass verbatim: one
    run per plan, a few points each, workload-dependent, and usage off the measured machine is
    invisible.

## Prior passes in this repository

34. [2026-09-13 pass](../2026-09-13/README.md) — the 45-model landscape and the original 44-plan
    census.
35. [2026-09-20 pass](../2026-09-20/README.md) — first-party re-verification, the relay-market
    advisory, and the models.dev cost tables.
36. [2026-09-20 relay addendum](../2026-09-20/RELAY-MARKET-ADDENDUM.md) — the fork's relay/reseller
    pass, kept as the origin of the enumeration method and of `agents-universe.csv`.
