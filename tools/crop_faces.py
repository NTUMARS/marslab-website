#!/usr/bin/env python3
"""Face-aware square crops for MARS Lab people photos.

Reads every image in tools/src_photos/, detects the largest face, and crops a
square framed with headroom above the head and shoulders below, then resizes to
800x800 and writes to public/people/<slug>.jpg. Falls back to a centered square
crop when no face is found. Per-image manual overrides live in OVERRIDES.

Also writes tools/contact_sheet.png (a labeled grid) for quick visual review.
"""
import os
import glob
import cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src_photos")
OUT = os.path.join(HERE, "..", "public", "people")
OUT = os.path.abspath(OUT)
SHEET = os.path.join(HERE, "contact_sheet.png")
SIZE = 800

# Per-slug tuning. scale = square side as multiple of detected face height.
# v_pos = where the face CENTER sits vertically inside the square (0=top,1=bottom).
# dx/dy = extra pixel nudge of the crop window (in source px) after placement.
OVERRIDES = {
    # slug: dict(scale=, v_pos=, dx=, dy=)
    "yanshuo-lu": dict(scale=1.7, v_pos=0.42),
    "chenxi-jiang": dict(scale=2.35, v_pos=0.32, dx=120),
    "kuangji-zuo": dict(scale=1.15, v_pos=0.50, dx=-80),
}
# Force a face box (x, y, w, h) in source pixels when detection fails or is bad.
FACE_OVERRIDE = {
    "yanshuo-lu": (40, 330, 330, 330),
    "chenxi-jiang": (1500, 860, 340, 490),
    "kuangji-zuo": (360, 720, 960, 1360),
}
DEFAULT = dict(scale=2.9, v_pos=0.44, dx=0, dy=0)

cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)
alt = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"
)


def detect_face(cv_img):
    gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    for clf in (cascade, alt):
        faces = clf.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=6,
                                     minSize=(60, 60))
        if len(faces):
            # largest by area
            return max(faces, key=lambda f: f[2] * f[3])
    return None


def square_box(W, H, face, cfg):
    """Return (left, top, side) integer square within image bounds."""
    if face is None:
        side = min(W, H)
        left = (W - side) // 2
        top = (H - side) // 2
        return left, top, side
    x, y, w, h = face
    fcx = x + w / 2.0
    fcy = y + h / 2.0
    side = h * cfg["scale"]
    side = min(side, W, H)          # cannot exceed image
    side = int(round(side))
    left = fcx - side / 2.0 + cfg["dx"]
    top = fcy - side * cfg["v_pos"] + cfg["dy"]
    left = int(round(max(0, min(left, W - side))))
    top = int(round(max(0, min(top, H - side))))
    return left, top, side


def process(path):
    slug = os.path.splitext(os.path.basename(path))[0]
    cfg = {**DEFAULT, **OVERRIDES.get(slug, {})}
    pil = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    W, H = pil.size
    # detect on an exif-correct CV image
    import numpy as np
    cv_img = cv2.cvtColor(np.array(pil), cv2.COLOR_RGB2BGR)
    if slug in FACE_OVERRIDE:
        face = FACE_OVERRIDE[slug]
    else:
        face = detect_face(cv_img)
    left, top, side = square_box(W, H, face, cfg)
    crop = pil.crop((left, top, left + side, top + side)).resize(
        (SIZE, SIZE), Image.LANCZOS)
    os.makedirs(OUT, exist_ok=True)
    crop.save(os.path.join(OUT, slug + ".jpg"), "JPEG", quality=90)
    return slug, (face is not None), crop


def contact_sheet(items):
    cols = 5
    cell = 300
    pad = 8
    label_h = 22
    rows = (len(items) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell, rows * (cell + label_h)), "#ffffff")
    draw = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial.ttf", 14)
    except Exception:
        font = ImageFont.load_default()
    for i, (slug, has_face, crop) in enumerate(items):
        r, c = divmod(i, cols)
        x = c * cell
        y = r * (cell + label_h)
        thumb = crop.resize((cell - 2 * pad, cell - 2 * pad), Image.LANCZOS)
        sheet.paste(thumb, (x + pad, y + pad))
        tag = slug + ("" if has_face else "  [no-face]")
        draw.text((x + pad, y + cell - pad), tag, fill="#000000", font=font)
    sheet.save(SHEET)
    print("contact sheet ->", SHEET)


def main():
    paths = sorted(glob.glob(os.path.join(SRC, "*")))
    items = []
    for p in paths:
        if os.path.basename(p).startswith("."):
            continue
        slug, has_face, crop = process(p)
        print(f"{'OK ' if has_face else 'NF '} {slug}")
        items.append((slug, has_face, crop))
    contact_sheet(items)
    print(f"done: {len(items)} images -> {OUT}")


if __name__ == "__main__":
    main()
