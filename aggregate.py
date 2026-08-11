"""
aggregate.py
------------
Reduces the full GLA London Public Realm Trees dataset (~1.1 million rows)
down to a small borough -> tree-count summary, saved as borough_counts.json.

Why: 1.1M individual points cannot be rendered in a browser map without
crashing. We aggregate to 33 borough totals ONCE, offline, and the web page
loads only the small JSON result.

Input : Borough_tree_list_2025Nov.csv  (from the London Datastore)
Output: borough_counts.json
Usage : python aggregate.py
"""

import csv
import json
import collections

INPUT = "Borough_tree_list_2025Nov.csv"
OUTPUT = "borough_counts.json"

counts = collections.Counter()

# utf-8-sig strips the byte-order mark (BOM) at the start of the file
with open(INPUT, encoding="utf-8-sig", newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        borough = (row["borough"] or "").strip()
        if borough:
            counts[borough] += 1

# sort boroughs from most trees to fewest
data = dict(sorted(counts.items(), key=lambda kv: -kv[1]))

with open(OUTPUT, "w") as out:
    json.dump(data, out, indent=2)

print(f"Wrote {OUTPUT}: {len(data)} boroughs, {sum(data.values()):,} trees total")
