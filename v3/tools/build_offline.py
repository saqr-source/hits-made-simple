"""Inline the whole site into one self-contained HTML file (works offline, no server).
Run: python3 tools/build_offline.py <out.html>"""
import base64, re, sys, os
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def b64(p, mime): return 'data:%s;base64,%s' % (mime, base64.b64encode(open(os.path.join(R, p), 'rb').read()).decode())
MIME = {'.woff2': 'font/woff2', '.webp': 'image/webp', '.png': 'image/png'}
css = open(os.path.join(R, 'assets/app.css')).read()
css = re.sub(r'url\((fonts/[^)]+|img/[^)]+)\)', lambda m: 'url(%s)' % b64('assets/' + m.group(1), MIME[os.path.splitext(m.group(1))[1]]), css)
js = open(os.path.join(R, 'assets/app.js')).read()
# map every asset path the script requests to a data URI
assets = {}
for d in ['assets/screens', 'assets/img']:
    for f in sorted(os.listdir(os.path.join(R, d))):
        assets[d + '/' + f] = b64(d + '/' + f, MIME[os.path.splitext(f)[1]])
shim = 'window.HITS_ASSETS=' + __import__('json').dumps(assets) + ';'
html = open(os.path.join(R, 'index.html')).read()
html = re.sub(r'<link rel="preload"[^>]*>\n', '', html)
html = html.replace('<link rel="apple-touch-icon" href="assets/img/icon-180.png">', '<link rel="apple-touch-icon" href="%s">' % assets['assets/img/icon-180.png'])
html = html.replace('<link rel="icon" href="assets/img/icon-180.png">', '<link rel="icon" href="%s">' % assets['assets/img/icon-180.png'])
html = re.sub(r'<link rel="stylesheet" href="assets/app.css[^"]*">', lambda m: '<style>' + css + '</style>', html)
data = open(os.path.join(R, 'assets/data.js')).read(); cfg = open(os.path.join(R, 'assets/config.js')).read()
html = re.sub(r'<script src="assets/data.js[^"]*"></script>\n<script src="assets/config.js[^"]*"></script>\n<script src="assets/app.js[^"]*"></script>',
              lambda m: '<script>' + data + '</script>\n<script>' + cfg + '</script>\n<script>' + shim + '</script>\n<script>' + js.replace('</script', '<\\/script') + '</script>', html)
assert 'assets/app.js' not in html and "src=\"assets/" not in html.replace("A('assets/", '')
open(sys.argv[1], 'w').write(html)
print(sys.argv[1], round(len(html) / 1e6, 2), 'MB')
