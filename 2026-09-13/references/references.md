# References — Coding-Subs Research Pass 2026-09-13

All sources accessed and verified on **2026-09-13 (UTC)** unless noted. Raw snapshots for most
primary sources live in [`../sources/`](../sources/). The model-landscape numbers come from an
Artificial Analysis page snapshot taken 2026-09-13 (see `../data/aa-snapshot-2026-09-13.json`).

## Model landscape (primary)

1. **Artificial Analysis — Models database** (snapshot of `artificialanalysis.ai/models` +
   embedded per-model dataset incl. `claude-opus-5` page payload), captured 2026-09-13.
   Source of: Intelligence Index (II), Terminal-Bench v4.0, context windows, API prices,
   modality flags, release dates. Snapshot: `../data/aa-snapshot-2026-09-13.json`.
   Note: page is JS-rendered; data was extracted from the embedded Next.js flight payload.

## Model documentation (primary)

2. **Anthropic — Model overview docs** (`docs.claude.com/en/docs/about-claude/models/overview.md`):
   Opus 5 / Fable 5.1 / Sonnet 5 / Haiku 4.5 specs, 1M context, pricing ($5/$25 Opus 5;
   $10/$50 Fable 5.1), batch 50% off, cache-read 10% (2.5% Fable 5.1/Mythos 5.1),
   300K output beta header. Snapshot: `../sources/anthropic-model-overview-docs.md`.
3. **Anthropic — "How large is the context window on paid Claude plans?"** (support.claude.com,
   article 8606394): Claude Code on paid plans exposes **1M context** for Opus 5 / Fable 5.1 /
   Sonnet 5 / Opus 4.8/4.7/4.6; **Pro users must enable usage credits** for 1M Opus;
   chat app contexts: Opus 5 class = 1M, 4.6/4.7/4.8 = 500K, others 200K; Cowork specifics.
   Snapshot: `../sources/anthropic-context-window-paid-plans.txt`.
4. **OpenAI — Codex pricing docs** (`developers.openai.com/codex/pricing.md`): Free/Go $8/Plus
   $20/Pro from $100 (5x) & $200 (20x); GPT-5.6 family (Sol/Terra/Luna) on Plus;
   GPT-5.3-Codex-Spark research preview on Pro; per-model local-messages-per-5h table
   (Plus: Sol 10–100, Terra 25–200, Luna 250–2,000, GPT-6 Astra 5–45); weekly limits;
   ChatGPT credits. Snapshot: `../sources/openai-codex-pricing.md`.
5. **Google — Gemini Developer API pricing** (`ai.google.dev/gemini-api/docs/pricing`):
   Gemini 3.8 Flash intro price **$0.75/$3.75 through Dec 31 2026**, then $1.50/$7.50;
   free tier; context caching; Batch 50%. Snapshot: `../sources/gemini-api-pricing-38flash.txt`.
6. **Kimi (Moonshot) — Kimi Code docs** (`kimi.com/code/docs/en/`): K3 = 2.8T params, 1M-token
   context, native vision; K2.7 Code 256K w/ image+video input; CLI + VS Code + Claude Code /
   OpenCode / Codex / Hermes integrations; quota shared with Kimi membership; 5h rolling +
   weekly refresh; Extra Usage top-ups near API rates. Snapshot: `../sources/kimi-code-membership-benefits-doc.txt`.
7. **Kimi API pricing** (`platform.kimi.ai/docs/pricing/chat.md` + ki-ai.chat cross-check of
   2026-08-04): K3 $3/$15 (cached input $0.30), 1M ctx; K2.7 Code $0.95/$4, 256K.
8. **Meta — Muse Code** official blog & docs (`developer.meta.com/ai/resources/blog/muse-code-new-plans-and-features/`,
   `dev.meta.ai/docs/muse-code/` + `/auth` + `/subscriptions`): out of beta Aug 31 2026; three
   subscription tiers (Everyday 10–50 prompts/5h; High 3x; Power 10x); multimodal uploads;
   workflows/subagents/SDK; pay-as-you-go per token alternative. Snapshots: `../sources/meta-muse-code-*.md`.

## Subscription & plan pricing (primary)

9. **Z.ai — GLM Coding Plan docs** (`docs.z.ai/devpack/overview.md` + FAQ + usage-policy +
   teamplan + transition + campaign pages, fetched as .md): supported models GLM-5.3 +
   GLM-5.3-Flash; Lite/Pro/Max 5-hour credits 2,000/12,000/28,000 and weekly 10,000/60,000/140,000;
   **official estimated token allowance tables** (e.g. Pro @95% cache: GLM-5.3 290–580M tokens/week);
   credit multipliers (GLM-5.3: in 6.9 / cached 1.7 / out 24 per 10k); off-peak 50% rate;
   vision/search/reader MCP included; works in Claude Code, Cline, OpenCode, Roo, Kilo, Codex,
   Goose, ZCode. Snapshots: `../sources/zai-*.md`.
10. **Z.ai — Plan Update Announcement / Legacy Migration** (docs.z.ai): current standard prices
    **Lite $18 / Pro $72 / Max $160 per month**; 50% migration discount ($9/$36/$80) for
    legacy users; quarterly/annual variants. Snapshot: `../sources/zai-legacy-plan-migration-prices.md`.
11. **Z.ai — GLM-5.3-Flash Usage Campaign** (docs.z.ai): Sep 3–20, 2026; unlimited GLM-5.3-Flash
    via ZCode 23:00–09:00 CST; doubled quota in other agents. Snapshot: `../sources/zai-glm53-flash-campaign.md`.
12. **MiniMax — Token Plan docs** (`platform.minimax.io/docs/token-plan/intro.md` +
    `guides/pricing-token-plan.md` + FAQ): Plus **$22** / Max **$55** / Ultra **$132** per month;
    5-hour rolling + weekly windows; 3–4/4–5/6–7 parallel agents; full model lineup
    (M3/M2.7/image/speech); credits $1 per 1,000; successor to Coding Plan. Snapshots: `../sources/minimax-*.md`.
13. **GitHub Copilot — plans & billing docs** (docs.github.com): Copilot Free/Student/Pro $10
    (1,000 credits)/Pro+ $39 (3,900)/Max $100 (10,000)/Business $19/Enterprise $39; **1 AI credit
    = $0.01** of token usage; base + flex allotment; model rate tables incl. GPT-6 Astra,
    GPT-5.6 family, Claude Opus 5/Fable 5.1, Gemini 3.8 Flash, Grok 4.6, Kimi K3 at API-mirror
    prices; code completions unbilled/unlimited. Snapshots: `../sources/github-copilot-*.txt`.
14. **Google Antigravity — docs** (`antigravity.google/docs/plans/`, `/docs/models/`): free tier
    model set incl. Gemini 3.8/3.7/3.6 Flash, Gemini 3.1 Pro, **Claude Sonnet 4.6 & Opus 4.6
    (thinking), gpt-oss-120b on free/AI Plus**; compute-based 5h + weekly quotas; AI-credit
    overage setting; Ultra = highest quotas + third-party models. Snapshots: `../sources/antigravity-*.txt`.
15. **Google AI plans — 9to5Google coverage of official I/O 2026 announcements** (May 19 / May 25 /
    Jun 8, 2026): AI Ultra new **$100 tier (5x Pro)**; former $249.99 tier cut to **$200 (20x)**;
    AI Plus dropped to **$4.99** (Jun 8); compute-based Gemini limits (5h refresh until weekly);
    Antigravity limits tripled twice after backlash (May 21). Snapshots: `../sources/9to5google-*.txt`.
16. **Anthropic — consumer pricing page + Claude Code help center** (`anthropic.com/pricing`,
    support articles 11145838 / 11647753 / 14552983 / 12429409): Pro $20 ($17 annual), Max from
    $100 (5x/20x); usage-credit purchase after limits; **weekly limits raised 25% permanently
    from Sep 14, 2026** (per Anthropic announcements quoted in HN thread, Aug 29 2026).
17. **Alibaba Cloud Model Studio — Coding Plan docs** (`alibabacloud.com/help/en/model-studio/...`,
    updated Sep 11, 2026): Pro **$50/mo**; 6,000 req/5h, 45,000/wk, 90,000/mo; models qwen3.7-plus
    (vision), qwen3.6-plus, kimi-k2.5 (vision), glm-5, MiniMax-M2.5 + more; Lite closed to new
    subs Mar 20, 2026; Anthropic- & OpenAI-compatible endpoints; slots restocked daily.
    Snapshot: `../sources/alibaba-cloud-coding-plan-doc.txt`.
18. **Cerebras Code** (`cerebras.ai/code`): Free / Pro $50 (24M tok/day) / Max $200 (120M tok/day),
    GLM 4.7 — **all paid tiers marked "sold out"** as of 2026-09-13.
    Snapshot: `../sources/cerebras-code-pricing-soldout.txt`.
19. **Trae pricing** (`trae.ai/pricing`): Free / Lite $3 ($5 usage) / Pro $10 ($20 usage) /
    Pro+ $30 (3.5x) / Ultra $100 (20x); SOLO mode included. Snapshot: `../sources/trae-pricing.txt`.
20. **Kiro pricing** (`kiro.dev/pricing`): Free 50 credits (Sonnet 4.5 + open-weight);
    Pro $20 = 1,000 credits; Pro+ $40; Pro Max $100; Power $200; add-ons $0.04/credit;
    paid tiers incl. Claude Sonnet 5 + Opus 5. Snapshot: `../sources/kiro-pricing.txt`.
21. **Replit pricing** (`replit.com/pricing`): Core $20/$18 (annual) incl. $20 model credit;
    Pro $100/$90 incl. $100 credit, 10 parallel agents. Snapshot: `../sources/replit-pricing.txt`.
22. **Kilo Code pricing** (`kilocode.ai/pricing`; acquired by Anaconda): free open-source platform;
    Kilo Gateway at exact provider rates; **Kilo Pass** $19→$26.60 / $49→$68.60 / $199→$278.60
    credits (up to 50% welcome, 40% steady bonus). Snapshot: `../sources/kilo-pricing-kilo-pass.txt`.
23. **Augment pricing** (`augmentcode.com/pricing`): Standard $20 flat (up to 50 seats, $20 usage);
    Business $100 (50 seats, $100 usage). Snapshot: `../sources/augment-pricing.txt`.
24. **Cline / Roo / OpenCode** (cline.bot/pricing, roocode.com, opencode.ai + /zen): free BYOK
    tools; OpenCode Zen = zero-markup PAYG gateway ($20 top-ups).
25. **Mistral Le Chat / Vibe** (`mistral.ai/pricing`): Le Chat paid tiers w/ $15–30/mo API
    credits; Vibe = coding agent across web/CLI/IDE (Devstral-powered).
26. **Chutes** (`chutes.ai/pricing`): pay-per-token, "no subscription, no markup", TEE compute.
27. **Abacus.AI ChatLLM Teams** (`abacus.ai/chatllm`): $10/mo ($7 first month), 100+ models incl.
    GPT-6 Astra, Fable 5.1, Opus 5, Gemini 3.8 Flash, Kimi K3, GLM 5.3, Grok 4.6; agent + code
    editor; quotas unpublished.

## Market context (secondary/press)

28. **KDnuggets — "5 AI Coding Subscription Plans That Give Developers the Best Value"**
    (Jun 29, 2026): independently ranks MiniMax Token Plan, Xiaomi **MiMo Token Plan** (1M ctx
    agentic coding, cheap), GLM Coding Plan (price hikes noted), Codex (ChatGPT-bundled),
    Kimi Code. Cross-check of this report's findings. Snapshot: `../sources/kdnuggets-5-best-value-coding-plans.md`.
29. **Pandaily — "Alibaba Cloud Launches 'Ultimate Coding Plan'"** (Feb 25, 2026): Lite $1 first
    month (18,000 req/mo), Pro $5.5 first month (90,000 req/mo); multi-lab model switching.
    Snapshot: `../sources/pandaily-alibaba-ultimate-coding-plan.md`.
30. **VentureBeat** (Jun 1, 2026): MiniMax M3 "eclipsing GPT-5.5 and Gemini 3.1 Pro on key
    benchmark performance for just 5–10% of the cost" — note AA II (29.6) is more conservative
    than the press framing; both recorded.
31. **CNBC / WSJ / Reuters / Engadget** (Jul–Sep 2026): Meta Muse Code & Muse Spark 1.1→1.3
    launch coverage; Muse Code = Meta's terminal coding agent (Spark 1.2 Aug 5; GA + plans
    Aug 31; Spark 1.3 Sep 2).
32. **Incrypted / Gizmodo / 36Kr / shattered.io** (Sep 5–10, 2026): Meta Muse AI agent launch
    with **100M free tokens/week** promo; Muse subscriptions $20–$100/mo. Third-party; promo
    terms unverified against first-party docs.
33. **Decrypt** (Feb 25, 2026) + follow-ups (Aug 3, 2026): Alibaba shut down the Qwen Code free
    tier (the 2,000 req/day OAuth flow), pushing users to the paid Coding Plan.
34. **Cognition blog** (Aug 5, 2026): "Introducing Devin Desktop" — Windsurf brand folding into
    Devin Desktop; legacy Windsurf plans in migration.
35. **South China Morning Post** (Apr 15, 2026): Z.ai/DeepSeek subscriptions sold via Tmall
    (first-party regional storefront, China).
36. **HN community threads** (via Algolia, 2026): heavy-user datapoints — Codex Pro 20x
    ≈ "$2,200/week API-equivalent on GPT-5.6 Sol" (Jul 18); Codex seen as "almost unlimited"
    vs Claude (Jul 8); Cursor users reporting unsupervised $200 overage (Aug 18);
    GLM/Kimi plans "more value if you need that many tokens" (Aug 13–14);
    Kimi K3 early tool-calling issues (Jul 16–22); Anthropic weekly-limit +25% announcement
    (Aug 29–31).

## Known gaps

- Kimi membership tier gating for K3 is from a third-party guide (checked Aug 4, 2026);
  first-party tier table is JS-rendered — verify at checkout.
- Muse Code subscription dollar prices are shown at onboarding only; press reports $20–$100.
- Windsurf/Devin Desktop 2026 pricing could not be verified (bot-protection block).
- Antigravity does not publish numeric quotas; only 5h/weekly compute-based windows.
- Codex/Cursor effective agent context windows are not documented; the models support 1M,
  but the harness may cap effective context (Codex historically compacts; UNKNOWN).
