"""HITS Made Simple v4 screens — one pipeline for all four screenshot sets.
Sources: <src>/<set>/<set>_NN.jpg (en_emp, en_mgr, ar_emp, ar_mgr) + the clean English login from the
'How to Register' guide. Steps: de-identify (dummy names / IDs / titles / addresses, boxes in RAW pixels),
scale to 589 px wide, fit to the 492:1052 phone slot (crop or pad with the screen's own edge colour).
Run: python3 tools/process_v4.py <src_dir> <register_guide_png> <out_dir>"""
import sys, os
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deidentify import replace, copy_patch, EN_NAMES as EN, AR_NAMES as AR
SRC, REG, OUT = sys.argv[1:4]
W0 = 589; H0 = round(W0 / (492 / 1052))
s720 = 720 / 589          # old manager dark boxes were measured on 720-wide originals
CARD_EN = lambda k=0: [EN[k % len(EN)], str(10001 + k), 'Department', 'Job Title']
CARD_AR = [AR[0], '10001', 'الإدارة', 'المسمى الوظيفي']
def rows_en(ys, x0=148, x1=498): return [((x0, y - 6, x1, y + 18), [(str(10001 + k), EN[k % len(EN)])]) for k, y in enumerate(ys)]
def rows_ar(ys, x0=98, x1=445): return [((x0, y - 14, x1, y + 14), [(str(10001 + k), AR[k % len(AR)])], 'right') for k, y in enumerate(ys)]
TEAM = [((142, 202, 562, 312), CARD_EN(0))] + [((142, y - 6, 562, y + 102), CARD_EN(k)) for k, y in enumerate([343, 477, 612, 746, 880, 1014, 1149], 1)]
ADDR_EN = [((252, 758, 622, 816), ['Sample Street, Maadi', 'Cairo'])]
NOTIF_EN_OLD = [((432,234,534,262), ['Sample'], 'right'), ((108,258,254,286), ['Employee']), ((380,439,547,467), ['Omar'], 'right'),
            ((108,462,372,490), ['Adel  Vacation:']), ((380,619,542,647), ['Sara'], 'right'), ((108,642,174,669), ['Nabil']),
            ((432,800,534,828), ['Karim'], 'right'), ((108,824,254,852), ['Fathy']), ((380,1004,537,1032), ['Mona'], 'right'),
            ((108,1027,347,1055), ['Samir']), ((380,1186,465,1213), ['Hany'], 'right')]
def NB(y0, y1, lines, x0, x1, al=None): return ((x0, y0, x1, y1), lines) + ((al,) if al else ())
TP = lambda d, nm, fn: ['Time Permission request for employee 10001', f'{nm} Time Permission: Personal', f'Permission Short [Late In] at {d} Oct 2026 From', '10:00:00 To 12:00:00 Permission Hours 02:00', 'waiting your approval']
VC = lambda a, b, c, d: [f'Vacation request for employee {a}', f'{b} Vacation: {c} From Date {d}', f'Oct 2026 To Date {d} Oct 2026 (1 Days)', 'waiting your approval']
def NOTIF(x0, x1, al, last):
    return [NB(238, 352, TP('19', 'Sample Employee', 0), x0, x1, al), NB(442, 533, VC('Omar Adel', 'Hassan', 'Annual Leave', '13'), x0, x1, al),
            NB(623, 714, VC('Sara Nabil', 'Fouad', 'Work From Home', '18'), x0, x1, al), NB(803, 917, TP('15', 'Karim Fathy Saleh', 0), x0, x1, al),
            NB(1008, 1099, VC('Mona Samir', 'Aziz', 'Work From Home', '11'), x0, x1, al), NB(1187, 1209, ['Vacation request for employee Hany Lotfy'], *last, al)]
NOTIF_EN = NOTIF(108, 553, None, (108, 452))
NOTIF_AR = NOTIF(36, 480, 'right', (135, 480))
NOTIF_AR_OLD = [((410,232,482,262), ['Sample'], 'right'), ((95,256,242,286), ['Employee']), ((335,436,482,467), ['Omar Adel'], 'right'),
            ((45,459,202,491), ['Hassan Ahmed']), ((320,616,482,649), ['Sara Nabil'], 'right'), ((45,639,112,672), ['Fouad']),
            ((410,797,482,829), ['Sample'], 'right'), ((95,820,242,852), ['Employee']), ((345,1001,482,1034), ['Mona'], 'right'),
            ((50,1024,262,1056), ['Samir Aziz Kamal']), ((345,1182,482,1214), ['Karim'], 'right')]
def sc(b, f): return tuple(round(v * f) for v in b)
# AR employee boxes were measured on 589-wide scaled images -> convert to raw 740
k740 = 740 / 589
CARD_AR_BOX_EMP = sc((100, 188, 432, 302), k740)
SPEC = {
 # ---------- English · employee (light) ----------
 'en_emp_01': [], 'en_emp_02': [((190, 270, 480, 348), ['Hi, Sample', 'Employee'])],
 **{f'en_emp_{n:02d}': [] for n in [3,4,5,6,7,8,9,10,11,12,13,14,24,25,26,27,28,29,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53]},
 **{f'en_emp_{n:02d}': ADDR_EN for n in range(15, 23)},
 'en_emp_23': [((340, 352, 640, 418), ['Sample Manager', 'Department'])],
 **{f'en_emp_{n:02d}': [((200, 240, 665, 376), CARD_EN())] for n in [30, 31, 32, 33]},
 'en_emp_51': [((45, 298, 660, 362), ['Sample Street, Area 1,', 'Cairo, Egypt'])],
 # ---------- English · manager ----------
 'en_mgr_01': NOTIF_EN, 'en_mgr_02': [], 'en_mgr_05': [], 'en_mgr_06': [], 'en_mgr_08': [],
 'en_mgr_09': rows_en([255, 379, 502, 626, 750, 873, 997, 1120]),
 'en_mgr_13': rows_en([255, 379, 502, 626, 750, 873, 997, 1120]),
 'en_mgr_14': TEAM, 'en_mgr_16': TEAM,
 'en_mgr_17': [((140, 224, 508, 294), ['Hi, Sample Employee'])],
 'en_mgr_18': [], 'en_mgr_19': [], 'en_mgr_20': [],
 'en_mgr_21': [((152, 200, 445, 282), ['Hi, Sample', 'Employee'])],
 'en_mgr_22': [((210, 246, 640, 410), CARD_EN())],
 'en_mgr_23': [((186, y - 4, 600, y + 31), [(str(10001), EN[0])]) for y in [311, 561, 811, 1061, 1311]],
 # ---------- Arabic · employee (boxes converted from the 589 measurements) ----------
 'ar_emp_01': [(sc((185, 205, 448, 285), k740), ['مرحبا،', 'موظف تجريبي'], 'right')],
 **{f'ar_emp_{n:02d}': [] for n in [2,3,4,5,6,7,8,9,11,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,30,31,32,33]},
 'ar_emp_10': [(sc((88, 590, 395, 660), k740), ['شارع تجريبي، المعادي', 'القاهرة'], 'right')],
 'ar_emp_12': [(sc((88, 590, 395, 660), k740), ['شارع تجريبي، المعادي', 'القاهرة'], 'right')],
 'ar_emp_20': [(CARD_AR_BOX_EMP, CARD_AR, 'right')],
 'ar_emp_29': [(sc((30, 236, 532, 288), k740), ['شارع تجريبي، المنطقة ١، القاهرة'], 'right', 24)],
 # ---------- Arabic · manager ----------
 'ar_mgr_01': NOTIF_AR,
 **{f'ar_mgr_{n:02d}': [((140, 200, 436, 318), CARD_AR, 'right')] for n in [2, 3, 4]},
 'ar_mgr_05': [], 'ar_mgr_06': [((88, 236, 450, 290), ['مرحبا، موظف تجريبي'], 'right')],
 'ar_mgr_07': rows_ar([263, 386, 510]), 'ar_mgr_08': rows_ar([263, 386, 510]),
 'ar_mgr_09': rows_ar([263, 386, 510, 633, 757, 880, 1004, 1128], 100),
 'ar_mgr_10': rows_ar([263, 386, 1004, 1128], 100), 'ar_mgr_11': rows_ar([263, 386, 510]),
 **{f'ar_mgr_{n:02d}': [] for n in [12, 13, 14, 15, 16, 17, 20, 21, 22, 23, 24]},
}
PATCH = {'en_mgr_13': [((38, 377, 139, 476), (38, 253))], 'ar_mgr_09': [((448, 377, 552, 479), (448, 252))], 'ar_mgr_10': [((448, 377, 552, 479), (448, 252))]}

def fit(im):
    im = im.resize((W0, round(im.height * W0 / im.width)), Image.LANCZOS)
    if im.height < H0:
        c = Image.new('RGB', (W0, H0), im.getpixel((W0 // 2, im.height - 3))); c.paste(im, (0, 0)); im = c
    return im.crop((0, 0, W0, H0))

os.makedirs(OUT, exist_ok=True)
for name, reps in SPEC.items():
    st = name[:6]
    im = Image.open(os.path.join(SRC, st, name + '.jpg')).convert('RGB')
    rtl = st.startswith('ar')
    for s_, d_ in PATCH.get(name, []): copy_patch(im, s_, d_)
    for r in reps: replace(im, r[0], r[1], rtl=rtl, align=r[2] if len(r) > 2 else None, size=r[3] if len(r) > 3 else None)
    fit(im).save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=86, method=6)

# clean English login (light): remove the guide's red frame, box and "1" marker
from PIL import ImageFilter
reg = Image.open(REG).convert('RGB')
a = np.asarray(reg).astype(int)
red = ((a[:, :, 0] - a[:, :, 1]) > 35) & ((a[:, :, 0] - a[:, :, 2]) > 35)
m = Image.fromarray((red * 255).astype('uint8')).filter(ImageFilter.MaxFilter(7))
red = np.asarray(m) > 0
b = a.copy()
ys, xs = np.where(red)
for y, x in zip(ys, xs):
    win = a[max(0, y - 14):y + 15, max(0, x - 14):x + 15].reshape(-1, 3)
    ok = win[(np.abs(win[:, 0] - win[:, 1]) < 25) & (win.sum(1) > 600)]
    b[y, x] = np.median(ok, 0) if len(ok) else (232, 242, 250)
reg = Image.fromarray(b.astype('uint8')).crop((8, 8, reg.width - 8, reg.height - 8))
reg = reg.resize((W0, round(reg.height * W0 / reg.width)), Image.LANCZOS)
pad = round(H0 * 0.06)
c = Image.new('RGB', (W0, H0), reg.getpixel((W0 // 2, 4))); c.paste(reg, (0, pad))
c.save(os.path.join(OUT, 'en_login.webp'), 'WEBP', quality=90, method=6)
print(len(SPEC) + 1, 'screens')
