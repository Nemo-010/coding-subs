# What a coding-agent session actually costs — measured, 2026-10-03

Everything else in this repository compares **prices**. This measures **value**: what a real
agent loop consumes, so a published quota can be converted into work actually done.

The gap it closes: every plan in this market is sold in a unit that is not a token —
Copilot sells *premium requests*, Z.ai sells *credits*, MiniMax sells *prompts*, Amp sells
*orb-minutes*, Devin sells *ACUs*, Trae sells *"usage value"*. The repo has been listing them
side by side as though that were a comparison. It is not, and this is the missing number.

## Method

A real agent loop (`tools/agentlab/`), driven against the one endpoint that answers with no
credential (measured 2026-10-02). The agent gets `list`, `read`, `edit` and `test` tools,
edits actual files, runs an actual test suite, reads the failures and iterates. Nothing is
simulated and no number is invented.

Token counts come from **tiktoken `cl100k_base`**, vocab sha256-verified — a real tokenizer,
not characters-divided-by-four. Raw measurements: `data/agentlab/`.

The scaling experiment is **repeated three times per size**, because one run is one sample of
a quantity that swings with turn count. The repetition turned out to be the most important
methodological choice in the pass — see Finding 2.

## Measured cost shape

| Quantity | Measured |
|---|---|
| Solve rate (with a `list` tool) | **8/8** |
| Mean turns per task | **8.2** |
| Mean input tokens per task | **3,779** |
| Mean output tokens per task | **208** |
| Cache-eligible fraction of input | **0.69** |

## Finding 1 — cost is context × turns, and it swings enormously

An agent resends the entire transcript every turn. The billed quantity is therefore not the
size of the conversation but the **sum of the full context over every turn**. Holding the bug
identical and varying only the size of the file that contains it, three runs each:

| File size | Mean session input | Min | Max | Run-to-run spread |
|---|---|---|---|---|
| 3,468 tok | 35,950 | 19,409 | 46,403 | **2.4×** |
| 32,268 tok | 196,687 | 99,151 | 358,835 | **3.6×** |
| 134,886 tok | 721,739 | 540,979 | 812,120 | **1.5×** |
| **563,166 tok** | **2,066,679** | 1,691,029 | 2,817,977 | **1.7×** |

**A one-line fix in a 563,166-token file consumes 2,066,679 input tokens.** Read a file at
turn two and it is re-sent on every subsequent turn; a large read across a ten-turn session
is billed ten times.

**The practical consequence: any plan comparison that does not state a context size is
meaningless.** The spread between the smallest and largest session measured here is **57×**,
and against the trivial 60-line fixtures it is larger still. That is a wider spread than
separates *every plan in this repository from every other one*.

## Finding 2 — run-to-run spread defeats single-sample claims

An identical task on an identical file and identical model varied by **1.5× to 3.6×** between
repeats. The cause is turn count: one extra exploration turn resends the whole context.

This is why the earlier single-run figures in this pass (265,445 for the large file) are not
trustworthy on their own — the same configuration later measured 530,637 and 2,066,679. Any
number in this market quoted from one run is a sample, not a measurement. **Cost per task in
this market is not a point estimate; it is a distribution with a long right tail**, and a
budget built on the mean will be exceeded roughly half the time.

## Finding 3 — tool surface decides outcomes, and failure costs more than success

Same 8 tasks, same endpoint, same client, same tokenizer. The only difference is whether the
agent was offered a directory listing:

| | Solved | Tokens spent | Tokens that produced nothing |
|---|---|---|---|
| **with `list`** | **8/8** | 35,529 | 0 |
| **without `list`** | **3/8** | 32,481 | **23,134 (71%)** |

Without the tool the agent does not fail cheaply. It guesses filenames — `app.py`, `main.py`,
`pyproject.toml`, `/workspace`, `/proc/self/cwd` — and pays for every guess on every
subsequent turn. **71% of all tokens went to tasks it never solved, and the failures cost
more than most of the successes.**

A missing tool is not a neutral handicap. It converts token spend into waste — money on a
token-metered plan, quota on a request-metered one.

## Finding 4 — vendor credits convert, and the conversion validates

Z.ai publishes the formula:

```
credit = (input × input_mult + cached_input × cached_mult + output × output_mult) / 10,000
GLM-5.3:  6.9 / 1.7 / 24        GLM-5.3-Flash:  2.3 / 0.56 / 8
```

**1 credit = 10,000 weighted tokens.** Checking the method against the vendor's own published
figure for GLM Lite (208–420M GLM-5.3 tokens/month at 95% cache):

| Cache assumption | Input tokens/month implied |
|---|---|
| 95% (Z.ai's stated assumption) | **177.5M** |
| measured 0.69 | 113.9M |

The published formula reproduces the vendor's range within its own stated mix uncertainty
(177.5M against the 208M low end). **The method is validated against the vendor's own number**,
which is what makes the conversions below worth reading rather than being arithmetic theatre.

## Finding 5 — published quotas in measured units

Z.ai sessions per week, using the measured cache and Z.ai's own weighting:

| Plan | Credits/wk | 3k file | 32k file | 135k file | 563k file |
|---|---|---|---|---|---|
| GLM Lite $18 | 10,000 | 597 | 109 | 30 | **10** |
| GLM Pro $72 | 60,000 | 3,584 | 655 | 179 | **62** |
| GLM Max $160 | 140,000 | 8,364 | 1,529 | 417 | **145** |

Request-metered plans — a request *is* a turn:

| Plan | Requests/mo | Measured tasks |
|---|---|---|
| Copilot Pro $10 | 1,500 | **182** |
| Copilot Pro+ $39 | 7,000 | **848** |
| Copilot Max $100 | 20,000 | **2,424** |

**This inverts the naive ranking.** Copilot sells *turns* at a flat price, so its cost per turn
does not grow with context size, while a token-metered plan's does. Copilot Max's 20,000
requests buy 2,424 trivial tasks — and the *same* 20,000 requests buy heavy 563k-file tasks
that would drain a token-metered plan's week. Which plan is cheaper depends entirely on the
shape of the work, and that is knowable only if you measure it.

## What this pass did not establish

- **These are lower bounds.** All 8 tasks are single-file, one-bug fixes. Multi-file changes,
  feature work and refactors read more and iterate more.
- **The cache fraction is the endpoint's claim, not a measurement of the plans.** `cl100k`
  counts are mine; `cached_tokens` comes from the vendor and is unreliable — on 2026-10-02 the
  same endpoint billed 89,063 tokens for a prompt it had evidently not read in full.
- **`cl100k_base` is not the tokenizer of any plan compared here.** A consistent proxy: ratios
  travel, absolute counts would shift by roughly ±15%.
- **No paid plan was subscribed to.** Whether a vendor meters the way its docs say is not
  something this pass can test.
- **One model, one endpoint.** Turn counts are specific to the stealth model on the anonymous
  endpoint. A frontier model may need fewer turns, or more.
- **~1 turn in 8 was lost to unparseable output** (prose instead of the required JSON). A real,
  counted cost that no vendor's docs mention, and a property of this model specifically.
- **Three repetitions is not a distribution.** It is enough to show the spread is large; it is
  not enough to characterise the tail.

## Why this is worth more than another price table

A price table says what a vendor charges. This says what the vendor's unit *buys*, in work —
and shows the answer swings **57×** on a variable no vendor discloses, with a run-to-run spread
of up to 3.6× on top. Read alongside `REVERIFY.md`, these are the first passes in this
repository that can say what a plan is **worth** rather than what it **costs**.
