"""Arabic-language HITS screens: scale to 589 px wide, de-identify with dummy Arabic data, crop to the 492:1052 slot.
Run: python3 tools/process_screens_ar.py <dir with e/eNN.jpg and m/mNN.jpg> <out_dir>"""
import sys, os
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deidentify import replace, copy_patch, AR_NAMES as N
SRC, OUT = sys.argv[1:3]
W0 = 589; H0 = round(W0 / (492 / 1052))
CARD = [N[0], '10001', 'الإدارة', 'المسمى الوظيفي']
def rows(ys, x0=98, x1=445): return [((x0, y - 14, x1, y + 14), [(str(10001 + k), N[k % len(N)])], 'right') for k, y in enumerate(ys)]
NOTIF = [((410,232,482,262), ['Sample'], 'right'), ((95,256,242,286), ['Employee']), ((335,436,482,467), ['Omar Adel'], 'right'),
         ((45,459,202,491), ['Hassan Ahmed']), ((320,616,482,649), ['Sara Nabil'], 'right'), ((45,639,112,672), ['Fouad']),
         ((410,797,482,829), ['Sample'], 'right'), ((95,820,242,852), ['Employee']), ((345,1001,482,1034), ['Mona'], 'right'),
         ((50,1024,262,1056), ['Samir Aziz Kamal']), ((345,1182,482,1214), ['Karim'], 'right')]
M = {
 'ar_home_emp':   ('e01', [((185,205,448,285), ['مرحبا،', 'موظف تجريبي'], 'right')], []),
 'ar_home_mgr':   ('m05', [((88,236,450,290), ['مرحبا، موظف تجريبي'], 'right')], []),
 'ar_my_leaves':  ('e07', [], []), 'ar_days': ('e08', [], []), 'ar_leave_hist': ('e09', [], []),
 'ar_leave_form': ('e10', [((88,590,395,660), ['شارع تجريبي، المعادي', 'القاهرة'], 'right')], []),
 'ar_leave_types':('e11', [], []), 'ar_leave_menu': ('e13', [], []), 'ar_balance': ('e14', [], []),
 'ar_my_perm':    ('e17', [], []), 'ar_perm_req': ('e19', [], []),
 'ar_perm_form':  ('e20', [((100,188,432,302), CARD, 'right')], []),
 'ar_perm_appr':  ('e22', [], []), 'ar_perm_filter':('e23', [], []),
 'ar_attend':     ('e26', [], []), 'ar_attend2': ('e27', [], []), 'ar_attend_log': ('e28', [], []),
 'ar_geo':        ('e29', [((30,232,532,292), ['Sample Street, Area 1, Cairo, Egypt'])], []),
 'ar_settings':   ('e30', [], []),
 'ar_chg_list':   ('e02', [], []), 'ar_chg_form': ('e04', [], []), 'ar_chg_pick': ('e05', [], []), 'ar_chg_filled': ('e06', [], []),
 'ar_notif':      ('m01', NOTIF, []),
 'ar_perm_types': ('m02', [((140,200,436,318), CARD, 'right')], []),
 'ar_perm_send':  ('m03', [((140,200,436,318), CARD, 'right')], []),
 'ar_perm_mission':('m04', [((140,200,436,318), CARD, 'right')], []),
 'ar_tk_filter':  ('m06', [], []),
 'ar_la_menu':    ('m07', rows([263, 386, 510]), []),
 'ar_la_confirm': ('m08', rows([263, 386, 510]), []),
 'ar_la_hist':    ('m10', rows([263, 386, 510, 633, 757, 880, 1004, 1128], 100), [((448,377,552,479), (448,252))]),
 'ar_la_current': ('m11', rows([263, 386, 510]), []),
 'ar_chg_appr_filter': ('m16', [], []), 'ar_chg_appr': ('m17', [], []),
}
os.makedirs(OUT, exist_ok=True)
for name, (src, reps, patches) in M.items():
    im = Image.open(os.path.join(SRC, src[0], src + '.jpg')).convert('RGB')
    im = im.resize((W0, round(im.height * W0 / im.width)), Image.LANCZOS)
    for s_, d_ in patches: copy_patch(im, s_, d_)
    for r in reps: replace(im, r[0], r[1], rtl=True, align=r[2] if len(r) > 2 else None)
    if im.height < H0:
        c = Image.new('RGB', (W0, H0), im.getpixel((W0 // 2, im.height - 2))); c.paste(im, (0, 0)); im = c
    im.crop((0, 0, W0, H0)).save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=86, method=6)
print(len(M), 'arabic screens')
