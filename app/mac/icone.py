"""Ícone psicodélico do Repertório: espiral hipnótica de arco-íris com um olho no centro.
O olho é o "olhar" do mapa; a íris usa as cores das 4 operações (laranja, azul, amarelo, roxo)."""
import sys
import numpy as np
from PIL import Image, ImageFilter

S = 2048  # desenha em 2x e reduz para suavizar as bordas
out = sys.argv[1]
y, x = np.mgrid[0:S, 0:S].astype(np.float32)
cx = cy = S / 2
dx, dy = x - cx, y - cy
r = np.hypot(dx, dy) + 1e-3
t = np.arctan2(dy, dx)


def hsv(h, s, v):
    h = (h % 1.0) * 6
    i = np.floor(h).astype(int) % 6
    f = h - np.floor(h)
    p, q, u = v * (1 - s), v * (1 - s * f), v * (1 - s * (1 - f))
    rgb = np.zeros(h.shape + (3,), np.float32)
    for k, (a, b, c) in enumerate([(v, u, p), (q, v, p), (p, v, u), (p, q, v), (u, p, v), (v, p, q)]):
        m = i == k
        rgb[m, 0], rgb[m, 1], rgb[m, 2] = a[m], b[m], c[m]
    return rgb


# fundo: espiral logarítmica de arco-íris com faixas que giram ao contrário
R = S * 0.40
spiral = t / (2 * np.pi) * 2 + 2.6 * np.log(r / R)
bands = 0.5 + 0.5 * np.sin(34 * np.log(r / R) - 6 * t)
stripes = np.sin(22 * np.log(r / R) + 5 * t)
hue = spiral + 0.08 * bands
val = 0.30 + 0.70 * np.clip((stripes + 0.25) / 0.5, 0, 1)
bg = hsv(hue, np.full_like(r, 0.95), val)

# olho em forma de amêndoa
w, h = S * 0.33, S * 0.19
def lens(ww, hh):
    return np.abs(dy) < hh * np.clip(1 - (dx / ww) ** 2, 0, None)
eye = lens(w, h)
outline = lens(w + S * 0.045, h + S * 0.05) & ~eye
glow = lens(w + S * 0.11, h + S * 0.12) & ~lens(w + S * 0.045, h + S * 0.05)

img = bg.copy()
img[glow] = hsv(hue[glow] + 0.5, np.full(glow.sum(), 0.55, np.float32), np.ones(glow.sum(), np.float32))
img[outline] = [0.04, 0.03, 0.06]
img[eye] = [1.0, 0.97, 0.90]

# íris: setores das 4 cores das operações, torcidos em redemoinho
ir = S * 0.165
cols = np.array([[255, 90, 60], [62, 123, 255], [245, 180, 0], [180, 85, 255]], np.float32) / 255
twist = (t / (2 * np.pi) * 8 + r / (S * 0.035)) % 4
iris = (r < ir) & eye
idx = np.floor(twist).astype(int) % 4
img[iris] = cols[idx[iris]]
ring = (r < ir) & (r > ir * 0.93) & eye
img[ring] = [0.04, 0.03, 0.06]
pupil = r < S * 0.068
img[pupil] = [0.02, 0.02, 0.03]
hl = np.hypot(dx + S * 0.03, dy + S * 0.032) < S * 0.022
img[hl] = [1, 1, 1]

# recorte no formato de ícone do macOS (superelipse) com sombra
box = S * 0.805 / 2
squircle = (np.abs(dx) / box) ** 5 + (np.abs(dy - S * 0.004) / box) ** 5 <= 1
rgba = np.zeros((S, S, 4), np.uint8)
rgba[..., :3] = (np.clip(img, 0, 1) * 255).astype(np.uint8)
rgba[..., 3] = squircle * 255
icon = Image.fromarray(rgba, 'RGBA')

shadow_mask = Image.fromarray(((np.abs(dx) / box) ** 5 + (np.abs(dy - S * 0.018) / box) ** 5 <= 1).astype(np.uint8) * 110, 'L')
shadow_mask = shadow_mask.filter(ImageFilter.GaussianBlur(S * 0.012))
canvas = Image.new('RGBA', (S, S), (0, 0, 0, 0))
canvas.paste(Image.new('RGBA', (S, S), (0, 0, 0, 255)), (0, 0), shadow_mask)
canvas.alpha_composite(icon)
canvas.resize((1024, 1024), Image.LANCZOS).save(out)
