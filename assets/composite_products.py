"""Composite the stacked mark onto tote/tee blanks with print-like lighting + fabric warp."""
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

root = Path(__file__).resolve().parent
blank_dir = Path(r"C:\Users\Bruno\.cursor\projects\d-repos-PTH\assets")

mark = Image.open(root / "mark.png").convert("RGBA")

for name in ("tote-blank.jpg", "tee-blank.jpg"):
    src = blank_dir / name
    local = root / name
    if src.exists():
        Image.open(src).convert("RGB").save(local, quality=92)


def tight_square(im: Image.Image, crop) -> Image.Image:
    """Crop then force 1200 square."""
    w, h = im.size
    l, t, r, b = crop
    box = (int(w * l), int(h * t), int(w * r), int(h * b))
    c = im.crop(box)
    side = min(c.size)
    cx, cy = c.width // 2, c.height // 2
    half = side // 2
    sq = c.crop((cx - half, cy - half, cx - half + side, cy - half + side))
    return sq.resize((1200, 1200), Image.Resampling.LANCZOS)


def ink_mask(rgba: Image.Image) -> np.ndarray:
    """0..1 ink coverage: black printed areas only (white text knocks out)."""
    arr = np.asarray(rgba).astype(np.float32)
    rgb = arr[..., :3]
    a = arr[..., 3] / 255.0
    luma = rgb.mean(axis=2) / 255.0
    ink = a * (1.0 - luma)
    ink = np.where(ink < 0.35, 0.0, np.where(ink > 0.65, 1.0, (ink - 0.35) / 0.3))
    return np.clip(ink, 0.0, 1.0)


def warp_to_fabric(ink: np.ndarray, fabric_rgb: np.ndarray, amount: float) -> np.ndarray:
    """Nudge the ink mask along fabric luminance gradients so it follows folds."""
    if amount <= 0:
        return ink
    gray = fabric_rgb.mean(axis=2)
    gray = np.asarray(
        Image.fromarray(gray.astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=3)),
        dtype=np.float32,
    )
    gy, gx = np.gradient(gray)
    scale = amount / (np.mean(np.abs(gx)) + np.mean(np.abs(gy)) + 1e-6)
    h, w = ink.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    src_y = np.clip(yy + gy * scale, 0, h - 1)
    src_x = np.clip(xx + gx * scale, 0, w - 1)
    y0 = np.floor(src_y).astype(np.int32)
    x0 = np.floor(src_x).astype(np.int32)
    y1 = np.clip(y0 + 1, 0, h - 1)
    x1 = np.clip(x0 + 1, 0, w - 1)
    wy = src_y - y0
    wx = src_x - x0
    i00 = ink[y0, x0]
    i01 = ink[y0, x1]
    i10 = ink[y1, x0]
    i11 = ink[y1, x1]
    top = i00 * (1 - wx) + i01 * wx
    bot = i10 * (1 - wx) + i11 * wx
    return top * (1 - wy) + bot * wy


def place(
    base: Image.Image,
    center,
    max_w: int,
    *,
    strength: float = 0.94,
    warp: float = 1.0,
) -> Image.Image:
    """Multiply black ink into fabric with soft fold lighting."""
    fabric = np.asarray(base.convert("RGB"), dtype=np.float32)
    scale = max_w / mark.width
    nw = max(1, int(mark.width * scale))
    nh = max(1, int(mark.height * scale))
    m = mark.resize((nw, nh), Image.Resampling.LANCZOS)
    x = int(center[0] - nw / 2)
    y = int(center[1] - nh / 2)
    x = max(0, min(x, fabric.shape[1] - nw))
    y = max(0, min(y, fabric.shape[0] - nh))

    region = fabric[y : y + nh, x : x + nw]
    ink = warp_to_fabric(ink_mask(m), region, amount=warp)

    lit = np.asarray(
        Image.fromarray(region.astype(np.uint8)).filter(ImageFilter.GaussianBlur(radius=10)),
        dtype=np.float32,
    )
    ink_rgb = ink[..., None]
    printed = region * (1.0 - ink_rgb) + lit * (1.0 - strength * ink_rgb) * ink_rgb

    out = fabric.copy()
    out[y : y + nh, x : x + nw] = printed
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8), mode="RGB")


tote_base = tight_square(Image.open(root / "tote-blank.jpg"), (0.18, 0.02, 0.82, 0.98))
tee_base = tight_square(Image.open(root / "tee-blank.jpg"), (0.18, 0.05, 0.82, 0.98))

tote = place(tote_base, center=(480, 760), max_w=480, strength=0.94, warp=1.5)
tee = place(tee_base, center=(600, 380), max_w=440, strength=0.93, warp=1.0)

tote.save(root / "tote.png", optimize=True)
tee.save(root / "tee.png", optimize=True)
print("wrote tote.png and tee.png (black marks)")
