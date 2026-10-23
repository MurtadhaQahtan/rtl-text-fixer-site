"""Renders before/after demo images with Pillow's BASIC layout engine: glyphs drawn strictly left-to-right with no shaping
and no bidi — the way apps without right-to-left support draw text. Row 1: the text pasted as-is. Row 2: the output of
RTL Text Fixer (computed by the real engine, _src/fixed.json)."""
import json, os
from PIL import Image, ImageDraw, ImageFont
G = "/usr/share/fonts/truetype/sand-box/google/"
FONTS = {"arab": G + "Noto Sans Arabic/NotoSansArabic-VariableFont_wdth,wght.ttf", "hebr": G + "IBM Plex Sans Hebrew/IBMPlexSansHebrew-Regular.ttf"}
S = json.load(open("_src/samples.json", encoding="utf-8")); F = json.load(open("_src/fixed.json", encoding="utf-8"))
os.makedirs("img", exist_ok=True)
for k in S:
    font = ImageFont.truetype(FONTS["hebr" if k in ("he", "yi") else "arab"], 40, layout_engine=ImageFont.Layout.BASIC)
    w = int(max(font.getlength(S[k]), font.getlength(F[k]))) + 130
    im = Image.new("RGB", (max(w, 600), 190), "white"); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, im.width - 1, 89], 10, fill=(253, 240, 240)); d.rounded_rectangle([0, 100, im.width - 1, 189], 10, fill=(236, 248, 240))
    r, c = (200, 40, 40), (20, 140, 70)   # cross and check drawn as lines
    d.line([(28, 32), (54, 58)], fill=r, width=6); d.line([(54, 32), (28, 58)], fill=r, width=6)
    d.line([(26, 146), (36, 158), (58, 130)], fill=c, width=6, joint="curve")
    d.text((90, 45), S[k], font=font, fill=(30, 30, 30), anchor="lm"); d.text((90, 145), F[k], font=font, fill=(30, 30, 30), anchor="lm")
    im.save(f"img/demo-{k}.png", optimize=True)
print("ok")
