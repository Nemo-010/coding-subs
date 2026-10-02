#!/usr/bin/env python3
import json
bench=json.load(open("bench.json")); reps=json.load(open("scale_reps.json"))
nl=json.load(open("bench_nolist.json"))
S=[r for r in bench if r["solved"]]
mean_turns=sum(r["turns"] for r in S)/len(S)
mean_in=sum(r["in_tokens"] for r in S)/len(S)
mean_out=sum(r["out_tokens"] for r in S)/len(S)
cache=sum(x["cache_frac"] for r in reps for x in r["runs"])/sum(len(r["runs"]) for r in reps)

def zai_credits(i,o,cache,im=6.9,cm=1.7,om=24.0):
    return (i*(1-cache)*im + i*cache*cm + o*om)/10000.0

print(f"SHAPE: {len(S)}/{len(bench)} solved  {mean_turns:.1f} turns  {mean_in:,.0f} in  {mean_out:,.0f} out  cache={cache:.2f}")
print()
print("SCALING (3 reps each, identical one-line fix, only file size varies)")
print(f"{'file tok':>10} {'mean in':>11} {'min':>10} {'max':>10} {'spread':>7} {'mean/file':>10}")
for r in reps:
    print(f"{r['file_tokens']:>10,} {r['in_mean']:>11,} {r['in_min']:>10,} {r['in_max']:>10,} "
          f"{r['in_max']/max(r['in_min'],1):>6.1f}x {r['in_mean']/r['file_tokens']:>9.1f}x")
print()
print("Z.AI CREDITS per reference session (GLM-5.3 weighting, measured cache)")
print(f"{'file tok':>10} {'mean in':>11} {'credits':>9}")
refs=[]
for r in reps:
    o=mean_out*(r['in_mean']/mean_in) if mean_in else mean_out
    cr=zai_credits(r['in_mean'],o,cache)
    refs.append((r['file_tokens'],r['in_mean'],cr))
    print(f"{r['file_tokens']:>10,} {r['in_mean']:>11,} {cr:>9.1f}")
print()
print("Z.AI PLANS -> sessions/week")
print(f"{'plan':16} {'credits/wk':>11} " + " ".join(f"{f'{t//1000}k':>8}" for t,_,_ in refs))
for p,c in {"GLM Lite $18":10000,"GLM Pro $72":60000,"GLM Max $160":140000}.items():
    print(f"{p:16} {c:>11,} " + " ".join(f"{c/cr:>8.0f}" for _,_,cr in refs))
print()
print("REQUEST-METERED (a request = a turn)")
for p,q in {"Copilot Pro $10":1500,"Copilot Pro+ $39":7000,"Copilot Max $100":20000}.items():
    print(f"  {p:18} {q:>7,} req/mo -> {q/mean_turns:>6.0f} measured tasks")
print()
print("WITHOUT-LIST WASTE")
t=sum(x['in_tokens']+x['out_tokens'] for x in nl); w=sum(x['in_tokens']+x['out_tokens'] for x in nl if not x['solved'])
print(f"  {sum(1 for x in nl if x['solved'])}/8 solved; {w:,} of {t:,} tokens = {100*w/t:.0f}% spent on unsolved tasks")
