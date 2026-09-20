#!/usr/bin/env python3
"""
mine-providers.py - structure-agnostic provider extraction for AI-gateway repos.

Motivation
----------
Two prior passes (Wei-Shaw/sub2api, router-for-me/CLIProxyAPI) each enumerated
providers by hand, and each time the list was incomplete because it relied on one
artifact (a README table, or a constants file). Repos move things. This script
extracts providers from *many independent signals* and merges them, so a future
session gets the union even if the layout changed.

Signals (each is independent; a provider found by any signal is reported)
-------------------------------------------------------------------------
  dirs      provider-like directories (auth/<x>, providers/<x>, internal/<x>)
  consts    symbolic constants  Foo = "provider-slug"  in Go/TS/JS
  cases     switch/match string labels that look like provider slugs
  json      JSON registries: litellm_provider, owned_by, provider, top-level keys
  config    YAML/TOML provider blocks and upstream entries
  markdown  README tables: provider rows and sponsor links
  vocab     a built-in vocabulary of ~200 known provider names, matched in text

Output
------
  providers-<slug>.csv   canonical provider rows (one per provider)
  providers-<slug>.jsonl evidence records (one per (provider, file, line, method))

Usage
-----
  python3 mine-providers.py --repo /path/to/repo --name sub2api --out out/
  python3 mine-providers.py --url https://github.com/x/y --name y --out out/
  python3 mine-providers.py --repo . --name x --out out/ --include-tests

No third-party dependencies. Python 3.8+.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import sys
from collections import defaultdict

# --------------------------------------------------------------------------
# 1. Known vocabulary and classification
# --------------------------------------------------------------------------

# provider id -> (display name, kind)
# kind: first-party | oauth-subscription | aggregator | media | infra
KNOWN = {
    # first-party model vendors
    "openai": ("OpenAI", "first-party"),
    "anthropic": ("Anthropic", "first-party"),
    "claude": ("Anthropic Claude", "oauth-subscription"),
    "google": ("Google", "first-party"),
    "gemini": ("Google Gemini", "oauth-subscription"),
    "gemini-cli": ("Gemini CLI", "oauth-subscription"),
    "aistudio": ("Google AI Studio", "oauth-subscription"),
    "vertex": ("Google Vertex AI", "first-party"),
    "vertex_ai": ("Google Vertex AI", "first-party"),
    "antigravity": ("Google Antigravity", "oauth-subscription"),
    "xai": ("xAI", "first-party"),
    "grok": ("xAI Grok", "first-party"),
    "kimi": ("Moonshot Kimi", "first-party"),
    "moonshot": ("Moonshot AI", "first-party"),
    "zhipu": ("Zhipu GLM", "first-party"),
    "glm": ("Zhipu GLM", "first-party"),
    "bigmodel": ("Zhipu BigModel", "first-party"),
    "zai": ("Z.AI GLM", "aggregator"),
    "deepseek": ("DeepSeek", "first-party"),
    "minimax": ("MiniMax", "first-party"),
    "qwen": ("Alibaba Qwen", "first-party"),
    "dashscope": ("Alibaba DashScope", "first-party"),
    "bailian": ("Alibaba Bailian", "first-party"),
    "alibaba": ("Alibaba Cloud", "first-party"),
    "aliyun": ("Alibaba Cloud", "first-party"),
    "volcengine": ("Volcengine", "first-party"),
    "ark": ("Volcengine Ark", "first-party"),
    "doubao": ("ByteDance Doubao", "first-party"),
    "seedance": ("ByteDance Seedance", "media"),
    "seedream": ("ByteDance Seedream", "media"),
    "tencent": ("Tencent Hunyuan", "first-party"),
    "hunyuan": ("Tencent Hunyuan", "first-party"),
    "xiaomi": ("Xiaomi MiMo", "first-party"),
    "mimo": ("Xiaomi MiMo", "first-party"),
    "stepfun": ("StepFun", "first-party"),
    "baidu": ("Baidu Qianfan", "first-party"),
    "qianfan": ("Baidu Qianfan", "first-party"),
    "ernie": ("Baidu ERNIE", "first-party"),
    "meta": ("Meta Llama", "first-party"),
    "llama": ("Meta Llama", "first-party"),
    "mistral": ("Mistral AI", "first-party"),
    "cohere": ("Cohere", "first-party"),
    "ai21": ("AI21 Labs", "first-party"),
    "arcee": ("Arcee AI", "first-party"),
    "inception": ("Inception", "first-party"),
    "sarvam": ("Sarvam AI", "first-party"),
    "upstage": ("Upstage", "first-party"),
    "nvidia": ("NVIDIA NIM", "first-party"),
    "amazon": ("Amazon", "first-party"),
    "aws": ("AWS", "first-party"),
    "bedrock": ("Amazon Bedrock", "first-party"),
    "azure": ("Microsoft Azure", "first-party"),
    "microsoft": ("Microsoft", "first-party"),
    "databricks": ("Databricks", "first-party"),
    "huggingface": ("Hugging Face", "aggregator"),
    "replicate": ("Replicate", "aggregator"),
    "voyage": ("Voyage AI", "first-party"),
    "jina": ("Jina AI", "first-party"),
    "nomic": ("Nomic AI", "first-party"),
    "openbmb": ("OpenBMB", "first-party"),
    "openweights": ("Open Weights", "first-party"),
    "aiand": ("AIand", "aggregator"),
    "longcat": ("LongCat", "first-party"),
    "bailing": ("Bailing", "first-party"),
    "sensenova": ("SenseNova", "first-party"),
    "iflytek": ("iFlytek Spark", "first-party"),
    "xfspark": ("iFlytek Spark", "first-party"),
    "spark": ("iFlytek Spark", "first-party"),
    "01ai": ("01.AI Yi", "first-party"),
    "yi": ("01.AI Yi", "first-party"),
    # coding/subscription agent products
    "codex": ("OpenAI Codex", "oauth-subscription"),
    "copilot": ("GitHub Copilot", "oauth-subscription"),
    "github-copilot": ("GitHub Copilot", "oauth-subscription"),
    "cursor": ("Cursor", "oauth-subscription"),
    "devin": ("Devin (Cognition)", "oauth-subscription"),
    "kiro": ("Amazon Kiro", "oauth-subscription"),
    "qoder": ("Alibaba Qoder", "oauth-subscription"),
    "trae": ("ByteDance Trae", "oauth-subscription"),
    "windsurf": ("Windsurf", "oauth-subscription"),
    "codebuddy": ("Tencent CodeBuddy", "oauth-subscription"),
    "workbuddy": ("Tencent WorkBuddy", "oauth-subscription"),
    "cline": ("Cline", "oauth-subscription"),
    "cindy": ("Cindy", "oauth-subscription"),
    "qwen-code": ("Qwen Code", "oauth-subscription"),
    "opencode": ("OpenCode Zen/Go", "oauth-subscription"),
    "opencode_go": ("OpenCode Zen/Go", "oauth-subscription"),
    "ollama": ("Ollama Cloud", "aggregator"),
    "agy": ("Antigravity", "oauth-subscription"),
    "amp": ("Sourcegraph Amp", "oauth-subscription"),
    "factory": ("Factory Droid", "oauth-subscription"),
    "zencoder": ("Zencoder", "oauth-subscription"),
    "augment": ("Augment Code", "oauth-subscription"),
    "charm": ("Charm Crush", "oauth-subscription"),
    "crush": ("Charm Crush", "oauth-subscription"),
    "goose": ("Block Goose", "oauth-subscription"),
    "roo": ("Roo Code", "oauth-subscription"),
    "kilo": ("Kilo Code", "oauth-subscription"),
    "droid": ("Factory Droid", "oauth-subscription"),
    "cerebras": ("Cerebras", "first-party"),
    "sambanova": ("SambaNova", "first-party"),
    "groq": ("Groq", "first-party"),
    "fireworks": ("Fireworks AI", "aggregator"),
    "deepinfra": ("DeepInfra", "aggregator"),
    "novita": ("NovitaAI", "aggregator"),
    "hyperbolic": ("Hyperbolic", "aggregator"),
    "perplexity": ("Perplexity", "aggregator"),
    "xai-grok": ("xAI Grok", "first-party"),
    "poe": ("Poe", "aggregator"),
    "lmstudio": ("LM Studio", "aggregator"),
    # aggregators / gateways
    "openrouter": ("OpenRouter", "aggregator"),
    "requesty": ("Requesty", "aggregator"),
    "vercel": ("Vercel AI Gateway", "aggregator"),
    "llmgateway": ("LLM Gateway", "aggregator"),
    "nano-gpt": ("NanoGPT", "aggregator"),
    "edenai": ("Eden AI", "aggregator"),
    "helicone": ("Helicone", "aggregator"),
    "portkey": ("Portkey", "aggregator"),
    "cloudferro-sherlock": ("CloudFerro Sherlock", "aggregator"),
    "fastrouter": ("FastRouter", "aggregator"),
    "302ai": ("302.AI", "aggregator"),
    "aihubmix": ("AIHubMix", "aggregator"),
    "merge-gateway": ("Merge Gateway", "aggregator"),
    "ofox": ("Ofox", "aggregator"),
    "zenmux": ("ZenMux", "aggregator"),
    "orcarouter": ("OrcaRouter", "aggregator"),
    "cortecs": ("Cortecs", "aggregator"),
    "kenari": ("Kenari", "aggregator"),
    "unorouter": ("UnoRouter", "aggregator"),
    "qvac": ("QVAC", "aggregator"),
    "gitlab": ("GitLab Duo", "oauth-subscription"),
    "baseten": ("Baseten", "aggregator"),
    "clarifai": ("Clarifai", "aggregator"),
    "digitalocean": ("DigitalOcean", "aggregator"),
    "crusoe": ("Crusoe", "aggregator"),
    "modelscope": ("ModelScope", "aggregator"),
    "siliconflow": ("SiliconFlow", "aggregator"),
    "z.ai": ("Z.AI", "aggregator"),
}

# infra/sponsor vocabulary (proxies, CDNs, payments) - kept separate so they are
# not mixed into the model-provider ranking
INFRA_VOCAB = {
    "bestproxy": "proxy", "rapidproxy": "proxy", "swiftproxy": "proxy",
    "colaproxy": "proxy", "duckip": "proxy", "proxy4free": "proxy",
    "roxybrowser": "browser", "axisnow": "cdn", "veilx": "cdn",
    "cyberpay": "payment", "fluxapay": "payment", "agentmarket": "payment",
    "cubence": "relay", "packyapi": "relay", "packycode": "relay",
    "aicodemirror": "relay", "aiberm": "relay", "pateway": "relay",
    "fennoai": "relay", "fenno": "relay", "apikey": "relay",
    "openmodel": "relay", "aigocode": "relay", "cctk": "relay",
    "codex-everywhere": "relay", "haoai": "relay", "lanox": "relay",
    "nagora": "relay", "pptoken": "relay", "ppdog": "relay", "etok": "relay",
    "aimzoon": "relay", "apimart": "media", "bmoplus": "accounts",
    "qiniu": "aggregator", "deepseek-relay": "relay",
}

# slug shape used to reject noise from consts/cases signals
SLUG_RE = re.compile(r"^[a-z][a-z0-9_-]{1,24}$")
STOP = {
    "true", "false", "nil", "null", "none", "auto", "text", "json", "string",
    "error", "default", "unknown", "local", "main", "test", "free", "pro",
    "plus", "team", "max", "min", "low", "high", "medium", "any", "all",
    "staging", "production", "dev", "prod", "admin", "user", "openai-response",
    "gemini-interactions", "interactions", "empty", "meta", "get", "post",
    "put", "delete", "content", "message", "model", "models", "token",
    "stream", "system", "user", "assistant", "tool", "tools", "image", "audio",
    "video", "embed", "rerank", "responses", "chat", "completions",
    # directory / language / generic words that leaked in before
    "cmd", "pkg", "internal", "ent", "migrations", "migration", "go", "rust",
    "site-name", "star-history-chart", "sub2api-logo", "sub2api", "brave",
    "tavily", "qwen3", "k3", "k2", "config-inline", "liveattestation",
    "oidc", "schema", "routes", "handler", "service", "repo", "store",
    "cache", "client", "server", "util", "misc", "logging", "runtime",
    # ordinary English / library names that are not providers here
    "inference", "infer", "litellm", "together", "cloudflare", "streaming",
}

SKIP_DIRS = {
    ".git", "node_modules", "vendor", "dist", "build", ".next", "target",
    "__pycache__", ".venv", "venv", "site-packages", ".cache", "coverage",
    "testdata", "fixtures", ".idea", ".vscode",
}

# only run the noisy vocabulary fallback inside paths that plausibly talk about
# providers, so "go"/"rust"/"cmd" in a Makefile do not become providers.
PROVIDER_PATH_RE = re.compile(
    r"(provider|auth|platform|registry|models?[/_.-]|config|readme|"
    r"upstream|gateway|billing|account|credential|sponsor|docs?[/_.-]|"
    r"constant|oauth|adapter|executor|routing|discovery)",
    re.I,
)

# tokens that are model names, not providers
MODELISH_RE = re.compile(
    r"^(gpt|claude|gemini|grok|qwen\d|qwq|k\d|glm|deepseek|minimax-m|"
    r"llama|mistral|mixtral|gemma|phi|o\d|text-|dall-e|whisper|tts)",
    re.I,
)

# plan tiers of one provider -> canonical provider
TIER_RE = re.compile(r"^(codex|claude|gemini)-(free|team|plus|pro|max|ultra)$", re.I)

# canonicalization of slugs that mean the same provider
CANON = {
    "vertex_ai": "vertex", "vertex-ai": "vertex",
    "vertex-ai-language-models": "vertex", "vertex-ai-embedding-models": "vertex",
    "text-completion-openai": "openai", "openai-codex": "codex",
    "codexeverywhere": "codex-everywhere", "lanox-ai": "lanox",
    "qiniu-ai": "qiniu", "qiniu-cloud-ai": "qiniu", "patewayai": "pateway",
    "opencode_go": "opencode", "openai-compatibility": "openai",
    "opencode-go": "opencode", "cognition": "devin",
    "fennoai": "fenno", "packycode": "packyapi",
    "xai-grok": "xai", "z.ai": "zai", "bigmodel": "zhipu",
    "ernie": "baidu", "qianfan": "baidu", "spark": "xfspark",
    "mimo": "xiaomi", "llama": "meta", "moonshot": "kimi",
    "gemini-cli": "gemini", "claude-code": "claude",
    "github-copilot": "copilot", "sensenova": "sensenova",
}

# distinctive provider names that are safe to match unquoted in provider-relevant files
STRONG_VOCAB = {
    "openrouter", "deepseek", "minimax", "zhipu", "moonshot", "kimi",
    "antigravity", "seedance", "seedream", "volcengine", "dashscope",
    "qianfan", "hunyuan", "xiaomi", "stepfun", "sensenova", "iflowcn",
    "modelscope", "siliconflow", "novita", "deepinfra", "sambanova",
    "cerebras", "fireworks", "perplexity", "helicone", "portkey",
    "requesty", "baseten", "clarifai", "digitalocean", "openrouter",
    "xai", "grok", "qwen", "glm", "ernie", "volcengine", "opencode",
    "codex", "antigravity", "augment", "devin", "kiro", "qoder", "trae",
    "windsurf", "codebuddy", "zenmux", "unorouter", "ofox", "kenari",
    "aihubmix", "302ai", "aicodemirror", "packyapi", "cubence", "aiberm",
}

TEXT_EXT = {
    ".go", ".ts", ".tsx", ".js", ".jsx", ".vue", ".py", ".rs", ".java",
    ".kt", ".cs", ".rb", ".php", ".md", ".markdown", ".json", ".jsonl",
    ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".txt", ".env",
    ".example", ".sh", ".sql",
}
MAX_BYTES = 4 * 1024 * 1024


def norm_slug(key):
    k = key.strip().lower()
    k = k.replace(" ", "-").replace("_", "-")
    return k


def classify(slug):
    s = norm_slug(slug)
    if s in KNOWN:
        return KNOWN[s]
    if s in INFRA_VOCAB:
        return (s.replace("-", " ").title(), "infra:" + INFRA_VOCAB[s])
    return (s.replace("-", " ").title(), "unknown")


def canon(slug):
    s = norm_slug(slug)
    m = TIER_RE.match(s)
    if m:
        return m.group(1).lower()
    return CANON.get(s, s)


# --------------------------------------------------------------------------
# 2. File walk
# --------------------------------------------------------------------------

def iter_text_files(root, include_tests=False, max_bytes=MAX_BYTES):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext not in TEXT_EXT:
                continue
            if not include_tests and ("_test." in fn or ".spec." in fn
                                      or ".test." in fn):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > max_bytes:
                    continue
                with open(p, "r", encoding="utf-8", errors="replace") as f:
                    yield p, f.read()
            except OSError:
                continue


# --------------------------------------------------------------------------
# 3. Signals
# --------------------------------------------------------------------------

CONST_RE = re.compile(
    r"""(?mx)
    (?P<name>\b[A-Za-z_][A-Za-z0-9_]*)
    \s*(?::=|=)\s*
    "(?P<val>[A-Za-z0-9][A-Za-z0-9_.\-/]{1,40})"
    """
)

# names whose RHS is almost always a provider slug
PROVIDERISH_NAME = re.compile(
    r"(provider|platform|vendor|upstream|backend|channel|endpoint|site)name?$",
    re.I,
)

CASE_RE = re.compile(r'(?m)^\s*(?:case|else if|elif)\s+"(?P<val>[a-z0-9_.\-]+)"')
YAML_KEY_RE = re.compile(
    r"(?m)^\s{0,6}(?P<key>[a-z][a-z0-9_\-]{1,30})\s*:\s*(?:$|[\"'\[\{])"
)
MD_LINK_RE = re.compile(r"https?://(?:www\.)?([a-z0-9][a-z0-9.\-]+\.[a-z]{2,})", re.I)
MD_ALT_RE = re.compile(r'alt="([^"]{2,40})"')
MD_TD_PROVIDER_RE = re.compile(
    r"<t[dh][^>]*>\s*(?:<a[^>]*>)?\s*(?:<img[^>]+>)?\s*([A-Za-z][A-Za-z0-9 ._\-/]{1,30})\s*"
)

JSON_KNOWN_KEYS = {"litellm_provider", "owned_by", "provider", "provider_id",
                   "vendor", "upstream", "platform"}
JSON_KEYS = re.compile(r'"(litellm_provider|owned_by|provider|provider_id|vendor|platform)"\s*:\s*"([^"]{1,40})"')


def record(evidence, provider, method, path, line, detail="", confidence="high"):
    evidence[provider].append({
        "provider": provider, "method": method, "confidence": confidence,
        "file": path, "line": line, "detail": detail,
    })


def _vocab_hit(line, line_lower, vocab):
    """Return known provider slugs present in the line.

    A bare word match is only accepted when the token is quoted ("openrouter"),
    hyphenated (codex-everywhere) or in STRONG_VOCAB. Without this gate the
    fallback fires on ordinary English ("inference", "together") and on library
    names ("litellm").
    """
    hits = []
    for v in vocab:
        if len(v) < 4:
            continue
        if not re.search(r"[^a-z0-9]" + re.escape(v) + r"[^a-z0-9]", line_lower):
            continue
        quoted = bool(re.search(r"[\"'`]" + re.escape(v) + r"[\"'`]", line, re.I))
        if quoted or "-" in v or v in STRONG_VOCAB:
            hits.append(v)
    return hits


def scan_text(text, path, evidence, vocab):
    """consts / cases / yaml / vocab / markdown; independent of layout."""
    rel = path
    lines = text.splitlines()
    vocab_ok = bool(PROVIDER_PATH_RE.search(path))
    dedot_vocab = {re.sub(r"[^a-z0-9]", "", v): v for v in vocab}
    for i, line in enumerate(lines, 1):
        for m in CONST_RE.finditer(line):
            name, val = m.group("name"), m.group("val")
            if PROVIDERISH_NAME.search(name) or norm_slug(val) in vocab:
                s = norm_slug(val)
                if SLUG_RE.match(s) and s not in STOP:
                    record(evidence, s, "consts", rel, i, f"{name}={val}")
        for m in CASE_RE.finditer(line):
            s = norm_slug(m.group("val"))
            if SLUG_RE.match(s) and s not in STOP and (
                    s in vocab or s in KNOWN or s in INFRA_VOCAB):
                record(evidence, s, "cases", rel, i, m.group("val"))
        # markdown provider tables
        if path.endswith((".md", ".markdown")):
            alt = MD_ALT_RE.search(line)
            if alt:
                s = norm_slug(alt.group(1))
                if SLUG_RE.match(s) and s not in STOP:
                    record(evidence, s, "markdown", rel, i, alt.group(1))
            if "<td" in line:
                for m in MD_TD_PROVIDER_RE.finditer(line):
                    cand = norm_slug(m.group(1))
                    if cand in KNOWN or cand in INFRA_VOCAB or cand in vocab:
                        record(evidence, cand, "markdown", rel, i, m.group(1))
            # sponsor links: derive the provider from the hostname. This is what
            # catches PP.dog / hao.ai / CCTK.AI, whose display name is a domain.
            for m in MD_LINK_RE.finditer(line):
                host = m.group(1).lower()
                if host.startswith("www."):
                    host = host[4:]
                dedot = re.sub(r"[^a-z0-9]", "", host)
                base = host.split(".")[0]
                hit = None
                if dedot in dedot_vocab:
                    hit = dedot_vocab[dedot]
                elif base in dedot_vocab:
                    hit = dedot_vocab[base]
                else:
                    for dv, original in dedot_vocab.items():
                        if len(dv) >= 5 and dedot.startswith(dv):
                            hit = original
                            break
                if hit:
                    record(evidence, hit, "markdown-host", rel, i, host,
                           confidence="medium")
        # vocabulary fallback: only in provider-relevant files, low confidence
        if vocab_ok:
            low = " " + line.lower() + " "
            for v in _vocab_hit(line, low, vocab):
                record(evidence, v, "vocab", rel, i, "", confidence="low")


def scan_json(text, path, evidence):
    """litellm_provider / owned_by / provider keys; top-level map keys."""
    if not path.endswith((".json", ".jsonl")):
        return
    try:
        data = json.loads(text)
    except Exception:
        # still catch embedded key/value pairs
        for m in JSON_KEYS.finditer(text):
            s = norm_slug(m.group(2))
            if SLUG_RE.match(s):
                record(evidence, s, "json", path, 0, m.group(1))
        return
    seen = set()

    def walk(node, depth=0):
        if depth > 6:
            return
        if isinstance(node, dict):
            for k, v in node.items():
                if k in JSON_KNOWN_KEYS and isinstance(v, str):
                    s = norm_slug(v)
                    if SLUG_RE.match(s) and s not in seen:
                        seen.add(s)
                        record(evidence, s, "json", path, 0, f"{k}={v}")
                if depth <= 2 and isinstance(v, (dict, list)):
                    walk(v, depth + 1)
        elif isinstance(node, list):
            for item in node[:4000]:
                walk(item, depth + 1)

    walk(data)
    # top-level map whose keys look like provider tiers (models.json style)
    if isinstance(data, dict):
        keys = [k for k in data.keys() if isinstance(k, str)]
        if 3 <= len(keys) <= 60 and all(
                SLUG_RE.match(norm_slug(k)) for k in keys):
            score = sum(1 for k in keys if norm_slug(k) in KNOWN)
            if score >= 2 or "models" in path.lower() or "registry" in path.lower():
                for k in keys:
                    s = norm_slug(k)
                    if s not in seen and s not in STOP:
                        seen.add(s)
                        record(evidence, s, "json-keys", path, 0, k)


def scan_dirs(root, evidence):
    """provider-like directories: auth/<x>, providers/<x>, internal/<x>."""
    interesting = ("auth", "provider", "providers", "platform", "platforms",
                   "upstream", "upstreams", "backend", "vendor")
    for dirpath, dirnames, _ in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        base = os.path.basename(dirpath).lower()
        if base in interesting:
            for d in list(dirnames):
                s = norm_slug(d)
                if s in STOP or not SLUG_RE.match(s):
                    continue
                # require a source file inside to avoid empty scaffolding
                sub = os.path.join(dirpath, d)
                has_src = False
                for _, _, fs in os.walk(sub):
                    if any(os.path.splitext(f)[1].lower() in (".go", ".py",
                                                              ".ts", ".js", ".rs")
                           for f in fs):
                        has_src = True
                        break
                if has_src:
                    record(evidence, s, "dirs", os.path.join(dirpath, d) + "/", 0, d)


def scan_yaml(text, path, evidence):
    if not path.endswith((".yaml", ".yml", ".toml")):
        return
    for i, line in enumerate(text.splitlines(), 1):
        m = YAML_KEY_RE.match(line)
        if not m:
            continue
        s = norm_slug(m.group("key"))
        if (s in KNOWN or s in INFRA_VOCAB) and s not in STOP:
            record(evidence, s, "config", path, i, m.group("key"))


# --------------------------------------------------------------------------
# 4. Main
# --------------------------------------------------------------------------

def build_vocab():
    v = set(KNOWN) | set(INFRA_VOCAB)
    for extra in ("openai-codex", "gemini-cli", "claude-code", "qwen3",
                  "seed-oss", "k2", "k3"):
        v.add(extra)
    return v


def mine(root, name, include_tests=False):
    vocab = build_vocab()
    evidence = defaultdict(list)
    scan_dirs(root, evidence)
    for path, text in iter_text_files(root, include_tests=include_tests):
        scan_text(text, path, evidence, vocab)
        scan_json(text, path, evidence)
        scan_yaml(text, path, evidence)
    return evidence


def write_outputs(evidence, outdir, name, min_confidence="low"):
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, f"providers-{name}.csv")
    jsonl_path = os.path.join(outdir, f"providers-{name}.jsonl")

    order = {"high": 3, "medium": 2, "low": 1}
    floor = order[min_confidence]

    # canonicalize
    merged = defaultdict(list)
    for slug, items in evidence.items():
        merged[canon(slug)].extend(items)

    rows = []
    for slug, items in merged.items():
        if MODELISH_RE.match(slug) and slug not in KNOWN:
            continue
        confs = {it["confidence"] for it in items}
        conf = "high" if "high" in confs else ("medium" if "medium" in confs
                                                else "low")
        if order[conf] < floor:
            continue
        display, kind = classify(slug)
        methods = sorted({it["method"] for it in items})
        rows.append({
            "repo": name,
            "provider": slug,
            "display_name": display,
            "kind": kind,
            "confidence": conf,
            "methods": "|".join(methods),
            "evidence_count": len(items),
            "first_evidence": f'{items[0]["file"]}:{items[0]["line"]}',
        })
    rows.sort(key=lambda r: (r["kind"], r["provider"]))

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["repo", "provider", "display_name",
                                          "kind", "confidence", "methods",
                                          "evidence_count", "first_evidence"])
        w.writeheader()
        w.writerows(rows)
    with open(jsonl_path, "w", encoding="utf-8") as f:
        for slug in sorted(merged):
            for it in merged[slug]:
                it = dict(it)
                it["repo"] = name
                it["provider"] = canon(it["provider"])
                f.write(json.dumps(it, ensure_ascii=False) + "\n")
    return rows


def main():
    ap = argparse.ArgumentParser(description="structure-agnostic provider miner")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--repo", help="path to a local repo")
    src.add_argument("--url", help="git URL to clone into --out/<name>")
    ap.add_argument("--name", required=True, help="repo slug for output names")
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--include-tests", action="store_true")
    ap.add_argument("--min-confidence", choices=["high", "medium", "low"],
                    default="low",
                    help="drop rows below this confidence (default low = keep all)")
    args = ap.parse_args()

    root = args.repo
    if args.url:
        root = os.path.join(args.out, args.name)
        if not os.path.isdir(root):
            subprocess.check_call(["git", "clone", "--depth", "1",
                                   args.url, root])

    if not os.path.isdir(root):
        sys.exit(f"not a directory: {root}")

    ev = mine(root, args.name, include_tests=args.include_tests)
    rows = write_outputs(ev, args.out, args.name,
                         min_confidence=args.min_confidence)
    by_kind = defaultdict(int)
    for r in rows:
        by_kind[r["kind"]] += 1
    print(f"{args.name}: {len(rows)} providers -> "
          f"{os.path.join(args.out, 'providers-' + args.name + '.csv')}")
    for k in sorted(by_kind):
        print(f"   {k:24} {by_kind[k]}")


if __name__ == "__main__":
    main()
