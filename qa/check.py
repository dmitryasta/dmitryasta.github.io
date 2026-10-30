"""Static checks over the built site (dist). Usage: python3 qa/check.py dist <site_url_with_base>
Checks: unique title/description, one h1, heading order, canonical, hreflang reciprocity, JSON-LD validity, internal links,
sitemap coverage, robots, content present without JS (text length), language attribute, images with alt."""
import sys, re, json, pathlib, collections
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

dist = pathlib.Path(sys.argv[1]); base_url = sys.argv[2].rstrip('/') + '/'
base_path = urlparse(base_url).path

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.title=''; s.in_title=False; s.meta={}; s.links=[]; s.h=[]; s.cur=None; s.ld=[]; s.in_ld=False; s.a=[]; s.imgs=[]; s.lang=None; s.text=[]; s.skip=0; s.alts=[]
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='html': s.lang=a.get('lang')
        if t=='title': s.in_title=True
        if t=='meta': s.meta[a.get('name') or a.get('property')]=a.get('content')
        if t=='link': s.links.append(a)
        if t in ('h1','h2','h3','h4'): s.cur=[t,'']
        if t=='script':
            s.skip+=1
            if a.get('type')=='application/ld+json': s.in_ld=True; s.ld.append('')
        if t=='style': s.skip+=1
        if t=='a' and a.get('href'): s.a.append(a['href'])
        if t=='img': s.imgs.append(a)
    def handle_endtag(s,t):
        if t=='title': s.in_title=False
        if t in ('h1','h2','h3','h4') and s.cur: s.h.append(tuple(s.cur)); s.cur=None
        if t=='script': s.skip-=1; s.in_ld=False
        if t=='style': s.skip-=1
    def handle_data(s,d):
        if s.in_title: s.title+=d
        if s.in_ld: s.ld[-1]+=d
        if s.cur: s.cur[1]+=d
        if not s.skip: s.text.append(d)

pages={}
for f in sorted(dist.rglob('index.html')):
    rel='/'+str(f.parent.relative_to(dist)).replace('\\','/')+'/'
    rel=rel.replace('/./','/') if rel!='/./' else '/'
    if rel=='/./': rel='/'
    p=P(); p.feed(f.read_text(encoding='utf-8')); pages[rel]=p
f404=dist/'404.html'
problems=[]
def bad(m): problems.append(m)

urlmap={}  # absolute url -> path
for path in pages:
    urlmap[base_url.rstrip('/')+ (path if base_path=='/' else path)]=path
# path in dist is root-relative; real URL = base_url + path without leading slash
def abs_of(path): return urljoin(base_url, path.lstrip('/'))
absset={abs_of(p):p for p in pages}

titles=collections.defaultdict(list); descs=collections.defaultdict(list)
for path,p in pages.items():
    t=p.title.strip(); d=(p.meta.get('description') or '').strip()
    titles[t].append(path); descs[d].append(path)
    h1=[x for x in p.h if x[0]=='h1']
    if len(h1)!=1: bad(f'{path}: {len(h1)} h1')
    # heading order: no jump of more than one level
    prev=1
    for lvl,_ in p.h:
        n=int(lvl[1]); 
        if n>prev+1: bad(f'{path}: heading jump h{prev}->h{n}')
        prev=n
    canon=[l for l in p.links if l.get('rel')=='canonical']
    if len(canon)!=1 or canon[0]['href']!=abs_of(path): bad(f'{path}: canonical {canon and canon[0]["href"]} != {abs_of(path)}')
    if not 25<=len(t)<=75: bad(f'{path}: title length {len(t)}: {t}')
    if not 70<=len(d)<=175: bad(f'{path}: description length {len(d)}')
    words=len(' '.join(p.text).split())
    if words<120: bad(f'{path}: only {words} words in static HTML')
    for lk in p.ld:
        try: json.loads(lk)
        except Exception as e: bad(f'{path}: invalid JSON-LD {e}')
    for im in p.imgs:
        if 'alt' not in im: bad(f'{path}: img without alt')
    # hreflang
    alts={l['hreflang']:l['href'] for l in p.links if l.get('rel')=='alternate' and l.get('hreflang')}
    for need in ('en','ru','sr-Latn','x-default'):
        if need not in alts: bad(f'{path}: missing hreflang {need}')
    if alts.get('x-default')!=alts.get('en'): bad(f'{path}: x-default != en')
    if abs_of(path) not in alts.values(): bad(f'{path}: self not in hreflang set')
    for lang,href in alts.items():
        tp=absset.get(href)
        if tp is None: bad(f'{path}: hreflang {lang} target missing {href}'); continue
        back={l['hreflang']:l['href'] for l in pages[tp].links if l.get('rel')=='alternate' and l.get('hreflang')}
        if back.get(lang if lang!='x-default' else 'x-default')!=href and lang!='x-default': bad(f'{path}: hreflang not reciprocal for {lang}')
    exp={'en':'en','ru':'ru','sr':'sr-Latn'}[ 'ru' if path.startswith('/ru/') else 'sr' if path.startswith('/sr/') else 'en']
    if p.lang!=exp: bad(f'{path}: html lang {p.lang} != {exp}')
    # internal links
    for h in p.a:
        if h.startswith(('mailto:','tel:','#','http://','https://')) and not h.startswith(base_url.rstrip('/')):
            continue
        u=urljoin(abs_of(path),h.split('#')[0]) if not h.startswith('http') else h.split('#')[0]
        if u==abs_of(path) or not u: continue
        tgt=urlparse(u).path
        local=tgt[len(base_path)-1:] if base_path!='/' and tgt.startswith(base_path) else tgt
        fp=dist/local.lstrip('/')
        if not (fp.exists() or (fp/'index.html').exists()): bad(f'{path}: broken internal link {h} -> {local}')
for t,ps in titles.items():
    if len(ps)>1: bad(f'duplicate title {t!r}: {ps}')
for d,ps in descs.items():
    if len(ps)>1: bad(f'duplicate description: {ps}')
# sitemap
sm=(dist/'sitemap.xml').read_text(encoding='utf-8')
locs=set(re.findall(r'<loc>([^<]+)</loc>',sm))
if locs!=set(absset): bad(f'sitemap mismatch: missing {sorted(set(absset)-locs)[:3]} extra {sorted(locs-set(absset))[:3]}')
robots=(dist/'robots.txt').read_text(encoding='utf-8')
if 'OAI-SearchBot' not in robots or 'Disallow' in robots: bad('robots.txt unexpected')
print(f'pages: {len(pages)}; unique titles: {len(titles)}; unique descriptions: {len(descs)}; sitemap urls: {len(locs)}')
print('PROBLEMS: none' if not problems else 'PROBLEMS:\n'+'\n'.join(problems[:80]))
if problems: print(f'total {len(problems)}')
