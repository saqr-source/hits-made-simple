"""English HITS screens: de-identify (dummy names, IDs and titles instead of blur), crop to the 492:1052 slot.
Numbers such as balances and attendance figures are left as they are (no names are attached to them).
Run: python3 tools/process_screens.py <raw_dir> <v22_processed_dir> <out_dir>"""
import sys, os
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from deidentify import replace, copy_patch, EN_NAMES as N
RAW, V22, OUT = sys.argv[1:4]
RATIO = 492 / 1052

def card(box): return ('card', box)          # name / ID / department / title card
CARD = lambda k=0: [N[k % len(N)], str(10001 + k), 'Department', 'Job Title']

def row_hdr(y, k, x0=148, x1=498, h=24): return (x0, y - 6, x1, y + h - 6), [(str(10001 + k), N[k % len(N)])]

SPECS = {
 'notifications': ('03', 0, [((432,234,534,262), ['Sample'], 'right'), ((108,258,254,286), ['Employee']), ((380,439,547,467), ['Omar'], 'right'),
                             ((108,462,372,490), ['Adel  Vacation:']), ((380,619,542,647), ['Sara'], 'right'), ((108,642,174,669), ['Nabil']),
                             ((432,800,534,828), ['Karim'], 'right'), ((108,824,254,852), ['Fathy']), ((380,1004,537,1032), ['Mona'], 'right'),
                             ((108,1027,347,1055), ['Samir']), ((380,1186,465,1213), ['Hany'], 'right')], []),
 'leave_approvals': ('13', 0, [row_hdr(y, k) for k, y in enumerate([255,379,502,626,750,873,997,1120])], [((38,377,139,476), (38,253))]),
 'perm_history_light': ('10', 0, [row_hdr(y, k) for k, y in enumerate([255,379,502,626,750,873,997,1120])], []),
 'home_light': ('16', 0, [((140,224,508,294), ['Hi, Sample Employee'])], []),
 'home_dark': ('32', 0, [((152,200,445,282), ['Hi, Sample', 'Employee'])], []),
 'geo': ('04', 0, [], []), 'geo_filter': ('01', 0, [], []), 'tk_filter': ('06', 0, [], []), 'perm_filter': ('07', 0, [], []),
 'team_list': ('15', 0, [((142,202,562,312), CARD(0))] + [((142, y - 6, 562, y + 102), CARD(k)) for k, y in enumerate([343,477,612,746,880,1014,1149], 1)], []),
 'leave_history_light': ('18', 0, [], []), 'leave_menu': ('19', 0, [], []), 'balance_periods': ('20', 0, [], []),
 'perm_history': ('24', 20, [((205,312,640,476), CARD())], []),
 'leave_history': ('25', 20, [((205,292,640,455), CARD())], []),
 'days_taken': ('27', 20, [((182,216,645,380), CARD())], []),
 'balance': ('30', 20, [], []),
 'attendance': ('23', 20, [], []),
 'perm_current': ('21', 20, [((186, y - 4, 600, y + 31), [(str(10001), N[0])]) for y in [311,561,811,1061,1311]], []),
 'perm_detail': ('22', 20, [((210,246,640,410), CARD())], []),
 'days_count': ('26', 20, [((185,216,650,380), CARD())], []),
}
FILLS = {'attendance': [((566,316,694,944), (560,600))]}   # screen-recorder overlay
os.makedirs(OUT, exist_ok=True)
for name, (n, top, reps, patches) in SPECS.items():
    im = Image.open(os.path.join(RAW, n + '.jpg')).convert('RGB')
    for b, s in FILLS.get(name, []):
        im.paste(Image.new('RGB', (b[2] - b[0], b[3] - b[1]), im.getpixel(s)), (b[0], b[1]))
    for src, dst in patches: copy_patch(im, src, dst)
    for r in reps: replace(im, r[0], r[1], align=r[2] if len(r) > 2 else None)
    W, H = im.size; h = round(W / RATIO)
    im = im.crop((0, top, W, top + h))
    im.save(os.path.join(OUT, name + '.webp'), 'WEBP', quality=86, method=6)
for f in ['login_empty', 'login_filled', 'forgot', 'settings', 'leave_list', 'leave_form', 'leave_types', 'my_permissions']:
    Image.open(os.path.join(V22, f + '.jpg')).convert('RGB').save(os.path.join(OUT, f + '.webp'), 'WEBP', quality=84, method=6)
print(len(SPECS), 'english screens')
