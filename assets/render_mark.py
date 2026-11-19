from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

out_dir = Path(__file__).resolve().parent
words = ["Plain", "Text", "Humans"]

font_paths = [
    out_dir / "fonts" / "IBMPlexMono-SemiBold.ttf",
    Path(r"C:\Windows\Fonts\IBMPlexMono-SemiBold.ttf"),
    Path(r"C:\Windows\Fonts\arialbd.ttf"),
]
font_path = next((p for p in font_paths if Path(p).exists()), None)
if not font_path:
    raise SystemExit("No suitable font found (need IBM Plex Mono SemiBold)")

size = 120
font = ImageFont.truetype(str(font_path), size)
# Side pads + tight leading between stacked bars
pads_x, pads_y = 24, 6

rows = []
for w in words:
    bbox = font.getbbox(w)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    bar_w = tw + pads_x * 2
    bar_h = th + pads_y * 2
    rows.append((w, tw, th, bbox, bar_w, bar_h))

bar_h = max(r[5] for r in rows)
rows = [(w, tw, th, bbox, bar_w, bar_h) for w, tw, th, bbox, bar_w, _ in rows]

width = max(r[4] for r in rows)
height = bar_h * len(rows)

# Left-aligned stacked bars (flush left)
mark = Image.new("RGBA", (width, height), (0, 0, 0, 0))
draw = ImageDraw.Draw(mark)
y = 0
for w, tw, th, bbox, bar_w, bh in rows:
    x0 = 0
    draw.rectangle([x0, y, x0 + bar_w, y + bh], fill=(0, 0, 0, 255))
    tx = x0 + pads_x - bbox[0]
    ty = y + (bh - th) // 2 - bbox[1]
    draw.text((tx, ty), w, font=font, fill=(255, 255, 255, 255))
    y += bh

mark_path = out_dir / "mark.png"
mark.save(mark_path)
print("wrote", mark_path, mark.size, "font", font_path)
