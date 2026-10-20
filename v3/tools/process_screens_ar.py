"""Arabic-language HITS screens (light theme): scale to 589 px wide, mask personal data, crop to the 492:1052 slot.
Run: python3 tools/process_screens_ar.py <dir with eNN.jpg / mNN.jpg> <out_dir>"""
import sys, os
from PIL import Image, ImageFilter
SRC, OUT = sys.argv[1:3]
W0 = 589; H0 = round(W0 / (492 / 1052))   # 1259

def blur(im, b):
    x0, y0, x1, y1 = [int(v) for v in b]
    r = im.crop((x0, y0, x1, y1)); w, h = r.size
    r = r.filter(ImageFilter.GaussianBlur(8)).resize((max(1, w // 10), max(1, h // 10)), Image.BILINEAR).resize((w, h), Image.BILINEAR).filter(ImageFilter.GaussianBlur(4))
    im.paste(r, (x0, y0))

def rows(ys, x0, x1, half=14): return [(x0, y - half, x1, y + half) for y in ys]

M = {
 'ar_home_emp':   ('e01', [(185, 205, 448, 285)]),
 'ar_home_mgr':   ('m05', [(88, 236, 450, 290)]),
 'ar_my_leaves':  ('e07', [(60, 352, 150, 384), (262, 352, 318, 384), (442, 352, 508, 384), (60, 440, 100, 470), (425, 440, 470, 470),
                           (55, 558, 120, 592), (255, 558, 310, 592), (445, 558, 500, 592), (55, 620, 120, 655), (255, 620, 310, 655), (445, 620, 500, 655),
                           (95, 802, 150, 832), (355, 802, 412, 832), (95, 885, 150, 915), (355, 885, 412, 915), (40, 1098, 560, 1210), (40, 1098, 560, 1210)]),
 'ar_days':       ('e08', [(100, 383, 158, 412), (358, 383, 414, 412), (100, 466, 158, 495), (358, 466, 414, 495),
                           (40, 680, 565, 1040), (40, 680, 565, 1040), (40, 680, 565, 1040)]),
 'ar_leave_hist': ('e09', []),
 'ar_leave_form': ('e10', [(88, 590, 395, 660)]),
 'ar_leave_types':('e11', []),
 'ar_leave_menu': ('e13', []),
 'ar_balance':    ('e14', [(100, 203, 225, 297), (30, 358, 430, 468), (100, 538, 225, 627), (30, 690, 430, 798), (100, 868, 225, 962), (30, 1022, 430, 1132)]),
 'ar_my_perm':    ('e17', []),
 'ar_perm_req':   ('e19', []),
 'ar_perm_form':  ('e20', [(100, 188, 432, 302)]),
 'ar_perm_appr':  ('e22', []),
 'ar_perm_filter':('e23', []),
 'ar_attend':     ('e26', [(80, 305, 125, 645), (270, 305, 410, 648), (318, 320, 370, 355), (325, 645, 505, 752), (100, 975, 145, 1140)]),
 'ar_attend2':    ('e27', [(40, 160, 590, 505), (95, 732, 148, 898), (48, 1092, 125, 1162), (312, 1092, 392, 1162), (318, 1158, 388, 1192)]),
 'ar_attend_log': ('e28', rows([258 + 76.5 * k for k in range(13)], 316, 552)),
 'ar_geo':        ('e29', [(30, 232, 532, 292)] + rows([305 + 76.4 * k for k in range(12)], 322, 550)),
 'ar_chg_list':   ('e02', []),
 'ar_chg_form':   ('e04', []),
 'ar_chg_pick':   ('e05', []),
 'ar_chg_filled': ('e06', []),
 'ar_notif':      ('m01', [(410, 232, 482, 262), (95, 256, 242, 286), (335, 436, 482, 467), (45, 459, 202, 491), (320, 616, 482, 649), (45, 639, 112, 672),
                           (410, 797, 482, 829), (95, 820, 242, 852), (345, 1001, 482, 1034), (50, 1024, 262, 1056), (345, 1182, 482, 1214)]),
 'ar_perm_types': ('m02', [(140, 195, 440, 322)]),
 'ar_perm_send':  ('m03', [(140, 195, 440, 322)]),
 'ar_perm_mission':('m04', [(140, 195, 440, 322)]),
 'ar_tk_filter':  ('m06', []),
 'ar_la_menu':    ('m07', rows([263, 386, 510], 98, 445)),
 'ar_la_confirm': ('m08', rows([263, 386, 510], 98, 445)),
 'ar_la_hist':    ('m10', rows([263, 386, 510, 633, 757, 880, 1004, 1128], 100, 445) + [(448, 252, 552, 354)]),
 'ar_la_current': ('m11', rows([263, 386, 510], 98, 445)),
 'ar_chg_appr_filter': ('m16', []),
 'ar_chg_appr':   ('m17', []),
}
os.makedirs(OUT, exist_ok=True)
for name, (src, boxes) in M.items():
    im = Image.open(os.path.join(SRC, src[0], src + '.jpg')).convert('RGB')
    im = im.resize((W0, round(im.height * W0 / im.width)), Image.LANCZOS)
    for b in boxes: blur(im, b)
    if im.height < H0:   # popup crops: extend the canvas with the popup's own edge colour
        c = Image.new('RGB', (W0, H0), im.getpixel((W0 // 2, im.height - 2))); c.paste(im, (0, 0)); im = c
    im = im.crop((0, 0, W0, H0))
    im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=84, method=6)
print(len(M), 'arabic screens')
