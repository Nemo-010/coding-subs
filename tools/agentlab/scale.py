#!/usr/bin/env python3
"""How does an agent turn cost scale with the size of the code it must read?

The fixtures above are ~60 lines. Real repos are not, and file contents dominate
context. This keeps the BUG identical and varies only the amount of code around it,
so the marginal cost of context is isolated.
"""
import json, os, subprocess, sys, tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PYTHONPATH", "/tmp/pylibs")
os.environ.setdefault("TIKTOKEN_CACHE_DIR", "/tmp/tikcache")
import agent, tiktoken
ENC = tiktoken.get_encoding("cl100k_base")

FILLER = '''def helper_{i}(x):
    """Deterministic helper number {i}."""
    total = 0
    for k in range(x):
        total += k * {i}
    return total

'''

def make_tree(target_lines, base):
    d = os.path.join(base, "scale")
    os.makedirs(d + "/src", exist_ok=True); os.makedirs(d + "/tests", exist_ok=True)
    body, i = [], 0
    while len(body) * 5 < target_lines:
        body.append(FILLER.format(i=i)); i += 1
    # the single real bug, at the very bottom of a large file
    body.append('''def inclusive_total(items):
    """Sum of items, including both endpoints of the range."""
    return sum(items) - items[-1]
''')
    src = "".join(body)
    open(d + "/src/big.py", "w").write(src)
    open(d + "/tests/run_tests.py", "w").write('''import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from big import inclusive_total
def test():
    assert inclusive_total([1,2,3]) == 6, inclusive_total([1,2,3])
if __name__ == "__main__":
    try:
        test(); print("1/1 passed")
    except AssertionError as e:
        print("FAIL inclusive_total:", e); sys.exit(1)
''')
    return d, src

def main():
    base = tempfile.mkdtemp(prefix="scale-")
    out = []
    for target in (50, 500, 2000, 8000):
        d, src = make_tree(target, base)
        agent.ROOT = d
        lines = src.count("\n") + 1
        file_tokens = len(ENC.encode(src))
        prompt = ("Run the test suite, find why it fails, fix src/big.py so the test "
                  "passes, confirm with the test suite, then declare done.")
        turns = agent.run(prompt, max_turns=14, verbose=False)
        tin = sum(x.get("in_tokens", 0) for x in turns)
        tout = sum(x.get("out_tokens", 0) for x in turns)
        p = subprocess.run([sys.executable, "tests/run_tests.py"], cwd=d,
                           capture_output=True, text=True)
        cached = [x.get("vendor_cached") or 0 for x in turns]
        reuse = [x.get("prefix_reuse", 0) for x in turns]
        rec = {"target_lines": target, "file_lines": lines, "file_tokens": file_tokens,
               "turns": len(turns), "in_tokens": tin, "out_tokens": tout,
               "solved": p.returncode == 0, "read_calls": sum(1 for x in turns if x.get("action") == "read"),
               "vendor_cached_total": sum(cached),
               "cache_frac_mean": round(sum(reuse)/len(reuse), 3) if reuse else 0,
               "cache_frac_last": reuse[-1] if reuse else 0}
        out.append(rec)
        print(f"  file={lines:>5} lines ({file_tokens:>7,} tok) turns={len(turns):>2} "
              f"in={tin:>8,} solved={p.returncode==0} reads={rec['read_calls']} "
              f"cache_frac={rec['cache_frac_mean']:.2f} vendor_cached={rec['vendor_cached_total']:,}")
    json.dump(out, open("scale.json", "w"), indent=2)
    print()
    print(f"{'file tok':>9} {'session in':>11} {'ratio':>7}")
    for r in out:
        print(f"{r['file_tokens']:>9,} {r['in_tokens']:>11,} {r['in_tokens']/max(r['file_tokens'],1):>7.2f}x")
    return 0

if __name__ == "__main__":
    sys.exit(main())
