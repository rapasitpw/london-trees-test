"""
aggregate.py
------------
Reduces the full GLA London Public Realm Trees dataset (~1.1 million rows)
down to a small per-borough summary, saved as borough_data.json.

For each borough it records:
  - count    : number of trees
  - area_km2 : borough land area, computed from the boundary polygons
  - per_km2  : trees per square kilometre (count / area)

Why: 1.1M individual points cannot be rendered in a browser map without
crashing. We aggregate to 33 borough summaries ONCE, offline, and the web page
loads only the small JSON result. Areas are computed here too so the page needs
no geometry maths at run time.

Inputs : Borough_tree_list_2025Nov.csv  (tree records, from the London Datastore)
         boroughs.geojson               (borough boundary polygons)
Output : borough_data.json
Usage  : python aggregate.py

Requires: shapely, pyproj  (pip install shapely pyproj)
"""

import csv
import json
import collections
from shapely.geometry import shape
from shapely.ops import transform
from pyproj import Transformer

TREES = "Borough_tree_list_2025Nov.csv"
SHAPES = "boroughs.geojson"
OUTPUT = "borough_data.json"

# 1. count trees per borough
counts = collections.Counter()
with open(TREES, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f):
        b = (row["borough"] or "").strip()
        if b:
            counts[b] += 1

# 2. borough areas from the polygons.
#    Transform lon/lat (EPSG:4326) to British National Grid (EPSG:27700, metres)
#    so that .area is correct in square metres.
to_metres = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True).transform
geo = json.load(open(SHAPES))

out = {}
for feature in geo["features"]:
    name = feature["properties"]["name"]
    area_km2 = transform(to_metres, shape(feature["geometry"])).area / 1_000_000
    n = counts.get(name, 0)
    out[name] = {
        "count": n,
        "area_km2": round(area_km2, 2),
        "per_km2": round(n / area_km2, 1),
    }

# 3. sort by count (descending) and write
out = dict(sorted(out.items(), key=lambda kv: -kv[1]["count"]))
with open(OUTPUT, "w") as fh:
    json.dump(out, fh, indent=2)

total = sum(v["count"] for v in out.values())
print(f"Wrote {OUTPUT}: {len(out)} boroughs, {total:,} trees total")
