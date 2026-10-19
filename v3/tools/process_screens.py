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
 'notifications': ('03', 0, [(438,234,534,262),(108,258,254,286),(396,439,547,467),(108,462,307,490),
                             (396,619,542,647),(108,642,174,669),(438,800,534,828),(108,824,254,852),
                             (396,1004,537,1032),(108,1027,347,1055),(396,1186,465,1213)], []),
 'perm_approvals': ('09', 0, rows([263,387,510,634,757,880,1004],148,495)+[(148,1114,398,1142),
                             (38,501,139,600),(38,625,139,724)], []),
 'leave_approvals': ('13', 0, rows([263,387,510,634,757,880,1004],148,498)+[(148,1114,472,1142),
                             (38,253,139,352)], []),
 'home_light': ('16', 0, [(172,224,508,294)], []),
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
