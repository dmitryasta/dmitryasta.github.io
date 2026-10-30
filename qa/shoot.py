"""Screenshots and layout checks with Playwright (Chromium). Usage: python3 qa/shoot.py <base_url> <outdir> [pages...]"""
import sys, json, asyncio
from playwright.async_api import async_playwright

base = sys.argv[1].rstrip('/')
out = sys.argv[2]
pages = sys.argv[3:] or ['/']
VIEWS = [('desktop', 1440, 900), ('mobile', 390, 844)]

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        report = []
        for name, w, h in VIEWS:
            ctx = await b.new_context(viewport={'width': w, 'height': h}, device_scale_factor=1)
            pg = await ctx.new_page()
            errors = []
            pg.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
            pg.on('pageerror', lambda e: errors.append(str(e)))
            for path in pages:
                await pg.goto(base + path, wait_until='networkidle')
                await pg.evaluate("document.querySelectorAll('.reveal').forEach(e=>e.classList.add('is-in'))")
                await pg.wait_for_timeout(500)
                info = await pg.evaluate("""() => ({
                  sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth,
                  h1: document.querySelectorAll('h1').length,
                  wide: [...document.querySelectorAll('body *')].filter(e => { const r = e.getBoundingClientRect(); return r.width > 0 && (r.right > document.documentElement.clientWidth + 1) && getComputedStyle(e).position !== 'fixed' }).slice(0,6).map(e => e.tagName + '.' + (e.className && e.className.baseVal === undefined ? e.className : ''))
                })""")
                slug = (path.strip('/') or 'home').replace('/', '_')
                await pg.screenshot(path=f'{out}/{slug}-{name}.png', full_page=True)
                report.append({'view': name, 'path': path, **info, 'errors': list(errors)})
                errors.clear()
            await ctx.close()
        await b.close()
        print(json.dumps(report, indent=1))
asyncio.run(main())
