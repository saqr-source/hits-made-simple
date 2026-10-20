"""De-identify real HITS screenshots: replace a personal-data area with clean dummy text
in the app's own colours (background sampled from the edge of the area, text colour sampled
from the original text). Nothing in the HITS interface itself is redrawn."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
F_AR = os.path.join(HERE, 'fonts', 'ar.ttf')
F_LAT = os.path.join(HERE, 'fonts', 'lat.ttf')
_cache = {}

def font(path, size):
    k = (path, size)
    if k not in _cache:
        f = ImageFont.truetype(path, size, layout_engine=ImageFont.Layout.RAQM)
        try: f.set_variation_by_axes([470 if path == F_LAT else 420])
        except Exception: pass
        _cache[k] = f
    return _cache[k]

def _colors(im, box):
    x0, y0, x1, y1 = box
    a = np.asarray(im.crop(box).convert('RGB')).reshape(-1, 3).astype(int)
    edge = np.concatenate([np.asarray(im.crop((x0, y0, x1, y0 + 2))).reshape(-1, 3), np.asarray(im.crop((x0, y1 - 2, x1, y1))).reshape(-1, 3),
                           np.asarray(im.crop((x0, y0, x0 + 2, y1))).reshape(-1, 3), np.asarray(im.crop((x1 - 2, y0, x1, y1))).reshape(-1, 3)]).astype(int)
    bg = tuple(int(v) for v in np.median(edge, 0))
    lum = a @ [0.299, 0.587, 0.114]; blum = 0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]
    far = a[np.argsort(np.abs(lum - blum))[-max(5, len(a) // 40):]]
    fg = tuple(int(v) for v in np.median(far, 0))
    if abs((0.299 * fg[0] + 0.587 * fg[1] + 0.114 * fg[2]) - blum) < 60:
        fg = (245, 245, 245) if blum < 128 else (38, 38, 40)
    return bg, fg

def _is_ar(s): return any('؀' <= c <= 'ۿ' for c in s)

def replace(im, box, lines, rtl=False, size=None, align=None):
    """box in pixels; lines: list of strings, or ('ID', 'name') tuples drawn as one line."""
    box = tuple(int(v) for v in box)
    bg, fg = _colors(im, box)
    d = ImageDraw.Draw(im)
    d.rectangle(box, fill=bg)
    x0, y0, x1, y1 = box
    n = len(lines); lh = (y1 - y0) / n
    sz0 = size or max(10, int(lh * 0.8))
    align = align or ('right' if rtl else 'left')
    for i, ln in enumerate(lines):
        cy = y0 + lh * (i + 0.5)
        parts = list(ln) if isinstance(ln, tuple) else [ln]
        sz = sz0
        while sz > 9:
            tot = sum(d.textlength(p, font=font(F_AR if _is_ar(p) else F_LAT, sz), direction='rtl' if _is_ar(p) else 'ltr') for p in parts) + sz * 0.35 * (len(parts) - 1)
            if tot <= (x1 - x0) - 6: break
            sz -= 1
        x = x1 - 2 if align == 'right' else x0 + 2
        for p in parts:
            f = font(F_AR if _is_ar(p) else F_LAT, sz)
            w = d.textlength(p, font=f, direction='rtl' if _is_ar(p) else 'ltr')
            if align == 'right':
                d.text((x, cy), p, font=f, fill=fg, anchor='rm', direction='rtl' if _is_ar(p) else 'ltr'); x -= w + sz * 0.35
            else:
                d.text((x, cy), p, font=f, fill=fg, anchor='lm'); x += w + sz * 0.35
    return im

def copy_patch(im, src_box, dst_xy):
    """Replace a real photo with the app's default avatar copied from another row."""
    p = im.crop(tuple(int(v) for v in src_box)); im.paste(p, tuple(int(v) for v in dst_xy)); return im

def blur(im, b):
    x0, y0, x1, y1 = [int(v) for v in b]
    r = im.crop((x0, y0, x1, y1)); w, h = r.size
    r = r.filter(ImageFilter.GaussianBlur(8)).resize((max(1, w // 10), max(1, h // 10)), Image.BILINEAR).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
    im.paste(r, (x0, y0)); return im

EN_NAMES = ['Sample Employee', 'Omar Adel Hassan', 'Sara Nabil Fouad', 'Karim Fathy Saleh', 'Mona Samir Aziz', 'Hany Lotfy Ali', 'Dina Wael Kamal', 'Tamer Reda Samy']
AR_NAMES = ['موظف تجريبي', 'عمر عادل حسن', 'سارة نبيل فؤاد', 'كريم فتحي صالح', 'منى سمير عزيز', 'هاني لطفي علي', 'دينا وائل كمال', 'تامر رضا سامي']
