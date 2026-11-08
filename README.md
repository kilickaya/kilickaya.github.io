# Mert Kilickaya’s research website

A buildless GitHub Pages site. Edit `index.html` for research and career content, `images.html` for photography, and `assets/css/editorial.css` for the shared design.

Preview locally with `python3 -m http.server 4173`, then open <http://localhost:4173>.

After content edits, regenerate the static profile exports and page metadata:

```sh
python3 scripts/build-profile.py
python3 scripts/build-profile.py --check
```

The generator reads the visible HTML and writes `profile.md`, `profile.json`, `llms.txt`, `publications.bib`, `robots.txt`, `sitemap.xml`, and the marked metadata blocks in both pages. It needs only Python’s standard library. Year-only dates stay year-only; missing values stay unspecified. It does not invent author lists, dates, employment status, metrics, or academic identifiers. `llms.txt` is a supplemental discovery aid, not a requirement for using the other exports.

Publication concept illustrations live in `images/research/`. Regenerate them with `python3 scripts/draw-publications.py`; their source notes are in `images/research/README.md`.

See `CONTENT-NOTES.md` for content provenance and details awaiting verification. Existing paper, slide, patent, supervision, CV and photography links are retained.
