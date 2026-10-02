# agentlab — measuring what a coding-agent session actually costs

Everything else in this repo compares *prices*. This measures *value*: what a real
agent loop consumes, so a published quota can be converted into actual work.

## Why

Plans in this market are sold in requests, credits, prompts, orb-minutes, ACUs and
"usage value". None of those is a token, and the repo has been listing them side by
side as if that were a comparison. To compare them you need one thing nobody had
measured: **how many tokens a real agent task consumes, and how that scales.**

## What it does

`agent.py` drives a real loop against the one endpoint that answers with no
credential (`space-bunny-free`, measured 2026-10-02). The agent gets tools
(`list`, `read`, `edit`, `test`), edits real files, runs a real test suite, sees the
failures and iterates. Token counts come from **tiktoken `cl100k_base`** (vocab
sha256-verified), not a rule of thumb.

`tasks.py` defines 8 real bug-fix tasks; all 8 fail before the fix and pass after it.

Run:
```
export PYTHONPATH=/path/to/tiktoken            # see below
python3 bench.py      # 8 tasks, with the list tool
AGENTLAB_NO_LIST=1 python3 bench.py            # the same 8, without it
python3 scale.py      # the same bug in files of 428 / 4k / 16k / 66k tokens
python3 final.py      # converts published plan quotas into measured units
```

## Safety

`safe_path()` confines every file tool to the workspace. Absolute paths, `..`
traversal and anything outside the root are **refused, not clamped**. An earlier
revision resolved absolute paths and read `/proc/self/environ`; that is fixed and
must stay fixed.

No credential, key or cookie is read from anywhere, ever — the endpoint needs none.

## Environment

tiktoken needs its BPE vocab. Download
`https://openaipublic.blob.core.windows.net/encodings/cl100k_base.tiktoken`
(sha256 `223921b76ee99bde995b7ff738513eef100fb51d18c93597a113bcffe865b2a7`), then place
it in a cache dir at the sha1 of that URL and point `TIKTOKEN_CACHE_DIR` at it:

```
mkdir -p /tmp/tikcache
curl -sL "$URL" -o /tmp/tikcache/$(printf '%s' "$URL" | sha1sum | cut -d' ' -f1)
export TIKTOKEN_CACHE_DIR=/tmp/tikcache
```

## Caveats that must travel with the numbers

- The model is a **stealth model on a free anonymous endpoint**. Its own
  `cached_tokens` reporting is not trustworthy (2026-10-02 measured it billing 89,063
  tokens for a prompt it had evidently not read in full). Raw token counts here are
  **my own tokenizer's**, which is model-independent; the cache fraction is the
  endpoint's claim and is labelled as such.
- The 8 tasks are **single-file, one-bug fixes**. Multi-file work, features and
  refactors cost more. Every figure is a **lower bound**.
- `cl100k_base` is not the tokenizer of the plans being compared. It is a consistent
  proxy; absolute counts would shift by maybe ±15% on a different tokenizer, ratios
  would not.
