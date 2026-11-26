"""Entry point for news-image-20261126 (arm 2: the front page).

The renderer already drew the page; this stage puts it where the harness looks
and refuses to publish anything that is not the 1024-square 8-bit PNG the
competition asks for.
"""
import struct
from pathlib import Path

POSTER = Path(__file__).resolve().parent / "entry.png"
TARGET = Path("/output/entry.png")


def read_header(path):
    raw = path.read_bytes()
    if raw[:8] != b"\x89PNG\r\n\x1a\n":
        raise SystemExit("entry.png is not a PNG")
    width, height = struct.unpack(">II", raw[16:24])
    depth, colour = raw[24], raw[25]
    return raw, width, height, depth, colour


def main():
    raw, width, height, depth, colour = read_header(POSTER)
    if (width, height) != (1024, 1024):
        raise SystemExit("poster must be 1024x1024, got %dx%d" % (width, height))
    if depth != 8 or colour not in (2, 6):
        raise SystemExit("unexpected PNG depth/colour: %d/%d" % (depth, colour))
    target = TARGET
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
    except OSError:
        target = POSTER.with_name("out-entry.png")
        target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(raw)
    print("wrote", target, target.stat().st_size, "bytes", "%dx%d" % (width, height))


if __name__ == "__main__":
    main()
