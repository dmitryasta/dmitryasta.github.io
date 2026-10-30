"""Generates 1200x630 Open Graph images (en, ru, sr) with Playwright. Run: python3 qa/og.py"""
import asyncio, pathlib
from playwright.async_api import async_playwright

ROOT = pathlib.Path(__file__).resolve().parent.parent
FONTS = ROOT / 'node_modules/@fontsource-variable'
TEXT = {
  'en': dict(name='Dmitry Astakhov', tag='Serbia Market Entry &amp; Trade Consulting', line='Import · Distribution · Local representation · Automation', city='Belgrade, Serbia'),
  'ru': dict(name='Дмитрий Астахов', tag='Выход на рынок Сербии и торговый консалтинг', line='Импорт · Дистрибуция · Представительство · Автоматизация', city='Белград, Сербия'),
  'sr': dict(name='Dmitry Astakhov', tag='Ulazak na tržište Srbije i trgovinski konsalting', line='Uvoz · Distribucija · Zastupanje · Automatizacija', city='Beograd, Srbija'),
}
def plates():
    out = []
    for i, cy in enumerate((470, 360, 250)):
        w, h = 230, 115
        cx = 930
        top = f'{cx},{cy-h} {cx+w},{cy} {cx},{cy+h} {cx-w},{cy}'
        l = f'{cx-w},{cy} {cx},{cy+h} {cx},{cy+h+22} {cx-w},{cy+22}'
        r = f'{cx},{cy+h} {cx+w},{cy} {cx+w},{cy+22} {cx},{cy+h+22}'
        hot = i == 2
        out.append(f'<polygon points="{l}" fill="#0d2442" stroke="rgba(127,176,255,.35)"/><polygon points="{r}" fill="#0a1c34" stroke="rgba(127,176,255,.35)"/><polygon points="{top}" fill="{"#1d4a86" if hot else "#143564"}" fill-opacity=".92" stroke="url(#e)" stroke-width="2"/>')
        if hot:
            out.append(f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="17" fill="#071426" stroke="#42c8e8" stroke-width="3"/><rect x="{cx-5}" y="{cy-5}" width="10" height="10" fill="#c9a227" transform="rotate(45 {cx} {cy})"/>')
    return ''.join(out)

def html(l):
    t = TEXT[l]
    ff = ''
    for fam, pkg, nm, wr in (('Manrope Variable', 'manrope', 'manrope', '200 800'), ('Inter Variable', 'inter', 'inter', '100 900')):
        for sub in ('cyrillic', 'latin-ext', 'latin'):
            rng = {'cyrillic': 'U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116', 'latin-ext': 'U+0100-02BA,U+02BD-02C5,U+02C7-02CC,U+02CE-02D7,U+02DD-02FF,U+1E00-1E9F,U+20A0-20AB,U+20AD-20C0', 'latin': 'U+0000-00FF,U+0131,U+0152-0153,U+2000-206F,U+20AC,U+2122'}[sub]
            ff += f"@font-face{{font-family:'{fam}';font-weight:{wr};src:url('file://{FONTS}/{pkg}/files/{nm}-{sub}-wght-normal.woff2') format('woff2-variations');unicode-range:{rng}}}"
    return f'''<!doctype html><html><head><meta charset="utf-8"><style>{ff}
*{{box-sizing:border-box;margin:0}}body{{width:1200px;height:630px;overflow:hidden;background:#071426;color:#f4f7fb;font-family:'Inter Variable',sans-serif;position:relative}}
.bg{{position:absolute;inset:0;background:radial-gradient(700px 520px at 80% 45%,rgba(77,141,255,.35),transparent 70%),radial-gradient(600px 400px at 0% 100%,rgba(66,200,232,.14),transparent 70%),linear-gradient(180deg,#0b1f3a,#071426)}}
.grid{{position:absolute;inset:0;background-image:linear-gradient(rgba(170,183,201,.07) 1px,transparent 1px),linear-gradient(90deg,rgba(170,183,201,.07) 1px,transparent 1px);background-size:60px 60px;-webkit-mask-image:radial-gradient(ellipse 80% 80% at 70% 50%,#000,transparent 75%)}}
.copy{{position:absolute;left:72px;top:0;bottom:0;width:640px;display:flex;flex-direction:column;justify-content:center;gap:22px}}
.mark{{display:flex;align-items:center;gap:14px;font-family:'Manrope Variable';font-weight:800;font-size:22px;color:#aab7c9;letter-spacing:.02em}}
.mark i{{width:44px;height:44px;border-radius:12px;border:2px solid #42c8e8;display:grid;place-items:center;font-style:normal;color:#f4f7fb;font-size:19px;background:#0b1f3a}}
h1{{font-family:'Manrope Variable';font-weight:800;font-size:68px;line-height:1.04;letter-spacing:-.035em}}
h2{{font-family:'Manrope Variable';font-weight:700;font-size:34px;line-height:1.2;letter-spacing:-.02em;background:linear-gradient(100deg,#7fb0ff,#42c8e8);-webkit-background-clip:text;color:transparent;max-width:600px}}
p{{font-size:24px;color:#aab7c9;line-height:1.4;max-width:600px}}
.city{{position:absolute;left:72px;bottom:44px;font-family:'Manrope Variable';font-weight:700;letter-spacing:.06em;font-size:17px;color:#42c8e8}}
svg{{position:absolute;right:0;top:0}}</style></head><body><div class="bg"></div><div class="grid"></div>
<svg width="1200" height="630" viewBox="0 0 1200 630"><defs><linearGradient id="e" x1="0" x2="1"><stop offset="0" stop-color="#4d8dff"/><stop offset="1" stop-color="#42c8e8"/></linearGradient></defs>{plates()}</svg>
<div class="copy"><div class="mark"><i>DA</i></div><h1>{t['name']}</h1><h2>{t['tag']}</h2><p>{t['line']}</p></div><div class="city">{t['city']}</div></body></html>'''

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--allow-file-access-from-files'])
        pg = await b.new_page(viewport={'width': 1200, 'height': 630})
        for l in TEXT:
            f = ROOT / f'qa/og-{l}.html'
            f.write_text(html(l), encoding='utf-8')
            await pg.goto(f'file://{f}')
            await pg.evaluate('document.fonts.ready')
            await pg.wait_for_timeout(400)
            await pg.screenshot(path=str(ROOT / f'public/og/og-{l}.png'))
            f.unlink()
        await b.close()
asyncio.run(main())
