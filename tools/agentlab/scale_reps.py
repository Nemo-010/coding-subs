#!/usr/bin/env python3
"""The scaling experiment, repeated, because a single run is one sample of a variable
that swings with turn count. Reports the distribution, not a point."""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("PYTHONPATH", "/tmp/pylibs"); os.environ.setdefault("TIKTOKEN_CACHE_DIR", "/tmp/tikcache")
import agent, tiktoken
from scale import make_tree
ENC = tiktoken.get_encoding("cl100k_base")
REPS = 3

base = tempfile.mkdtemp(prefix="scalereps-")
out = []
for target in (428, 4028, 16028, 65828):
    runs = []
    for rep in range(REPS):
        d, src = make_tree(target, base)
        agent.ROOT = d
        turns = agent.run("Run the test suite, find why it fails, fix src/big.py so the test "
                          "passes, confirm with the test suite, then declare done.",
                          max_turns=14, verbose=False)
        tin = sum(x.get("in_tokens", 0) for x in turns)
        p = subprocess.run([sys.executable, "tests/run_tests.py"], cwd=d, capture_output=True, text=True)
        runs.append({"turns": len(turns), "in_tokens": tin, "solved": p.returncode == 0,
                     "cache_frac": round(sum(x.get("prefix_reuse",0) for x in turns)/len(turns),3)})
    ins = sorted(r["in_tokens"] for r in runs)
    out.append({"approx_target": target, "file_tokens": len(ENC.encode(src)), "runs": runs,
                "in_mean": sum(ins)//len(ins), "in_min": ins[0], "in_max": ins[-1],
                "solved": sum(1 for r in runs if r["solved"])})
    print(f"  file={out[-1]['file_tokens']:>7,} tok  runs={REPS}  solved={out[-1]['solved']}/{REPS}  "
          f"in_mean={out[-1]['in_mean']:>8,}  min={ins[0]:>8,}  max={ins[-1]:>8,}  spread={ins[-1]/max(ins[0],1):.1f}x")
json.dump(out, open("scale_reps.json","w"), indent=2)
print()
print("The spread between repeated runs of an IDENTICAL task is itself a finding.")
