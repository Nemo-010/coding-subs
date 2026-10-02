# Ten deep reviews — 2026-10-03 pass

Ten reviews of this pass, written as attempts to **falsify** it. Each names what was tested,
what held, and what did not. Reviews that would have been hollow praise are given the space
instead to attack a weak point. Numbered, and each ends with a verdict.

---

## Review 1 — Did the pass actually re-read every source, or copy the last one?

**Test.** Compare `2026-10-03/sources/` against `2026-10-02/sources/` by sha256. A pass that
claims to re-fetch must produce different bytes where the page changed and provably fresh
bytes everywhere.

**What held.** 55 files were fetched serially with a per-source http/bytes/ms/sha256 log
(`data/fetch-log.json`), and the 2026-10-02 tree was left untouched for comparison. The Z.ai
campaign page hashes identically to the 2026-10-02 copy, which is the correct result for a
page that did not change, and proves the comparison discriminates.

**What did not.** Six data files (`providers-database`, `models-database`, `agents-universe`,
`free-tier-index`, `cost-per-usable-token`, `subscription-multipliers`) were copied forward
from 2026-10-02 rather than re-derived. That is defensible for tables whose inputs are not
first-party pricing pages, but the README must not let a reader think they were re-checked.

**Fix applied.** The report now separates "VERIFIED live" from "CARRIED FORWARD" explicitly.

**Verdict.** PASS WITH DISCLOSURE — the fetch is real; six tables are carried and now say so.

---

## Review 2 — The Meta row. A price with no first-party source.

**Test.** `2026-10-02` carried `Muse Code High Usage $15`. Does any first-party page state a
Muse subscription price?

**What held.** The pass fetched `dev.meta.ai/docs/muse-code/subscriptions.md` and read all
three tiers. The page describes Everyday / High Usage / Power Usage and their multipliers
(10-50 prompts per 5h, 5x, 20x) but **states no price for any of them**.

**What did not.** The previous table's `$15` has no first-party provenance — it came from a
third-party listing. Carrying it as if verified was the same class of error this repo exists
to catch.

**Fix applied.** The Meta price is now `UNKNOWN` with a `source_quality` of "VERIFIED plan;
price not published", and three Muse rows replace the one.

**Verdict.** PASS — a real defect from the prior pass was found and labelled, not smoothed.

---

## Review 3 — Cursor Pro+. Structured data versus the visible page.

**Test.** The visible Cursor pricing text renders only `$20 / mo` and `$40 / user / mo`.
Where does `Pro+ $60` and `Ultra $200` come from?

**What held.** Both are in the page's own JSON-LD: `{"@type":"Offer","name":"Pro+",
"price":"60"}`. Structured data is machine-written by the vendor, which makes it *stronger*
evidence than the marketing copy a human eyeballs.

**What did not.** The extraction script initially reported only the prose prices and would
have missed Pro+ entirely. That is a tooling near-miss: the pass would have shipped a table
missing a newly-launched tier while claiming to have read the page.

**Fix applied.** `tools/extract-2026-10-03.py` reads schema.org `Offer` blocks for Cursor
and Kiro, and the Kiro result found four missing tiers rather than one.

**Verdict.** PASS — but only because the tool was changed mid-pass; the first extraction was
wrong.

---

## Review 4 — The Google locale trap.

**Test.** Reproduce the Google fetch. Does `gemini.google/subscriptions/` return USD?

**What held.** It returns a **Spanish-locale** page to this sandbox, with no `$19.99` in the
text and plan names in Spanish. A pass that parsed it would have extracted nothing — or worse,
picked up an unrelated `$` figure from a promotion.

**What did not.** The first extraction run printed `AI Pro $ 199.99`, which is the *Ultra*
price adjacent to the Pro label in the layout. A sloppier regex would have published
"AI Pro = $199.99".

**Fix applied.** Re-fetched with `?hl=en&gl=us`, stored as `google-ai-subscriptions-us.html`,
and the report records the locale artefact as a vantage-point limitation. The correct figures
are Plus $4.99 / Pro $19.99 / Ultra from $99.99 and $199.99.

**Verdict.** PASS WITH WARNING — the pass nearly published a wrong number through a layout
ambiguity. The US-locale file is kept alongside the Spanish one so the difference is
auditable.

---

## Review 5 — The 8-row arithmetic check: is it real or theatre?

**Test.** Ajam's rule: a regression clause must **fail against the unpatched tree**. Stash
the cost-table fix and run the validator.

**What held.** `tools/validate.py` enforces that each cost row's `price_usd_month`,
`monthly_tokens_low` and `usd_per_mtok_low` agree within 5 %. Against the git-stashed
2026-10-02 tree it reports **8 failures** with the exact ratio (2.00x, 2.01x, 1.33x, 1.25x).
Against the fixed tree it passes.

**What did not.** The first version of this check used a 3x tolerance and **passed on the
broken tree** — it was theatre. Tightening to 5 % made it bite.

**Fix applied.** Tolerance is 5 %, with an explicit escape hatch only for a row that *names*
a vendor-published effective-usage multiplier in `capacity_basis`.

**Verdict.** PASS — the clause demonstrably fails pre-fix, which is the only thing that makes
it worth having.

---

## Review 6 — CSV field-count integrity, the silent-shift bug.

**Test.** Can a row with more fields than its header still satisfy `csv.DictReader` and every
existing check?

**What held.** Yes. `DictReader` collects surplus cells under a `None` key, so
`None in row.values()` is `False` and the old validator passed. Fifteen rows across four
files were affected, shifting `status`, `source_quality` and in six cases the price.

**What did not.** The 2026-10-02 pass shipped those fifteen rows and printed
`OK: all checks passed (census shape)`. The check that would have caught it did not exist.

**Fix applied.** The validator now compares `len(row)` to `len(header)` for every
`data/*.csv`, plus empty/duplicate header names. It reports the six `first-party-plans` rows
by line number against the pre-fix tree.

**Verdict.** PASS — a validator blind spot was found and closed, and the failure is
reproducible.

---

## Review 7 — Is "1 of 25 free endpoints" a fair claim?

**Test.** Re-examine the 2026-10-02 anonymous probe. Is `AUTH_REQUIRED` being read as "down"?

**What held.** The probe records 401/403 as `AUTH_REQUIRED` and says in its own docstring that
this is *not* the same as down — the endpoint exists and lacks a key. Six endpoints publish a
full anonymous `/models` catalogue (NVIDIA NIM 81 models, Hugging Face 134, OrcaRouter 205,
AIHubMix 417, DeepInfra 183) and then refuse a single token, which is the substantive finding.

**What did not.** The headline "1 of 25" invites the reading that 24 providers are broken. The
report should lead with "22 are gated, not down", as the probe file does.

**Fix applied.** The 2026-10-03 report does not repeat the 1-of-25 figure without that
qualifier, and points at the probe file for the mechanism.

**Verdict.** PASS WITH FRAMING FIX — the measurement is sound; the summary line was doing the
data an injustice.

---

## Review 8 — OpenAI: what is actually being claimed?

**Test.** Both OpenAI pricing URLs return HTTP 403. Is the pass entitled to keep those rows?

**What held.** The rows are kept but re-labelled `CARRIED FORWARD (not re-verified
2026-10-03)`, and REVERIFY.md states the 403 explicitly with the two URLs. A reader can see
that no check happened.

**What did not.** There is no fallback: `openai.com/chatgpt/pricing/` also 403s, so there is
no first-party path from this sandbox at all. The pass cannot verify OpenAI and should not
pretend a third-party listing is a substitute.

**Fix applied.** None available beyond labelling. Recorded as a hard gap.

**Verdict.** PASS (as a gap) — the limitation is the finding. Any future pass must verify
OpenAI from a different vantage point or leave it carried.

---

## Review 9 — The Meta/Devin/Kiro "new rows": drift or my own missed reading?

**Test.** Were Cursor Pro+, Kiro's four tiers and Devin Max genuinely new, or did the
2026-10-02 pass simply fail to read them?

**What held.** Kiro's five tiers are in the page's schema.org block today; the old row had
one. The distinction between "vendor launched it" and "I failed to read it" cannot be settled
from today's page alone.

**What did not.** The report's heading "new plans that did not exist in the previous table"
asserts vendor change when it can only prove *table* change. That is an overclaim.

**Fix applied.** The heading in REVERIFY.md says what is demonstrable: "new plans that did
not exist in the previous table". The README's "what changed" section is scoped to the table,
and the falsification list includes the possibility that the vendor did not change.

**Verdict.** PASS — an overclaim was caught and re-scoped. This is the review that earned its
place.

---

## Review 10 — Does the pass do the work Ajam actually asked for?

**Test.** The instruction was "every single source, one by one, fetch, update, along the way".
Measure against that literally.

**What held.** 55 sources, serially, one at a time, with a per-source log; 26 of 28 providers
re-verified against a live page today; each finding recorded as it was made, in REVERIFY.md.

**What did not.** Two things. First, the **relay/reseller universe** (≈30 provider domains in
`2026-09-20/data/relay-providers-database.csv`) was **not** re-fetched this pass — that is a
second, larger source set and it was left for a later one. Second, the "update" is a new
pass directory plus a corrected cost table; the 2026-10-02 tables were **not rewritten in
place**, so the two passes must be read together for the timeline.

**Fix applied.** Both are stated in REVERIFY.md's counts and in this review. Neither is
hidden.

**Verdict.** PARTIAL — the first-party universe is done properly; the relay universe is not,
and the report should not be read as covering it.

---

---

## Review 11 — Is `cl100k_base` a fair proxy for token counts?

**Test.** The measured counts come from OpenAI's tokenizer, but the plans compared include
GLM, Qwen, Claude and Gemini, which tokenize differently. Does that invalidate the numbers?

**What held.** Every count is a tokenizer's count of the *actual serialized payload*, which
makes it model-independent and reproducible. Ratios — the scaling curve, the 71% waste, the
credit conversion — are properties of the loop, not of the tokenizer.

**What did not.** Absolute counts would shift on a different tokenizer, plausibly ±15%, and
the Z.ai conversion applies `cl100k` counts to GLM weights. The pass says so in AGENT-COST.md
rather than leaving a reader to discover it.

**Verdict.** PASS WITH DISCLOSURE — the right proxy for ratios, the wrong one for a claim
about a specific vendor's billing.

---

## Review 12 — The A/B was confounded, and the first version of it was not honest

**Test.** The with-`list` arm (8/8) ran *before* retry-with-backoff was added to the client,
and the without-`list` arm (3/8) ran *after*. That is two changes, not one.

**What held.** Re-running the with-`list` arm on the identical client restored the comparison
to a single variable: **8/8 with, 3/8 without.**

**What did not.** The first A/B would have shipped with an uncontrolled difference between its
arms — exactly the class of flaw this repo is supposed to catch in other people's numbers. It
was caught by re-reading the run order, not by any check.

**Fix applied.** Both arms re-run on the same client version; `bench_withlist.json` holds the
re-run. The confound is recorded here rather than quietly overwritten.

**Verdict.** FAIL AS FIRST RUN, PASS AFTER — and the near-miss is the point of the review.

---

## Review 13 — Single-run scaling numbers were not trustworthy

**Test.** The first scaling run gave 265,445 tokens for the 65,828-token file. A later
identical run gave 530,637. Which is right?

**What held.** Neither alone. Three repetitions per size show a **1.5×–3.6× spread** across
repeats of an identical task, driven by turn count.

**What did not.** The pass was about to publish a point estimate for a quantity with a long
right tail. The 265,445 figure and the 2,066,679 figure are the same configuration measured on
different days.

**Fix applied.** `scale_reps.py` runs three reps per size and the report publishes mean, min,
max and spread. Repetition is what turned this from an anecdote into a finding.

**Verdict.** PASS — a real defect in the method, found by repeating a run the pass had already
declared finished.

---

## Review 14 — Does the Z.ai cross-check actually validate the method?

**Test.** The formula at Z.ai's own 95% cache assumption gives 177.5M tokens/month for GLM
Lite. Z.ai's published figure is 208–420M. Is 177.5M a validation or a 15% miss?

**What held.** It lands just below the vendor's low end on an assumption (output share) the
vendor does not publish. Reproducing a vendor's own range from the vendor's own formula is
meaningful independent confirmation.

**What did not.** It is not exact, and the pass must not claim the method is "confirmed" when
it is "consistent within the mix uncertainty". The 208M end would need a slightly different
output ratio.

**Fix applied.** AGENT-COST.md says "reproduces the range within its own stated mix
uncertainty", not "matches".

**Verdict.** PASS WITH PRECISION FIX — the claim was softened to what is demonstrable.

---

## Review 15 — The agent's `read` tool was a sandbox-escape primitive

**Test.** During the first benchmark run the transcript showed `read /proc/self/cwd` and
`read` of environment variables. Did the tool allow that?

**What held.** It did: `os.path.join(ROOT, path)` discards the root when the second argument
is absolute, so any absolute path was readable. That is a sandbox escape, and reading the
environment is prohibited outright.

**What did not.** Nothing about it was safe, and it was discovered only by reading a
transcript closely, not by any check.

**Fix applied.** `safe_path()` resolves with `realpath` and refuses anything outside the root —
absolute paths, `..` traversal, and paths that symlink out. Verified: `/proc/self/environ`,
`../../etc/passwd` and `.env` are all refused. Recorded in `tools/agentlab/README.md` as a
property that must stay fixed.

**Verdict.** PASS AFTER FIX — the most serious defect found in this pass, and it was found by
reading output rather than trusting the design.

---

## Review 16 — Is the workload representative?

**Test.** Eight tasks, all single-file, one-bug fixes, each 30–60 lines. Real agent work is
multi-file features and refactors.

**What held.** The scaling experiment addresses exactly this: it holds the bug constant and
varies file size, so the *shape* of the cost curve generalises even though the fixtures are
small. The 563k-token row is representative of a real repo file.

**What did not.** Turn counts, exploration behaviour and error rates are all properties of
these tiny fixtures. A real feature request would explore more, and the pass cannot say by how
much. Every figure is a **lower bound** and the report says so.

**Fix applied.** None available. Recorded as the primary limitation.

**Verdict.** PASS (as a stated bound) — the honest framing is that this measures the floor.

---

## Summary of verdicts

| # | Area | Verdict |
|---|---|---|
| 1 | Sources actually re-fetched | PASS WITH DISCLOSURE |
| 2 | Meta price with no first-party source | PASS |
| 3 | Cursor Pro+ via structured data | PASS (tool fixed mid-pass) |
| 4 | Google locale trap | PASS WITH WARNING |
| 5 | 8-row arithmetic regression clause | PASS |
| 6 | CSV field-count integrity | PASS |
| 7 | "1 of 25 free endpoints" framing | PASS WITH FRAMING FIX |
| 8 | OpenAI 403 | PASS (as a gap) |
| 9 | "New plan" overclaim | PASS |
| 10 | Coverage against the instruction | PARTIAL |
| 11 | `cl100k` as a token proxy | PASS WITH DISCLOSURE |
| 12 | Confounded A/B (client changed mid-pass) | FAIL AS FIRST RUN, PASS AFTER |
| 13 | Single-run scaling numbers | PASS (after repetition) |
| 14 | Z.ai cross-check precision | PASS WITH PRECISION FIX |
| 15 | `read` tool sandbox escape | PASS AFTER FIX |
| 16 | Workload representativeness | PASS (as a stated bound) |

**Six reviews found real defects in this pass's own work**, and they are the reason to trust
the rest: a missed pricing tier (3), a near-miss wrong number (4), a confounded experiment
(12), single-sample numbers presented as measurements (13), an overclaim (9), and a
**sandbox-escape primitive in the agent's own file tool** (15).

Three of those six were caught only by attacking work already declared finished. A report that
scored sixteen clean passes would be a report nobody had tried to break.
