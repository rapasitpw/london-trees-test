# London's Street Trees, by Borough

An interactive visualisation of the ~1.14 million publicly maintained trees in
London, showing how they are distributed across the city's 33 boroughs.

**Live site:** https://rapasitpw.github.io/london-trees-test/

Built for the CCI *Visualisation and Sensing* project.

## What it does

- A **choropleth map** (Leaflet) shades each borough by its tree count — darker
  greens mean more trees. Hover a borough to see its exact figure.
- A **ranked bar chart** (D3) lists every borough, sortable by tree count or
  alphabetically.
- The map and chart are **linked**: click a bar or a borough to highlight it in
  both views and zoom the map to it.

## The data

Source: [London Public Realm Trees](https://data.london.gov.uk/dataset/local-authority-maintained-trees/),
Greater London Authority, via the London Datastore (UK Open Government Licence).

The raw dataset is ~1.14 million rows and far too large to render point-by-point
in a browser. `aggregate.py` reduces it **once, offline** to a small
`borough_counts.json` (33 borough totals), which is what the web page loads.

> Note: some boroughs (Croydon, Havering, City of London) appear very low
> because they released only partial data, not because they lack trees.

## Files

| File | Purpose |
|------|---------|
| `index.html` | The whole site — map, chart, styling and logic in one file |
| `borough_counts.json` | Aggregated data the site loads (borough → tree count) |
| `boroughs.geojson` | London borough boundary polygons for the map |
| `aggregate.py` | Script that generates `borough_counts.json` from the raw CSV |

## Running it

It's a static site — no build step. Because the browser loads local files
(`borough_counts.json`, `boroughs.geojson`), open it through a web server rather
than `file://`:

```bash
python -m http.server 8000
# then visit http://localhost:8000
```

Or just deploy the folder to GitHub Pages.

## Re-generating the data

```bash
# place Borough_tree_list_2025Nov.csv (from the London Datastore) alongside aggregate.py
python aggregate.py   # writes borough_counts.json
```

## Built with

[Leaflet](https://leafletjs.com/) · [D3.js](https://d3js.org/) · GitHub Pages
