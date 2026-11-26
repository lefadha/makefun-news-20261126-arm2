"""Geometry gate for arm 2: every text block fits its tile and the page.

Uses the renderer's own block list, so what is measured here is exactly what
build() draws: wrapped height vs the tile height, line width vs the tile width,
and the block's edges vs the 24 px ink border.
"""
import sys

sys.path.insert(0, "/opt/data/makefun/news26/entry2")
from PIL import Image, ImageDraw  # noqa: E402

import render as R  # noqa: E402

d = ImageDraw.Draw(Image.new("RGB", (R.W, R.H)))
bad = 0
worst = []
for b in R.blocks(d):
    lines = R.wrap(d, b["text"], b["size"], b["bold"], b["maxw"], b["serif"]) \
        if b["wrap"] else [b["text"]]
    wid = max(R.tw(d, ln, b["size"], b["bold"], b["serif"]) for ln in lines)
    hei = len(lines) * b["lh"]
    x0 = b["right"] - wid if b["right"] else b["x"]
    fits = wid <= b["maxw"] + 0.5 and hei <= b["maxh"] and len(lines) <= 3
    inside = x0 >= 24 and x0 + wid <= R.W - 24 and b["y"] >= 24 and b["y"] + hei <= R.H - 24
    ok = fits and inside
    bad += 0 if ok else 1
    worst.append((b["maxh"] - hei, b["id"], len(lines), round(wid), round(hei), b["maxh"], ok))
    if not ok:
        print("OVERFLOW", b["id"], "lines", len(lines), "w", round(wid), "of", b["maxw"],
              "h", round(hei), "of", b["maxh"], "x0", round(x0))

tight = sorted(worst)[:6]
print("blocks", len(worst), "overflow", bad)
print("tightest:", ", ".join("%s %spx/%s" % (i[1], i[4], i[5]) for i in tight))
print("text runs at full size:", sum(len(R.wrap(d, b["text"], b["size"], b["bold"],
                                               b["maxw"], b["serif"]))
                                     if b["wrap"] else 1 for b in R.blocks(d)))
print("GEOM", "PASS" if bad == 0 else "FAIL")
