"""Crop real HITS screenshots to the 492:1052 phone slot and mask personal data.
Masking = heavy blur + pixelation of the region (UI itself is never redrawn).
Run: python3 tools/process_screens.py <raw_dir> <v22_processed_dir> <out_dir>"""
import sys, os
from PIL import Image, ImageFilter
RAW, V22, OUT = sys.argv[1:4]
RATIO = 492/1052

def blur(im, box):
    x0,y0,x1,y1 = box
    reg = im.crop(box)
    w,h = reg.size
    reg = reg.filter(ImageFilter.GaussianBlur(8))
    reg = reg.resize((max(1,w//10),max(1,h//10)), Image.BILINEAR).resize((w,h), Image.BILINEAR)
    reg = reg.filter(ImageFilter.GaussianBlur(4))
    im.paste(reg, (x0,y0))

def fill(im, box, sample):
    c = im.getpixel(sample)
    im.paste(Image.new('RGB',(box[2]-box[0],box[3]-box[1]),c),(box[0],box[1]))

def crop_ratio(im, top):
    W,H = im.size
    h = round(W/RATIO)
    return im.crop((0,top,W,top+h))

def rows(ys, x0, x1, half=14):
    return [(x0,y-half,x1,y+half) for y in ys]

NEW = {
 # name: (raw file, top crop, blur boxes, fill boxes)
 'notifications': ('03', 0, [(380,234,534,262),(108,258,254,286),(380,439,547,467),(108,462,307,490),
                             (380,619,542,647),(108,642,174,669),(380,800,534,828),(108,824,254,852),
                             (380,1004,537,1032),(108,1027,347,1055),(380,1186,465,1213)], []),
 # 'perm_approvals' (not shipped)
 'leave_approvals': ('13', 0, rows([263,387,510,634,757,880,1004],148,498)+[(148,1114,472,1142),
                             (38,253,139,352)], []),
 'home_light': ('16', 0, [(140,224,508,294)], []),
 'geo': ('04', 0, [], []),
 'tk_filter': ('06', 0, [], []),
 'perm_filter': ('07', 0, [], []),
 'perm_history': ('24', 20, [(210,310,652,480)], []),
 'leave_history': ('25', 20, [(210,290,652,460)], []),
 'days_taken': ('27', 20, [(190,213,652,384)] + rows([703,820,937,1054,1171,1288],230,312,19)
                          + rows([703,820,937,1054,1171,1288],543,614,19), []),
 'balance': ('30', 20, [(83,463,187,504),(308,463,412,504),(538,463,642,504),(68,588,122,617),(528,588,567,617),
                        (113,750,182,784),(343,750,407,784),(568,750,652,784),
                        (113,842,182,876),(343,842,407,876),(568,842,642,876)], []),
 'attendance': ('23', 20, [], [((566,316,694,944),(560,600))]),
 'geo_filter': ('01', 0, [], []),
 'perm_filter': ('07', 0, [], []),
 'team_list': ('15', 0, rows([216,243,271,299],142,562,14)+rows([351,379,407,434,485,513,541,568,619,647,675,703,754,782,809,837,888,916,943,971,1022,1050,1078,1105,1156,1184,1210],142,562,14)+[(440,1160,552,1196)], []),
 'perm_history_light': ('10', 0, rows([263,386,510,634,757,880,1004],148,495)+[(148,1114,470,1142)], []),
 'leave_history_light': ('18', 0, [], []),
 'leave_menu': ('19', 0, [], []),
 'balance_periods': ('20', 0, [(368,219,508,306),(142,343,563,450),(368,518,508,605),(142,642,563,749),(368,822,508,908),(142,940,563,1047)], []),
 'perm_current': ('21', 20, rows([322,573,823,1073,1324],202,594,19), []),
 'perm_detail': ('22', 20, [(217,243,642,412)], []),
 'days_count': ('26', 20, [(190,213,652,384),(128,1138,167,1172),(220,1138,260,1172),(313,1188,352,1222),(403,908,452,944),(503,1198,537,1232),(595,1198,634,1232),(102,838,664,1248),(102,838,664,1248),(102,838,664,1248),(102,838,664,1248),(40,838,102,1248)], []),
}
os.makedirs(OUT, exist_ok=True)
for name,(n,top,blurs,fills) in NEW.items():
    im = Image.open(os.path.join(RAW, n+'.jpg')).convert('RGB')
    for b,s in fills: fill(im,b,s)
    for b in blurs: blur(im,b)
    im = crop_ratio(im, top)
    im.save(os.path.join(OUT, name+'.webp'), 'WEBP', quality=84, method=6)
    print(name, im.size)
for f in ['login_empty','login_filled','home','forgot','settings','leave_list','leave_form','leave_types','my_permissions']:
    im = Image.open(os.path.join(V22, f+'.jpg')).convert('RGB')
    nm = 'home_dark' if f=='home' else f
    im.save(os.path.join(OUT, nm+'.webp'), 'WEBP', quality=84, method=6); print(nm, im.size)
