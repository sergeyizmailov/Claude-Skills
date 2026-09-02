#!/usr/bin/env python3
"""Make one creative file into N byte-distinct variants, one per account.

    python3 uniquify.py creatives/slots.mp4 --n 5 --out creatives/uniq/
    python3 uniquify.py creatives/*.jpg --n 3 --out creatives/uniq/ --tags J41-16,J41-17,J41-18

Images (Pillow): crop 1–4 px per edge (random per variant), ±1% brightness, re-encode JPEG at
a jittered quality, strip EXIF. Videos (ffmpeg): trim 40–160 ms from the head, scale to a
1-2 px different even size back to original via crop, re-encode (x264 CRF jitter), re-mux;
audio copied. Output names carry the tag or the index: slots.J41-16.mp4.

Then upload per account with media.py — hashes are account-scoped anyway (04 → Media). What
this buys: identical bytes across accounts is an UNVERIFIED linking hypothesis; the cost of
insurance is a few seconds of CPU. It does not "pass review" — content is what reviewers see.

Deterministic per (file, tag): the same input and tag always produce the same output, so a
re-run does not create a new variant for an account that already has one.
"""

from __future__ import annotations

import argparse
import hashlib
import pathlib
import random
import shutil
import subprocess
import sys

IMG = {".jpg", ".jpeg", ".png", ".webp"}
VID = {".mp4", ".mov", ".m4v"}


def seed_for(path: pathlib.Path, tag: str) -> random.Random:
    h = hashlib.sha256((path.name + "|" + tag).encode()).hexdigest()
    return random.Random(int(h[:16], 16))


def uniq_image(src: pathlib.Path, dst: pathlib.Path, rnd: random.Random) -> None:
    try:
        from PIL import Image, ImageEnhance
    except ImportError:
        sys.exit("pip install pillow")
    im = Image.open(src).convert("RGB")
    w, h = im.size
    left, top, right, bottom = (rnd.randint(1, 4) for _ in range(4))
    im = im.crop((left, top, w - right, h - bottom))
    im = ImageEnhance.Brightness(im).enhance(1 + rnd.uniform(-0.01, 0.01))
    if dst.suffix.lower() in (".jpg", ".jpeg"):
        im.save(dst, "JPEG", quality=rnd.randint(88, 95), optimize=True)
    else:
        im.save(dst)


def uniq_video(src: pathlib.Path, dst: pathlib.Path, rnd: random.Random) -> None:
    if not shutil.which("ffmpeg"):
        sys.exit("ffmpeg not found (brew install ffmpeg)")
    trim = rnd.randint(40, 160) / 1000
    crf = rnd.randint(19, 23)
    dx, dy = rnd.choice([0, 2]), rnd.choice([0, 2])
    vf = f"crop=iw-{dx}:ih-{dy}:{dx // 2}:{dy // 2},scale=trunc(iw/2)*2:trunc(ih/2)*2" if (dx or dy) else "scale=trunc(iw/2)*2:trunc(ih/2)*2"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{trim:.3f}", "-i", str(src),
           "-vf", vf, "-c:v", "libx264", "-crf", str(crf), "-preset", "medium", "-pix_fmt", "yuv420p",
           "-c:a", "copy", "-movflags", "+faststart", "-map_metadata", "-1", str(dst)]
    subprocess.run(cmd, check=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--n", type=int, help="number of variants (ignored when --tags is given)")
    ap.add_argument("--tags", help="comma-separated account tags → one variant per tag")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    tags = [t.strip() for t in args.tags.split(",")] if args.tags else [f"v{i:02d}" for i in range(1, (args.n or 1) + 1)]
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    made = 0
    for f in args.files:
        src = pathlib.Path(f)
        ext = src.suffix.lower()
        if ext not in IMG | VID:
            print(f"  skip {src.name}: unsupported type")
            continue
        for tag in tags:
            dst = out / f"{src.stem}.{tag}{ext}"
            if dst.exists():
                print(f"  = {dst.name} (exists)")
                continue
            rnd = seed_for(src, tag)
            (uniq_image if ext in IMG else uniq_video)(src, dst, rnd)
            print(f"  + {dst.name}")
            made += 1
    print(f"\n{made} variant(s) → {out}. Upload each with media.py --account <the tag's account>.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
