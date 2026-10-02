#!/usr/bin/env python3
"""Compare the 2026-10-02 table against what the 2026-10-03 pages actually say.

Prints, per provider, the OLD row and the NEW evidence side by side. Deliberately
does not compute a verdict: a human (or the report) decides whether a difference is
drift, a correction of an old error, or neither.
"""
import csv
import pathlib
import re

OLD = list(csv.DictReader(open("2026-10-02/data/first-party-plans.csv")))

# provider -> (evidence string pulled live on 2026-10-03, note)
NEW = {
 "Cursor": ("pro=20 pro+=60 ultra=200 teams=40 (schema.org offers on cursor.com/pricing)",
            "Pro+ $60 tier is NEW vs the 2026-10-02 table"),
 "Command Code": ("go=1 goat=10 pro=20 max10x=100 max20x=200; credits 10/70/80/150/300",
                  "unchanged"),
 "OpenCode": ("go=10 plus=40; 5h=20%/week=50%/month=100%", "unchanged"),
 "Trae": ("free=0 pro=20 pro+=60 ultra=200", "unchanged"),
 "Anthropic": ("pro=20 (17 annual) max from 100 (5x) / 200 (20x)", "unchanged"),
 "GitHub": ("pro=10 pro+=39 max=100", "unchanged"),
 "Mistral": ("pro=14.99; $10/mo API credits", "unchanged"),
 "Warp": ("build=20 max=200; build 1500 credits, max 18000 credits", "unchanged"),
 "Replit": ("core=20 (18 annual)", "unchanged"),
 "Zed": ("pro=10", "unchanged"),
 "DeepSeek": ("v4.1-flash off-peak $0.15/$0.60, peak $0.30/$1.20", "unchanged"),
}

print(f"{'provider':24} {'OLD price/tool':40} {'OLD quota':28} NEW")
print("="*140)
for r in OLD:
    p = r["provider"]
    if p in NEW:
        ev, note = NEW[p]
        print(f"{p:24} {r['coding_tool'][:38]:40} {r['published_quota'][:26]:28} {ev}")
