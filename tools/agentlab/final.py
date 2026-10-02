#!/usr/bin/env python3
"""Final conversion: published plan quotas -> measured agent work."""
import json

bench = json.load(open("bench.json"))
scale = json.load(open("scale.json"))
S = [r for r in bench if r["solved"]]
mean_turns = sum(r["turns"] for r in S)/len(S)
mean_in    = sum(r["in_tokens"] for r in S)/len(S)
mean_out   = sum(r["out_tokens"] for r in S)/len(S)
cache      = sum(r["cache_frac_mean"] for r in scale)/len(scale)

# Z.ai's published formula: (in*4.5... no -- verbatim multipliers) /10,000
ZAI = {"GLM-5.3": (6.9, 1.7, 24.0)}
def zai_credits(in_tok, out_tok, model="GLM-5.3"):
    im, cm, om = ZAI[model]
    fresh = in_tok*(1-cache); ca = in_tok*cache
    return (fresh*im + ca*cm + out_tok*om)/10000.0

REFS = [("tiny file (428 tok)", 4173, 130),
        ("small file (4k tok)", 18145, 250),
        ("medium file (16k tok)", 82273, 400),
        ("large file (66k tok)", 265445, 500)]

print("MEASURED SHAPE:", f"{len(S)}/{len(bench)} solved, {mean_turns:.1f} turns/task, "
      f"{mean_in:,.0f} in, {mean_out:,.0f} out, cache {cache:.2f}")
print()
print("Z.AI CREDITS PER REFERENCE TASK (GLM-5.3 weighting, cache measured at "
      f"{cache:.2f})")
print(f"{'reference task':24} {'raw in':>9} {'weighted':>11} {'credits':>9}")
for name, i, o in REFS:
    w = zai_credits(i, o)*10000
    print(f"{name:24} {i:>9,} {w:>11,.0f} {w/10000:>9.1f}")

print()
print("Z.AI PLANS: tasks/week at each reference size")
print(f"{'plan':16} {'credits/wk':>11} " + " ".join(f"{n.split(' (')[0][:9]:>10}" for n,_,_ in REFS))
ZP = {"GLM Lite $18": 10000, "GLM Pro $72": 60000, "GLM Max $160": 140000}
for p, c in ZP.items():
    row = []
    for _, i, o in REFS:
        cr = zai_credits(i, o); row.append(f"{c/cr:>10.1f}")
    print(f"{p:16} {c:>11,} " + " ".join(row))

print()
print("REQUEST-METERED PLANS (a request is a turn; a turn costs the whole context)")
print(f"{'plan':18} {'requests/mo':>12} {'measured tasks':>15} {'tokens @4k file':>17}")
CP = {"Copilot Pro $10": 1500, "Copilot Pro+ $39": 7000, "Copilot Max $100": 20000}
for p, q in CP.items():
    tasks = q/mean_turns
    toks = q*(mean_in/mean_turns + 4000)
    print(f"{p:18} {q:>12,} {tasks:>15.0f} {toks:>17,}")

print()
print("DOLLAR-CEILING PLANS (priced with the vendor's own token price)")
print(f"{'plan':18} {'ceiling':>8} {'model':>22} {'tokens':>14} {'small-file tasks':>18}")
def ceil_tasks(ceiling, pin, pout, model):
    ifr = mean_in/(mean_in+mean_out)
    blend = ifr*pin + (1-ifr)*pout
    tok = ceiling/blend*1e6
    return tok, tok/18145, tok/265445
for p, ce, pin, pout, m in [("OpenCode Go $10",60,0.14,0.28,"MiMo-V2.6-Flash"),
                            ("OpenCode Go+ $40",240,0.14,0.28,"MiMo-V2.6-Flash")]:
    tok, s, l = ceil_tasks(ce, pin, pout, m)
    print(f"{p:18} {ce:>8} {m:>22} {tok/1e6:>13,.0f}M {s:>18,.0f}")
    print(f"{'':18} {'':8} {'':22} {'(large file:':>13} {l:>18,.0f} tasks)")
