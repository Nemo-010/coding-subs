#!/usr/bin/env python3
"""Run the real agent loop over every task and measure the true cost of each.

The number that matters is NOT the size of the final conversation. It is the SUM
of the full context sent on every turn, because an agent resends the transcript
each time. That sum is what a metered plan actually bills, and nothing in this
repo has ever measured it.
"""
import json, os, shutil, subprocess, sys, tempfile, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PYTHONPATH", "/tmp/pylibs")
os.environ.setdefault("TIKTOKEN_CACHE_DIR", "/tmp/tikcache")
import agent
from tasks import TASKS

TASK_PROMPT = ("Run the test suite, find why it fails, fix the source so the test "
               "passes, confirm with the test suite, then declare done.")

def materialise(tid, t, base):
    d = os.path.join(base, tid)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d + "/src"); os.makedirs(d + "/tests")
    for p, c in t["files"].items():
        open(os.path.join(d, p), "w").write(c)
    open(os.path.join(d, "tests/run_tests.py"), "w").write(t["test"])
    return d

def final_state(d):
    p = subprocess.run([sys.executable, "tests/run_tests.py"], cwd=d,
                       capture_output=True, text=True)
    return p.returncode == 0, (p.stdout + p.stderr).strip()[:120]

def main():
    base = tempfile.mkdtemp(prefix="bench-")
    results = []
    for tid, t in TASKS.items():
        d = materialise(tid, t, base)
        agent.ROOT = d
        t0 = time.time()
        turns = agent.run(TASK_PROMPT, max_turns=16, verbose=True)
        wall = round(time.time() - t0, 1)
        ok, msg = final_state(d)
        tin = sum(x.get("in_tokens", 0) for x in turns)
        tout = sum(x.get("out_tokens", 0) for x in turns)
        unparsable = sum(1 for x in turns if x.get("action") in (None, "UNPARSEABLE"))
        vendor_cached = [x.get("vendor_cached") for x in turns if x.get("vendor_cached")]
        rec = {"task": tid, "diff": t["diff"], "turns": len(turns), "solved": ok,
               "in_tokens": tin, "out_tokens": tout, "unparsable": unparsable,
               "wall_s": wall, "final_ctx": turns[-1].get("in_tokens", 0) if turns else 0,
               "vendor_cached_last": vendor_cached[-1] if vendor_cached else None,
               "final_msg": msg}
        results.append(rec)
        print(f"  -> {tid}: solved={ok} turns={len(turns)} in={tin:,} out={tout:,} "
              f"wall={wall}s unparsable={unparsable}")
    json.dump(results, open("bench.json", "w"), indent=2)
    solved = [r for r in results if r["solved"]]
    print(f"\n{len(solved)}/{len(results)} solved")
    if solved:
        tot = sum(r["in_tokens"] + r["out_tokens"] for r in solved)
        print(f"mean tokens per solved task: {tot/len(solved):,.0f}")
        print(f"mean input per solved task:  {sum(r['in_tokens'] for r in solved)/len(solved):,.0f}")
    return 0

if __name__ == "__main__":
    sys.exit(main())
