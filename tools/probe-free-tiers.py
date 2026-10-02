#!/usr/bin/env python3
"""Probe the free-tier / anonymous-access universe: which endpoints answer, and how.

Question this answers: of the "free tier" endpoints a coding agent could be pointed
at today, which ones actually answer a real request from this sandbox, without an
account, without a card, and how long do they take? A vendor saying "free" is a
claim; a 200 with a completion is an observation.

Rounds: each endpoint is probed REQ_ROUNDS times with a tiny chat completion (and a
/models list where the API exposes one) so a one-off 503 is not read as "down" and a
one-off 200 is not read as "up".

Honesty rules in this file:
  * A 401/403 is recorded as AUTH_REQUIRED, not as down: the endpoint exists and
    only lacks a key. That distinction is the whole point of the "anon" column.
  * No key, token, cookie or credential of any kind is read from the environment,
    a file or a prompt. If an endpoint needs one, the probe records that it needs
    one and stops. This tool cannot and will not test an authenticated path.
  * A response body is never stored. Only status, timing and token counts.

Usage: python3 tools/probe-free-tiers.py [PASS_DIR] [ROUNDS]
Exit: 0 ran, 2 could not run.
Writes PASS_DIR/data/free-tier-probe.json
"""
import concurrent.futures as cf
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
ROOT = Path(__file__).resolve().parent.parent

# label -> (base_url, wire_format, model_to_try)
# wire_format: openai (/chat/completions) | ollama (/api/chat) | google (native)
ENDPOINTS = {
    # --- global free tiers ---
    "NVIDIA NIM":            ("https://integrate.api.nvidia.com/v1", "openai", "deepseek-ai/deepseek-v4.1-flash"),
    "Groq":                  ("https://api.groq.com/openai/v1", "openai", "qwen/qwen3.8-27b"),
    "Google AI Studio":      ("https://generativelanguage.googleapis.com/v1beta", "google", "gemini-3.8-flash"),
    "Cloudflare Workers AI": ("https://api.cloudflare.com/client/v4/accounts/anonymous/ai/v1", "openai", "@cf/meta/llama-3.3-70b-instruct-fp8-fast"),
    "OpenRouter":            ("https://openrouter.ai/api/v1", "openai", "inclusionai/ling-3.0-flash-sante:free"),
    "Hugging Face router":   ("https://router.huggingface.co/v1", "openai", "Qwen/Qwen3-8B"),
    # --- free-pool gateways ---
    "OrcaRouter":            ("https://api.orcarouter.ai/v1", "openai", "orcarouter/free"),
    "Onomeo":                ("https://onomeo.com/v1", "openai", "gemini-3.1-flash-lite"),
    "Empero":                ("https://free.empero.org/v1", "openai", "glm-5.3-flash"),
    "BazaarLink":            ("https://api.bazaarlink.ai/v1", "openai", "auto:free"),
    "Token Harbor":          ("https://tokenharbor.ai/v1", "openai", "deepseek-v4-flash"),
    "AIHubMix":              ("https://aihubmix.com/v1", "openai", "glm-4.7-flash-free"),
    "TokenRouter":           ("https://api.tokenrouter.com/v1", "openai", "qwen3.8-max-free"),
    "Vercel AI Gateway":     ("https://ai-gateway.vercel.sh/v1", "openai", "inclusionai/ling-3.0-flash-sante-free"),
    # --- coding-agent gateways on a free plan ---
    "OpenCode Zen":          ("https://opencode.ai/zen/v1", "openai", "space-bunny-free"),
    "AMD Token Factory":     ("https://developer.amd.com.cn/radeon/api/v1", "openai", "MiniCPM5-1B"),
    # --- vendor APIs whose free tier this repo has only ever read about ---
    "Mistral API":           ("https://api.mistral.ai/v1", "openai", "mistral-small-4"),
    "Cerebras":              ("https://api.cerebras.ai/v1", "openai", "gpt-oss-120b"),
    "Cohere":                ("https://api.cohere.com/v2", "openai", "command-a-plus"),
    "DeepInfra":             ("https://api.deepinfra.com/v1/openai", "openai", "tencent/Hy3"),
    "Fireworks AI":          ("https://api.fireworks.ai/inference/v1", "openai", "accounts/fireworks/models/gpt-oss-120b"),
    "Together AI":           ("https://api.together.xyz/v1", "openai", "openai/gpt-oss-120b"),
    "SiliconFlow INTL":      ("https://api.siliconflow.com/v1", "openai", "Qwen/Qwen3-8B"),
    "Ollama Cloud":          ("https://ollama.com/api", "ollama", "deepseek-v4.1-flash"),
    # --- zero-cost stealth models whose vendors say "callable with no key" ---
    "OpenCode Zen (no key)": ("https://opencode.ai/zen/v1", "openai", "space-bunny-free"),
}

REQ_ROUNDS = 3
TIMEOUT = 45


def post_json(url: str, body: dict, headers: dict, timeout: int = TIMEOUT):
    """One request. Returns (status, ms, parsed_or_None, error_name)."""
    data = json.dumps(body).encode()
    hdr = {"User-Agent": UA, "Content-Type": "application/json", **headers}
    req = urllib.request.Request(url, data=data, headers=hdr, method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(20000)
            ms = round((time.time() - t0) * 1000)
            try:
                return r.status, ms, json.loads(raw), None
            except Exception:  # noqa: BLE001 - body shape varies wildly
                return r.status, ms, None, "unparseable-body"
    except urllib.error.HTTPError as e:
        ms = round((time.time() - t0) * 1000)
        return e.code, ms, None, None
    except Exception as e:  # noqa: BLE001
        ms = round((time.time() - t0) * 1000)
        return None, ms, None, type(e).__name__


def get_json(url: str, headers: dict, timeout: int = TIMEOUT):
    req = urllib.request.Request(url, headers={"User-Agent": UA, **headers}, method="GET")
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read(400000)
            return r.status, round((time.time() - t0) * 1000), json.loads(raw), None
    except urllib.error.HTTPError as e:
        return e.code, round((time.time() - t0) * 1000), None, None
    except Exception as e:  # noqa: BLE001
        return None, round((time.time() - t0) * 1000), None, type(e).__name__


def classify(status, err):
    if status == 200:
        return "ANON_OK"
    if status in (401, 403):
        return "AUTH_REQUIRED"
    if status == 429:
        return "RATE_LIMITED"
    if status in (402,):
        return "PAYMENT_REQUIRED"
    if status in (404,):
        return "NO_SUCH_ROUTE_OR_MODEL"
    if status is None:
        return f"UNREACHABLE ({err})"
    return f"HTTP_{status}"


def tokens_of(label, fmt, body):
    """Best-effort token count out of a completion body; never guesses."""
    if not isinstance(body, dict):
        return None
    if fmt == "openai":
        u = body.get("usage") or {}
        if "total_tokens" in u:
            return u["total_tokens"]
    if fmt == "ollama":
        if "eval_count" in body:
            return body.get("prompt_eval_count", 0) + body.get("eval_count", 0)
    if fmt == "google":
        u = body.get("usageMetadata") or {}
        if "totalTokenCount" in u:
            return u["totalTokenCount"]
    return None


def probe_once(label, base, fmt, model):
    if fmt == "openai":
        status, ms, body, err = post_json(
            base + "/chat/completions",
            {"model": model, "messages": [{"role": "user", "content": "hi"}], "max_tokens": 1},
            {},
        )
    elif fmt == "ollama":
        status, ms, body, err = post_json(
            base + "/chat", {"model": model, "messages": [{"role": "user", "content": "hi"}], "stream": False}, {}
        )
    else:  # google native
        status, ms, body, err = post_json(
            f"{base}/models/{model}:generateContent",
            {"contents": [{"parts": [{"text": "hi"}]}]},
            {},
        )
    return {
        "status": status, "ms": ms, "err": err,
        "class": classify(status, err),
        "total_tokens": tokens_of(label, fmt, body),
    }


def main():
    pass_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else sorted(
        p for p in ROOT.iterdir() if p.is_dir() and len(p.name) == 10 and p.name[4] == "-")[-1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else REQ_ROUNDS
    print(f"probing {len(ENDPOINTS)} free-tier endpoints, {rounds} rounds, no credentials of any kind")

    # 1) /models listings: does the endpoint exist and what does it admit to?
    models = {}
    for label, (base, fmt, model) in ENDPOINTS.items():
        if fmt == "openai":
            st, ms, body, err = get_json(base + "/models", {})
        elif fmt == "ollama":
            st, ms, body, err = get_json(base + "/tags", {})
        else:
            st, ms, body, err = get_json(base + "/models", {})
        n = None
        if isinstance(body, dict):
            for k in ("data", "models", "tags"):
                if isinstance(body.get(k), list):
                    n = len(body[k])
        models[label] = {"status": st, "ms": ms, "err": err, "model_count": n,
                         "class": classify(st, err)}

    # 2) real completions, N rounds
    results = {label: [] for label in ENDPOINTS}
    for rnd in range(rounds):
        with cf.ThreadPoolExecutor(max_workers=10) as ex:
            futs = {ex.submit(probe_once, label, base, fmt, model): label
                    for label, (base, fmt, model) in ENDPOINTS.items()}
            for f in cf.as_completed(futs):
                results[futs[f]].append(f.result())
        print(f"  round {rnd+1}/{rounds} done")

    summary = {}
    for label, runs in results.items():
        ok = sum(1 for r in runs if r["class"] == "ANON_OK")
        classes = {}
        for r in runs:
            classes[r["class"]] = classes.get(r["class"], 0) + 1
        oks = sorted(r["ms"] for r in runs if r["class"] == "ANON_OK")
        summary[label] = {
            "models_probe": models[label],
            "anon_ok_rounds": ok,
            "rounds": rounds,
            "classes": classes,
            "median_ms_ok": oks[len(oks) // 2] if oks else None,
            "tokens_seen": sorted({r["total_tokens"] for r in runs if r["total_tokens"] is not None}),
            "runs": runs,
        }
        verdict = "ANON_OK" if ok == rounds else (max(classes, key=classes.get) if classes else "?")
        print(f"  {label:26} {verdict:24} ok={ok}/{rounds} median={summary[label]['median_ms_ok']}ms")

    out = pass_dir / "data" / "free-tier-probe.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({
        "date": pass_dir.name,
        "method": "unauthenticated POST /chat/completions (or /api/chat, or :generateContent) with max_tokens=1; no credentials read from anywhere",
        "endpoints": len(ENDPOINTS),
        "rounds": rounds,
        "summary": summary,
    }, indent=2))
    anon = sum(1 for s in summary.values() if s["anon_ok_rounds"] == rounds)
    print(f"\n{anon}/{len(ENDPOINTS)} answered every round with no credential; wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
