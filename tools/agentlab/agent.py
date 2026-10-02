#!/usr/bin/env python3
"""Drive a real coding-agent loop and measure what it consumes, turn by turn.

The loop is real: the agent reads files, edits, and runs the test suite, and sees
the failures. Nothing is faked and no result is invented. Token counts come from a
real tokenizer (tiktoken cl100k_base, vocab hash-verified), not from a rule of thumb.

Two cache numbers are recorded per turn:
  vendor_cached   what the endpoint itself reported as cached (only it knows)
  prefix_reuse    the fraction of this request that is a byte-identical prefix of the
                  previous request, i.e. the ceiling a prefix cache could reach
"""
import json, os, subprocess, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from client import chat

import tiktoken
ENC = tiktoken.get_encoding("cl100k_base")

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "workload")

def tok(s):
    return len(ENC.encode(s))

def count_messages(msgs):
    """Tokens in a chat request, including the per-message framing overhead."""
    n = 0
    for m in msgs:
        n += 4 + tok(m["role"]) + tok(m["content"])
    return n + 2

def prefix_reuse(prev, cur):
    """Longest common byte prefix of the serialized requests, as frac of cur."""
    if not prev:
        return 0.0
    a = json.dumps(prev, sort_keys=True).encode()
    b = json.dumps(cur, sort_keys=True).encode()
    i = 0
    for x, y in zip(a, b):
        if x != y:
            break
        i += 1
    return round(i / max(len(b), 1), 4)

_NOLIST = os.environ.get("AGENTLAB_NO_LIST") == "1"

_TOOLS = ['  {"tool":"read","path":"src/inventory.py"}',
          '  {"tool":"edit","path":"src/inventory.py","old":"<exact text>","new":"<replacement>"}',
          '  {"tool":"test"}',
          '  {"tool":"done"}']
if not _NOLIST:
    _TOOLS.insert(0, '  {"tool":"list"}')
_RULE = ("call \"list\" first to see the files, then read a file before editing it."
         if not _NOLIST else "read a file before editing it.")

SYSTEM = ("You are a coding agent. You fix bugs in a Python codebase.\n\n"
          "Reply with exactly ONE JSON object per turn, nothing else:\n"
          + "\n".join(_TOOLS) + "\n\n"
          "Rules: " + _RULE + " Use \"test\" to run the suite. Use \"done\" when "
          "all tests pass. Emit no prose, only the JSON object.")

def run_tests():
    p = subprocess.run([sys.executable, "tests/run_tests.py"], cwd=ROOT,
                       capture_output=True, text=True, timeout=60)
    return (p.stdout + p.stderr).strip()

def do_edit(path, old, new):
    fp = safe_path(path)
    if fp is None:
        return f"refused: path outside the workspace: {path}"
    if not os.path.isfile(fp):
        return f"no such file: {path}"
    src = open(fp).read()
    if old not in src:
        return f"FAILED: old text not found in {path}"
    if src.count(old) > 1:
        return f"FAILED: old text is not unique in {path} ({src.count(old)} matches)"
    open(fp, "w").write(src.replace(old, new, 1))
    return f"edited {path}"

def safe_path(path):
    """Resolve inside ROOT only. Anything escaping is refused, not clamped."""
    if os.path.isabs(path):
        return None
    full = os.path.realpath(os.path.join(ROOT, path))
    root = os.path.realpath(ROOT)
    if full != root and not full.startswith(root + os.sep):
        return None
    return full

def do_read(path):
    fp = safe_path(path)
    if fp is None:
        return f"refused: path outside the workspace: {path}"
    if not os.path.isfile(fp):
        return f"no such file: {path}"
    return open(fp).read()

def do_list(path="."):
    fp = safe_path(path)
    if fp is None or not os.path.isdir(fp):
        return f"no such directory: {path}"
    out = []
    for dirpath, dirnames, filenames in os.walk(fp):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        rel = os.path.relpath(dirpath, ROOT)
        for f in sorted(filenames):
            out.append(os.path.join(rel, f) if rel != "." else f)
    return "\n".join(sorted(out)) or "(empty)"

def extract_json(text):
    """Pull the first balanced {...} object out of a completion."""
    depth = 0; start = None
    in_str = False; esc = False
    for i, ch in enumerate(text):
        if in_str:
            if esc: esc = False
            elif ch == "\\": esc = True
            elif ch == '"': in_str = False
            continue
        if ch == '"': in_str = True
        elif ch == "{":
            if depth == 0: start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                try:
                    return json.loads(text[start:i+1])
                except ValueError:
                    start = None
    return None

def run(task, max_turns=14, verbose=True, root=None):
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": task}]
    turns = []
    prev_req = None
    for t in range(1, max_turns + 1):
        in_tok = count_messages(msgs)
        reuse = prefix_reuse(prev_req, msgs)
        prev_req = json.loads(json.dumps(msgs))
        r = chat(msgs, max_tokens=900)
        if not r["ok"]:
            turns.append({"turn": t, "error": r["error"], "ms": r["ms"]})
            break
        out_tok = tok(r["content"])
        u = r["usage"] or {}
        rec = {"turn": t, "in_tokens": in_tok, "out_tokens": out_tok,
               "vendor_prompt": u.get("prompt_tokens"),
               "vendor_cached": (u.get("prompt_tokens_details") or {}).get("cached_tokens"),
               "prefix_reuse": reuse, "ms": r["ms"]}
        action = extract_json(r["content"])
        if action is None:
            rec["action"] = "UNPARSEABLE"
            rec["raw"] = r["content"][:160]
            msgs.append({"role": "assistant", "content": r["content"]})
            msgs.append({"role": "user", "content": "That was not JSON. Reply with one JSON object."})
            turns.append(rec)
            continue
        tool = action.get("tool")
        rec["action"] = tool
        if tool == "done":
            result = "agent declared done"
        elif tool == "list":
            result = do_list(action.get("path", "."))
        elif tool == "read":
            result = do_read(action.get("path", ""))
        elif tool == "edit":
            result = do_edit(action.get("path", ""), action.get("old", ""), action.get("new", ""))
        elif tool == "test":
            result = run_tests()
        else:
            result = f"unknown tool: {tool}"
        rec["result_head"] = result[:100].replace("\n", " ")
        msgs.append({"role": "assistant", "content": r["content"]})
        msgs.append({"role": "user", "content": f"RESULT:\n{result}"})
        turns.append(rec)
        if verbose:
            print(f"  t{t:>2} in={in_tok:>6} out={out_tok:>4} reuse={reuse:.2f} "
                  f"vendor_cached={rec['vendor_cached']} {tool:<6} {rec['result_head'][:52]}")
        if tool == "done":
            break
        if tool == "test" and "7/7 passed" in result:
            break
    return turns

if __name__ == "__main__":
    TASK = ("Run the test suite, find why any failing tests fail, fix the source so "
            "all tests pass, and confirm with the test suite. Then declare done.")
    print("TASK:", TASK[:70], "...")
    turns = run(TASK)
    json.dump(turns, open("run1.json", "w"), indent=2)
    print(f"\nturns={len(turns)} total_in={sum(t.get('in_tokens',0) for t in turns)} "
          f"total_out={sum(t.get('out_tokens',0) for t in turns)}")
