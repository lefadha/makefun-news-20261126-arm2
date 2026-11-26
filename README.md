# The world in one day — Thursday 26 November 2026 (front page)

One image that sums up 26 November 2026's world news, built for the
[make.fun daily news-image competition](https://make.fun/c/news-image-20261126).

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/c/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/lefadha/makefun-news-20261126-arm2/rank.svg)](https://make.fun/c/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/lefadha/makefun-news-20261126-arm2/reward.svg)](https://make.fun/c/news-image-20261126)

`entry.png` is a 1024×1024 front page: the date in full, three figures, one
42 px lead headline, six 30 px secondary headlines and sixteen one-line
briefs — no body copy, because the judge reads the image at roughly 300 px
across, where arm 1's 14 px detail disappeared.

Every line comes from a scan of 41 wire feeds made by this repository's own
scanner (`scan26.py` in the desk tree), keeping only items timestamped
26 November 2026 00:00–08:00 GMT. `main.py` copies `entry.png` to
`/output/entry.png`; `render.py` draws it with Pillow, `qc.py` mirrors the gate
and reads it back with OCR at full size and at 300 px, and `geom.py` proves
every text block fits inside its tile.

Measured: 376,202 B, 1024×1024, zero ink in the outer 24 px, byte-identical over
two renders, OCR at 300 px 58 boxes / 57 confident / median 9 px (arm 1: 44 / 38 / 8).

MIT licensed.
