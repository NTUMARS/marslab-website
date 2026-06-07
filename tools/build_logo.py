#!/usr/bin/env python3
"""Build MARS Lab header logo + favicons from the planet emblem.

Header logo: orange planet emblem + dark "MARS / Lab" wordmark (reads on white).
Favicons: square planet emblem at standard sizes. SVG wrappers embed the PNG so
the Astro template needs no markup changes (logo.svg / favicon.svg keep names).
"""
import base64
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PUB = os.path.abspath(os.path.join(HERE, "..", "public"))
DARK = (26, 26, 24, 255)  # ~ --primary-color

# --- 1. emblem (planet + near star), transparent bg ---
logo = Image.open(os.path.join(HERE, "live_logo.png")).convert("RGBA")
emblem = logo.crop((40, 30, 700, 690))            # 660x660 square
# tight square emblem for favicons (drop the star, center the planet)
fav = logo.crop((40, 110, 660, 690))              # planet-focused
fs = max(fav.size)
favsq = Image.new("RGBA", (fs, fs), (0, 0, 0, 0))
favsq.paste(fav, ((fs - fav.size[0]) // 2, (fs - fav.size[1]) // 2), fav)


def font(path, size):
    return ImageFont.truetype(path, size)

AVENIR = "/System/Library/Fonts/Avenir Next.ttc"
# Avenir Next.ttc faces: index 0..; pick Heavy (bold geometric)
f_mars = ImageFont.truetype(AVENIR, 200, index=7)   # Heavy
f_lab = ImageFont.truetype(AVENIR, 158, index=5)    # Demi/Bold

# --- 2. header logo: emblem + stacked "MARS" / "Lab" ---
em_h = 360
em = emblem.resize((round(emblem.size[0] * em_h / emblem.size[1]), em_h),
                   Image.LANCZOS)
pad = 20
text_x = pad + em.size[0] + 30
canvas_w = text_x + 560
canvas_h = 420
logo_img = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
logo_img.paste(em, (pad, (canvas_h - em_h) // 2 + 6), em)
d = ImageDraw.Draw(logo_img)
# MARS (top), Lab (below), left-aligned, vertically centered as a block
def th(f, t):
    b = d.textbbox((0, 0), t, font=f)
    return b[3] - b[1], b[1]
mh, mo = th(f_mars, "MARS")
lh, lo = th(f_lab, "Lab")
gap = 18
block_h = mh + gap + lh
top = (canvas_h - block_h) // 2
d.text((text_x, top - mo), "MARS", font=f_mars, fill=DARK)
d.text((text_x, top + mh + gap - lo), "Lab", font=f_lab, fill=DARK)
# trim transparent margins on the right
bbox = logo_img.getbbox()
logo_img = logo_img.crop((0, 0, bbox[2] + pad, canvas_h))
logo_img.save(os.path.join(PUB, "logo.png"))
print("logo.png", logo_img.size)


def svg_wrap(png_path, out_path):
    with open(png_path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode()
    im = Image.open(png_path)
    w, h = im.size
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" '
           f'xmlns:xlink="http://www.w3.org/1999/xlink" '
           f'width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<image width="{w}" height="{h}" '
           f'xlink:href="data:image/png;base64,{b64}"/></svg>')
    with open(out_path, "w") as fh:
        fh.write(svg)


svg_wrap(os.path.join(PUB, "logo.png"), os.path.join(PUB, "logo.svg"))

# --- 3. favicons (square planet) ---
def save_png(size, name, bg=None):
    canvas = Image.new("RGBA", (size, size), bg or (0, 0, 0, 0))
    inner = round(size * 0.92)
    r = favsq.resize((inner, inner), Image.LANCZOS)
    off = (size - inner) // 2
    canvas.alpha_composite(r, (off, off))
    if bg:
        canvas = canvas.convert("RGB")
    canvas.save(os.path.join(PUB, name))

save_png(96, "favicon-96x96.png")
save_png(180, "apple-touch-icon.png", bg=(255, 255, 255))
save_png(192, "web-app-manifest-192x192.png", bg=(255, 255, 255))
save_png(512, "web-app-manifest-512x512.png", bg=(255, 255, 255))
# favicon.ico (multi-size)
ico = favsq.resize((256, 256), Image.LANCZOS)
ico.save(os.path.join(PUB, "favicon.ico"),
         sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
# favicon.svg wrapper from a 256 png
save_png(256, "_favsrc.png")
svg_wrap(os.path.join(PUB, "_favsrc.png"), os.path.join(PUB, "favicon.svg"))
os.remove(os.path.join(PUB, "_favsrc.png"))
print("favicons written")
