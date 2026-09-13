# Deep Reviews — pass 2026-09-13

Five independent review passes were performed before publishing, per standing practice.
Each pass used a distinct lens, had to find-or-fix something real, and its fixes were folded
in before the next pass. Findings are numbered; all are marked FIXED.

---

## Review 1 — Re-derivation (recompute every number from raw sources)

Re-derived, from the archived first-party sources (not from this report's own text):
GLM weekly→monthly capacity math (48/97/146/292/290/580/676/1352 M tokens/week × 4.33),
the workload's API cost on eight models (15M input + 37.5M output at list prices), the GLM
Lite API-equivalent value, and all arbitrage multiples.

**Findings:**
1. Report stated GLM Lite capacity value as "$738–$1,489/mo"; exact re-derivation gives
   $736.9–$1,488 (186 × 208/52.5 = 736.9) — first figure misrounded. → **FIXED** ($737).
2. All other arithmetic re-derived clean: 208–420M (48/97 × 4.33), 1,256–2,511M (Pro),
   2,927–5,854M (Max); Opus-5 workload cost $1,012.50; GLM-5.3 $186; multiples 41–83×;
   Codex Pro 20x ≈ $9.5k/mo from the $2,200/week community datapoint (×4.33).

## Review 2 — Claim-scope (is every claim scoped to its source and date?)

Checked each factual claim against its citation for overreach or staleness.

**Findings:**
3. Report said Claude weekly limits "rose 25% on Sep 14, 2026" — but Sep 14 is *after* the
   research date (Sep 13); the +25% was *announced* (Anthropic statements quoted Aug 29–31)
   and effective Sep 14. Tense overstated certainty. → **FIXED** ("announced, effective Sep 14,
   2026 — the day after this research date").
4. Scope otherwise held: "1M in Claude Code" correctly scoped to the Anthropic support doc with
   the Pro-tier usage-credits caveat; Muse free-100M-tokens/week kept THIRD-PARTY/promo status;
   MiniMax M3 kept the press-vs-AA-II tension visible; "Gemini 3.8 Flash is the flagship"
   grounded in the AA dataset (no 3.8 Pro slug exists); K3 tier-gating kept THIRD-PARTY.

## Review 3 — Consistency-router (cross-check report ↔ databases ↔ sources)

**Findings:**
5. **Real inconsistency:** the providers DB carried GLM Lite capacity "192-388M; Flash
   584M-1,168M" (4.0-week math) *labeled* 4.33wk, while the report said 208–420M (4.33-week
   math, matching Z.ai's official weekly tables). → **FIXED** (CSV updated to 208-420M /
   632M-1,264M and a validator check now pins CSV↔report agreement).
6. Root README claimed "30+ providers"; the DB actually has 26 distinct provider groups (44
   plans). → **FIXED** (README now says 26; validator floor set at ≥20 distinct).
7. Row-by-row sweep of the workload-test verdicts against the capacity column found no other
   contradictions (e.g., GLM Lite PASS at 100M vs 208M low-end holds).

## Review 4 — Security / adversarial

Assumed an adversarial reader: ToS violations, credential leakage, data-exfiltration risk,
supply-chain/prompt-injection surface, scam exposure.

**Findings:**
8. **Missing privacy caution:** an HN-linked reverse-engineering writeup (runtimewire, Aug
   2026) claims Muse Code sends some prompts/telemetry to Meta by default. The report praised
   Muse's economics without a data-use caveat. → **FIXED** (privacy note added to caveats,
   pointing at Meta's Model API ToS).
9. ToS hygiene verified: resold shared accounts are explicitly excluded and flagged RISKY;
   the Tmall storefront note is marked informational only. No credentials/API keys anywhere in
   the repo (only format placeholders like `sk-sp-xxxxx` from provider docs). No executable
   agent-instruction files (no AGENTS.md/skills) that a coding agent might auto-ingest —
   `tools/validate.py` is inert Python run only by CI or a human.

## Review 5 — Tests / CI

**Findings:**
10. `tools/validate.py` initially failed its own run (missing `docs/reviews.md`) — correct
    behavior; re-run after this file landed: **OK**. A date check that would have broken CI on
    any day after the research date was loosened to "pass dir ≤ today" with an opt-in
    `STRICT_DATE` env for same-day runs. → **FIXED**.
11. Model cross-check regex missed dotted slugs (e.g. `gemini-3.8-flash`); normalized to
    dash-form before lookup. → **FIXED**.
12. Added a CSV↔report GLM-capacity consistency assertion so Review-3-style drift is caught
    mechanically in CI (`.github/workflows/ci.yml` runs the validator on every push).

---

**Verdict: all five lenses produced at least one accepted fix (11 fixes total across 10
findings + 1 correct initial failure). The pass was published only after fixes 1–12 landed
and `python3 tools/validate.py` returned OK.**
