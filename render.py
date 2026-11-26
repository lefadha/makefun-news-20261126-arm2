"""Draw 26 November 2026's world news as a FRONT PAGE (arm 2).

Every line comes from this run's own scan of 41 wire feeds
(`news26/scan_out.txt`), items timestamped 26 November 2026 00:00-08:00 GMT.
Nothing invented. No body copy: one lead headline at 42 px, six secondary
headlines at 30 px, three figure blocks and sixteen one-line briefs -- the
sizes a 300 px read keeps, instead of arm 1's 14 px detail.

Authored in this run's session (the run started 08:00Z, after the open).
"""
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
M = 30
RIGHT = W - M

PAPER = (250, 248, 243)
INK = (17, 19, 18)
SOFT = (80, 84, 79)
FAINT = (128, 132, 124)
RED = (166, 32, 28)
BLUE = (22, 46, 92)
RULE = (176, 170, 156)
PANEL = (255, 255, 252)

FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FSB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

DATE = "THURSDAY 26 NOVEMBER 2026"
TAG = "THE WORLD IN ONE DAY"
EDITION = "LIVE EDITION \u00b7 08:00 GMT"

LEAD = ("TRADE", "US sets 20% tariffs on Singapore and 13 partners")

FIGURES = [
    ("31", "killed in Cairo fuel-truck fire"),
    ("1,000,000", "satellites cleared for SpaceX"),
    ("13", "dead in Indonesia mine flood"),
]

STORIES = [
    ("TECH", "Nvidia halts chip exports to Asia"),
    ("ASIA", "Bank of Korea raises rates to 3.25%"),
    ("EUROPE", "EU leaders split over Ukraine funding"),
    ("SPORT", "Sinner out of Australian Open after surgery"),
    ("MIDEAST", "Gaza meningitis cases surge"),
    ("AFRICA", "Congo Ebola cases pass 12,000"),
]

BRIEFS = [
    ("EGYPT", "Cairo truck fire kills 31"),
    ("INDONESIA", "13 dead in mine flood"),
    ("USA", "Six die in air crash"),
    ("RUSSIA", "Trump, NATO warn Moscow"),
    ("ISRAEL", "New cabinet by week's end"),
    ("USA", "Macy's parade postponed"),
    ("TECH", "Apple pulls MiniMax app"),
    ("FRANCE", "Navy holds narco-sub"),
    ("IRAQ", "8 French jailed for life"),
    ("SRI LANKA", "Mass grave inquiry"),
    ("NKOREA", "Kim widens tactical nukes"),
    ("TECH", "Anthropic denies claim"),
    ("GAZA", "Meningitis cases surge"),
    ("SUDAN", "War, drought hit farmers"),
    ("AFGHAN", "Aid cuts hit women"),
    ("SPAIN", "Sanchez seeks reelection"),
]

FOOT = ("94 wire items from 41 feeds, 00:00-08:00 GMT \u00b7 "
        "one page, no body copy \u00b7 26.11.2026")

# vertical plan (1024-space)
DATE_Y = 46
FIG_NUM_Y, FIG_CAP_Y = 108, 178
LEAD_Y, LEAD_H = 230, 150
SEC_Y, SEC_H, SEC_GAP = 384, 92, 8
RAIL_HEAD_Y, RAIL_RULE_Y, RAIL_ROW_Y, RAIL_LH = 680, 702, 708, 30


def font(size, bold=False, serif=False):
    if serif:
        return ImageFont.truetype(FSB if bold else F, size)
    return ImageFont.truetype(FB if bold else F, size)


def tw(d, s, size, bold=False, serif=False):
    return d.textlength(s, font=font(size, bold, serif))


def wrap(d, text, size, bold, maxw, serif=False):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if tw(d, t, size, bold, serif) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def blocks(d):
    """Every text block with its box: build() draws these, audit() checks them."""
    B = []

    def add(bid, text, size, x, y, maxw, maxh, fill, bold=False, serif=False,
            wrap_=False, lh=None, right=None):
        B.append(dict(id=bid, text=text, size=size, x=x, y=y, maxw=maxw, maxh=maxh,
                      fill=fill, bold=bold, serif=serif, wrap=wrap_,
                      lh=lh or int(size * 1.15), right=right))

    add("tag", TAG, 15, M, 26, 420, 20, SOFT, bold=True)
    add("edition", EDITION, 15, RIGHT - 260, 26, 260, 20, SOFT, bold=True, right=RIGHT)
    add("date", DATE, 42, M, DATE_Y, RIGHT - M, 52, INK, bold=True, serif=True)

    col = (RIGHT - M) / 3
    for i, (num, cap) in enumerate(FIGURES):
        x = M + i * col
        add("fig%d_n" % i, num, 54, x, FIG_NUM_Y, col - 18, 64, RED, bold=True, serif=True)
        add("fig%d_c" % i, cap, 21, x, FIG_CAP_Y, col - 18, 48, SOFT, wrap_=True, lh=24)

    add("lead_k", "LEAD STORY \u00b7 " + LEAD[0], 17, M + 14, LEAD_Y + 10, 600, 22,
        RED, bold=True)
    add("lead_h", LEAD[1], 42, M + 14, LEAD_Y + 32, RIGHT - M - 28, 96, INK,
        bold=True, serif=True, wrap_=True, lh=46)

    gap = 20
    gw = (RIGHT - M - gap) / 2
    for i, (kicker, head) in enumerate(STORIES):
        cx = M + (i % 2) * (gw + gap)
        cy = SEC_Y + (i // 2) * (SEC_H + SEC_GAP)
        add("sec%d_k" % i, kicker, 16, cx + 14, cy + 7, gw - 28, 20, BLUE, bold=True)
        add("sec%d_h" % i, head, 30, cx + 14, cy + 28, gw - 28, 62, INK,
            bold=True, wrap_=True, lh=31)

    add("rail_head", "THE REST OF THE DAY", 16, M, RAIL_HEAD_Y, 400, 20, RED, bold=True)
    for i, (region, line) in enumerate(BRIEFS):
        cx = M + (i // 8) * gw
        ry = RAIL_ROW_Y + (i % 8) * RAIL_LH
        add("br%d_t" % i, region, 15, cx, ry + 3, 96, 18, BLUE, bold=True)
        add("br%d_h" % i, line, 24, cx + 100, ry, gw - 100, RAIL_LH, INK, bold=True)

    add("foot", FOOT, 12, M, 962, RIGHT - M, 16, FAINT)
    return B


def draw(d, S):
    """Draw the page at `S`x supersampling from the same block list."""
    page = blocks(d)
    d.rectangle([M * S, 98 * S, RIGHT * S, 103 * S], fill=RED)          # masthead rule
    d.rectangle([M * S, 214 * S, RIGHT * S, 215 * S], fill=RULE)        # under figures
    for i in range(1, 3):                                              # figure dividers
        x = M + i * (RIGHT - M) / 3
        d.rectangle([x * S, 112 * S, (x + 1) * S, 208 * S], fill=RULE)

    d.rectangle([M * S, LEAD_Y * S, RIGHT * S, (LEAD_Y + LEAD_H) * S], fill=PANEL)
    d.rectangle([M * S, LEAD_Y * S, (M + 6) * S, (LEAD_Y + LEAD_H) * S], fill=BLUE)

    gw = (RIGHT - M - 20) / 2
    for i in range(len(STORIES)):
        cx = M + (i % 2) * (gw + 20)
        cy = SEC_Y + (i // 2) * (SEC_H + SEC_GAP)
        d.rectangle([cx * S, cy * S, (cx + gw) * S, (cy + SEC_H) * S], fill=PANEL)
        d.rectangle([cx * S, cy * S, (cx + 4) * S, (cy + SEC_H) * S], fill=BLUE)

    d.rectangle([M * S, RAIL_RULE_Y * S, RIGHT * S, (RAIL_RULE_Y + 1) * S], fill=RULE)
    d.rectangle([M * S, 956 * S, RIGHT * S, 957 * S], fill=RULE)

    for b in page:
        lines = wrap(d, b["text"], b["size"], b["bold"], b["maxw"], b["serif"]) \
            if b["wrap"] else [b["text"]]
        for j, ln in enumerate(lines):
            wpx = tw(d, ln, b["size"], b["bold"], b["serif"])
            x = b["right"] - wpx if b["right"] else b["x"]
            d.text((x * S, (b["y"] + j * b["lh"]) * S),
                   ln, font=font(b["size"] * S, b["bold"], b["serif"]), fill=b["fill"])


def build(out="/opt/data/makefun/news26/entry2/entry.png", scale=2):
    img = Image.new("RGB", (W * scale, H * scale), PAPER)
    d = ImageDraw.Draw(img)
    draw(d, scale)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img.resize((W, H), Image.LANCZOS).save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    build()
