#!/usr/bin/env python3
"""Build SEO_KEYWORD_RESEARCH (csv, xlsx) and KEYWORD_TO_PAGE_MAP.csv from qa/keywords_data.py
and a built site (dist directory).

usage: python3 qa/seo_tables.py <dist_dir> <out_dir> [default_site_url_with_base]

The implementation status is computed from the built HTML, not asserted: a query counts as covered on its
page when its content words (stemmed by prefix) all occur on that page. "Strong" means they all occur in
title, H1, H2/H3 or FAQ questions. This is a co-occurrence proxy, not an exact-phrase match.
"""
import csv, json, re, sys, os, collections
from pathlib import Path
from bs4 import BeautifulSoup

sys.path.insert(0, str(Path(__file__).parent))
from keywords_data import ROWS, PAGES, CLUSTERS  # noqa

DIST = Path(sys.argv[1])
OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)
DEFAULT_BASE = (sys.argv[3] if len(sys.argv) > 3 else 'https://dmitryasta.github.io/').rstrip('/') + '/'
DATE = '2026-10-30'

PREFIX = {'EN': '', 'RU': '/ru', 'SR': '/sr'}
INTENT = {'K': 'Коммерческий', 'T': 'Транзакционный', 'I': 'Информационный', 'N': 'Навигационный', 'R': 'Исследовательский'}
GEO = {'RU': 'Россия', 'RS': 'Сербия', 'BAL': 'Балканы', 'INT': 'Международная аудитория'}
ORIGIN = {'S': 'Запрос из ТЗ (исходный список)', 'G': 'Пробел, замеченный в выдаче 30.10.2026', 'H': 'Гипотеза эксперта (подсказка, не статистика)'}
COMP = {
    1: 'Наблюдение: выдача занята авторитетными доменами (госгиды, юрфирмы, крупные сервисы)',
    2: 'Наблюдение: сервисных страниц в выборке мало или нет',
    3: 'Наблюдение: смешанная выдача (каталоги, новости, единичные сервисные страницы)',
    0: 'Не проверялась',
}
LANGNAME = {'EN': 'Английский', 'RU': 'Русский', 'SR': 'Сербский (латиница)', 'DE': 'Немецкий', 'TR': 'Турецкий', 'ZH': 'Китайский'}
SERVICE_NAME = {
    'S_ENTRY': 'Выход на рынок Сербии', 'S_DIST': 'Поиск дистрибьюторов и покупателей', 'S_IMP': 'Импорт в Сербию',
    'S_EXP': 'Экспорт из Сербии', 'S_REP': 'Местное коммерческое представительство', 'S_RES': 'Исследование рынка',
    'S_AUTO': 'Автоматизация бизнеса',
}


def path_for(lang, pid):
    pre = PREFIX[lang]
    if pid == 'home': p = '/'
    elif pid in ('about', 'services', 'contact', 'insights', 'privacy'): p = f'/{pid}/'
    elif pid.startswith('svc:'): p = f"/services/{pid[4:]}/"
    elif pid.startswith('art:'): p = f"/insights/{pid[4:]}/"
    else: raise ValueError(pid)
    return (pre + p) if pre else p


def load_page(path):
    f = DIST / path.lstrip('/') / 'index.html'
    html = f.read_text(encoding='utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    title = (soup.title.string or '').strip() if soup.title else ''
    md = soup.find('meta', attrs={'name': 'description'})
    desc = md['content'].strip() if md and md.get('content') else ''
    h1 = ' '.join(h.get_text(' ', strip=True) for h in soup.find_all('h1'))
    heads = [h.get_text(' ', strip=True) for h in soup.find_all(['h2', 'h3'])]
    faq = [s.get_text(' ', strip=True) for s in soup.select('details > summary')]
    main = soup.find('main') or soup.body
    for t in main.find_all(['script', 'style']): t.decompose()
    body = main.get_text(' ', strip=True)
    links = set()
    for a in soup.find_all('a', href=True):
        links.add(a['href'])
    return dict(title=title, desc=desc, h1=h1, heads=heads, faq=faq, body=body, links=links, html=html)


STOP = {
    'EN': {'to', 'in', 'of', 'the', 'how', 'for', 'a', 'and', 'vs', 'from', 'into', 'with', 'on'},
    'RU': {'в', 'на', 'из', 'и', 'по', 'как', 'для', 'при', 'с', 'или'},
    'SR': {'u', 'i', 'za', 'na', 'iz', 'o', 'od', 'kako', 'ili'},
}


def words(text):
    text = text.lower().replace('ё', 'е')
    return re.findall(r"[a-zа-яčćžšđ0-9\-]+", text)


def stem(w, lang):
    if lang == 'RU' and w.startswith('рынок'): w = 'рынк'
    if lang == 'RU' and w.startswith('сербск'): w = 'серб'
    if len(w) <= 4: return w
    return w[:5] if lang == 'EN' else w[:4]


def tokens(q, lang):
    return [stem(w, lang) for w in words(q) if w not in STOP.get(lang, set()) and len(w) > 1]


def covers(stems, text_words):
    """share of stems that appear as a prefix of some word"""
    if not stems: return 0.0
    ok = 0
    for s in stems:
        if any(w.startswith(s) for w in text_words): ok += 1
    return ok / len(stems)


# ---- parse rows ----
rows = []
cluster = None
for line in ROWS.strip().splitlines():
    line = line.strip()
    if not line: continue
    if line.startswith('#'):
        m = re.match(r'#\s*-+\s*([A-M])\.', line)
        if m: cluster = m.group(1)
        continue
    parts = line.split('|')
    assert len(parts) == 12, (len(parts), line)
    q, lang, geo, intent, origin, comp, cr, sf, ip, gap, page, note = parts
    rows.append(dict(q=q, lang=lang, geo=geo, intent=intent, origin=origin, comp=int(comp), cr=int(cr), sf=int(sf),
                     ip=int(ip), gap=int(gap), page=page, note=note, cluster=cluster))

# ---- score ----
for r in rows:
    raw = 4 * r['sf'] + 4 * r['cr'] + 3 * r['ip'] + 2.5 * r['gap']
    r['score'] = round(raw / 60 * 100)
    r['tier'] = 'A' if r['score'] >= 85 else 'B' if r['score'] >= 70 else 'C' if r['score'] >= 55 else 'D'

# ---- page index ----
cache = {}
def page(lang, key):
    pid = PAGES[key]
    path = path_for(lang, pid)
    if path not in cache:
        cache[path] = load_page(path)
    return path, cache[path]

# inbound internal links
all_paths = []
for lang in PREFIX:
    for key, pid in PAGES.items():
        all_paths.append(path_for(lang, pid))
for lang in PREFIX:
    for pid in ('insights', 'privacy'):
        all_paths.append(path_for(lang, pid))
for p in set(all_paths):
    if p not in cache: cache[p] = load_page(p)

def resolve(from_path, href):
    if href.startswith(('http', 'mailto:', '#', 'tel:')): return None
    from urllib.parse import urljoin, urlparse
    u = urlparse(urljoin('http://x' + from_path, href))
    p = u.path
    if not p.endswith('/'): p += '/'
    return p

inbound = collections.defaultdict(set)
for p, d in cache.items():
    for h in d['links']:
        t = resolve(p, h)
        if t and t != p and t in cache:
            inbound[t].add(p)

# ---- status ----
for r in rows:
    lang = r['lang']
    if r['page'] == '-' or lang not in PREFIX or r['tier'] == 'D':
        r['path'] = ''
        r['status'] = 'Не таргетируется'
        r['where'] = ''
        r['reason'] = r['note'] or ('низкий балл приоритизации' if r['tier'] == 'D' else 'нет языковой версии')
        if lang not in PREFIX: r['reason'] = 'нет языковой версии; ' + (r['note'] or '')
        if r['page'] != '-' and lang in PREFIX and r['tier'] == 'D':
            # still compute the path for reference
            r['path'] = path_for(lang, PAGES[r['page']])
        continue
    path, d = page(lang, r['page'])
    r['path'] = path
    st = tokens(r['q'], lang)
    head_words = words(' '.join([d['title'], d['h1']] + d['heads'] + d['faq']))
    body_words = words(' '.join([d['title'], d['desc'], d['h1'], d['body']]))
    where = []
    for name, txt in (('title', d['title']), ('description', d['desc']), ('H1', d['h1']), ('H2/H3', ' '.join(d['heads'])), ('FAQ', ' '.join(d['faq']))):
        if covers(st, words(txt)) == 1.0: where.append(name)
    r['where'] = ', '.join(where)
    ch = covers(st, head_words)
    cb = covers(st, body_words)
    if ch == 1.0: r['status'] = 'Внедрено: в заголовках страницы (title, H1, H2/H3 или вопрос FAQ)'
    elif cb == 1.0: r['status'] = 'Внедрено: в тексте страницы'
    elif cb >= 0.6: r['status'] = 'Частично: не все термины запроса есть на странице'
    else: r['status'] = 'Не покрыто: добавить в план правок'
    r['reason'] = r['note']

rows_sorted = rows  # keep thematic order, add rank
rank = {id(r): i + 1 for i, r in enumerate(sorted(rows, key=lambda x: (-x['score'], x['cluster'], x['q'])))}

# ---- CSV: SEO_KEYWORD_RESEARCH ----
HEAD = ['№', 'Ключевой запрос', 'Язык', 'География', 'Кластер', 'Поисковое намерение',
        'Подтвержденная или оценочная частотность', 'Источник статистики', 'Дата получения', 'Конкурентность',
        'Коммерческая релевантность (1-5)', 'Соответствие услугам Дмитрия (1-5)', 'Рекомендуемая страница', 'Приоритет',
        'Статус внедрения',
        'Происхождение запроса', 'Вероятность запроса услуги, а не справки (1-5)', 'Пробел в выдаче (0-2)', 'Баллы (0-100)', 'Ранг по баллам',
        'Где найден на странице', 'Примечание']
FREQ = 'нет данных (не измерялась)'
SRC = 'Недоступно: Wordstat вернул страницу сервисных работ, Google Trends без данных, доступа к Keyword Planner, Search Console и Яндекс Вебмастеру нет'

def row_out(i, r):
    page_label = ''
    if r['path']:
        nm = SERVICE_NAME.get(r['page'], '')
        page_label = r['path'] + (f' ({nm})' if nm else '')
    lang = LANGNAME.get(r['lang'], r['lang'])
    return [i, r['q'], lang, GEO[r['geo']], CLUSTERS[r['cluster']], INTENT[r['intent']], FREQ, SRC, DATE, COMP[r['comp']],
            r['cr'], r['sf'], page_label, f"{r['tier']} ({r['score']})", r['status'],
            ORIGIN[r['origin']], r['ip'], r['gap'], r['score'], rank[id(r)], r['where'], r['reason']]

with open(OUT / 'SEO_KEYWORD_RESEARCH.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(HEAD)
    for i, r in enumerate(rows, 1):
        w.writerow(row_out(i, r))

# ---- CSV: KEYWORD_TO_PAGE_MAP ----
MH = ['Ключевой запрос', 'Язык', 'Кластер', 'Приоритет', 'Страница (путь)', 'URL по умолчанию', 'Тип страницы', 'Роль', 'Где запрос внедрен',
      'Статус внедрения', 'Входящие внутренние ссылки (число)', 'Примеры страниц со ссылкой на эту страницу']
def page_type(key):
    if key.startswith('S_'): return 'Услуга'
    if key.startswith('A_'): return 'Статья'
    return {'H': 'Главная', 'ABOUT': 'О консультанте', 'SVCS': 'Список услуг', 'CONTACT': 'Контакты'}.get(key, '')
with open(OUT / 'KEYWORD_TO_PAGE_MAP.csv', 'w', newline='', encoding='utf-8-sig') as f:
    w = csv.writer(f)
    w.writerow(MH)
    for r in rows:
        if not r['path'] or r['status'] == 'Не таргетируется': continue
        inb = sorted(inbound.get(r['path'], []))
        w.writerow([r['q'], LANGNAME.get(r['lang'], r['lang']), CLUSTERS[r['cluster']], f"{r['tier']} ({r['score']})", r['path'],
                    DEFAULT_BASE + r['path'].lstrip('/'), page_type(r['page']),
                    'Основная страница для запроса', r['where'], r['status'], len(inb), '; '.join(inb[:4])])

# ---- summary json for the reports ----
summ = collections.OrderedDict()
summ['rows'] = len(rows)
summ['by_tier'] = collections.Counter(r['tier'] for r in rows)
summ['by_lang'] = collections.Counter(r['lang'] for r in rows)
summ['by_origin'] = collections.Counter(r['origin'] for r in rows)
summ['by_cluster'] = collections.Counter(r['cluster'] for r in rows)
summ['by_status'] = collections.Counter(r['status'] for r in rows)
tg = [r for r in rows if r['status'] != 'Не таргетируется']
summ['targeted'] = len(tg)
summ['targeted_status'] = collections.Counter(r['status'] for r in tg)
summ['tierAB_status'] = collections.Counter(r['status'] for r in rows if r['tier'] in 'AB' and r['status'] != 'Не таргетируется')
summ['uncovered'] = [(r['q'], r['lang'], r['path'], r['status']) for r in tg if r['status'].startswith(('Не покрыто', 'Частично'))]
summ['excluded'] = [(r['q'], r['lang'], r['tier'], r['score'], r['reason']) for r in rows if r['status'] == 'Не таргетируется']
(OUT / '_summary.json').write_text(json.dumps(summ, ensure_ascii=False, indent=1, default=dict), encoding='utf-8')

# ---- XLSX ----
try:
    from openpyxl import Workbook
    from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
    from openpyxl.utils import get_column_letter
    wb = Workbook()
    ws0 = wb.active; ws0.title = 'Методология'
    meth = [
        ('SEO_KEYWORD_RESEARCH: семантическое ядро Dmitry Astakhov | Serbia Market Entry & Trade Consulting', True),
        (f'Дата сбора наблюдений и проверки сайта: {DATE}.', False),
        ('', False),
        ('Что в таблице НЕТ', True),
        ('Нет частотности, сложности и стоимости клика. Инструменты недоступны: Yandex Wordstat вернул страницу сервисных работ, Google Trends вернул пустой блок, доступа к Keyword Planner, Search Console, Яндекс Вебмастеру, Ahrefs, Semrush нет. Ни одна цифра в таблице не является объемом спроса.', False),
        ('Поэтому столбец частотности заполнен фразой "нет данных (не измерялась)", а приоритет считается без частотности.', False),
        ('', False),
        ('Происхождение запросов', True),
        ('Запрос из ТЗ: исходный список кластеров A-J и раздела 6. Пробел: тема, по которой в выдаче 30.10.2026 не видно сервисных страниц (по двум файлам исследования выдачи). Гипотеза эксперта: предложенная формулировка, спрос на нее не подтвержден.', False),
        ('', False),
        ('Система приоритизации (прозрачная, без частотности)', True),
        ('Баллы = (4 x соответствие услуге + 4 x коммерческая релевантность + 3 x вероятность запроса услуги + 2,5 x пробел в выдаче) / 60 x 100.', False),
        ('Соответствие услуге (1-5): насколько запрос совпадает с услугой, которую Дмитрий действительно оказывает и которая описана на сайте.', False),
        ('Коммерческая релевантность (1-5): насколько ищущий похож на заказчика B2B (производитель, экспортер, импортер).', False),
        ('Вероятность запроса услуги (1-5): ищет ли человек консультанта, а не бесплатную справку или другую услугу (например, таможенного брокера).', False),
        ('Пробел в выдаче (0-2): 2 = сервисных страниц в выборке не видно, 1 = фрагментарно, 0 = выдача занята авторитетными доменами.', False),
        ('Приоритеты: A от 85, B от 70 до 84, C от 55 до 69, D ниже 55 (отдельно не таргетируется).', False),
        ('Частотность намеренно не входит в формулу: большой объем не может поднять запрос с низким соответствием услугам выше уровня C. Когда появятся данные Wordstat, Keyword Planner или Search Console, их нужно добавить отдельным столбцом и использовать для порядка внутри уровня.', False),
        ('Оценки 1-5 и 0-2 являются экспертными суждениями, а не измерениями; их стоит пересмотреть после появления данных о показах и обращениях.', False),
        ('', False),
        ('Статус внедрения', True),
        ('Считается автоматически по собранному сайту (qa/seo_tables.py): запрос засчитан, если все его значимые слова встречаются на целевой странице на языке запроса. "В заголовках" означает, что все слова есть в title, H1, H2/H3 или вопросах FAQ. Это проверка совместной встречаемости слов, а не точной фразы.', False),
        ('', False),
        ('Конкурентность', True),
        ('Описание наблюдения в американском поисковом инструменте 30.10.2026 (WebSearch), не позиции в Google или Яндексе и не показатель сложности.', False),
    ]
    for i, (t, b) in enumerate(meth, 1):
        c = ws0.cell(row=i, column=1, value=t)
        c.font = Font(bold=b, size=12 if b else 11)
        c.alignment = Alignment(wrap_text=True, vertical='top')
    ws0.column_dimensions['A'].width = 140

    ws = wb.create_sheet('Семантическое ядро')
    ws.append(HEAD)
    for i, r in enumerate(rows, 1):
        ws.append(row_out(i, r))
    hdr_fill = PatternFill('solid', fgColor='17263D')
    thin = Side(style='thin', color='CCCCCC')
    for c in ws[1]:
        c.font = Font(bold=True, color='FFFFFF'); c.fill = hdr_fill
        c.alignment = Alignment(wrap_text=True, vertical='center')
    widths = [5, 44, 14, 16, 30, 16, 22, 40, 12, 40, 12, 12, 46, 12, 40, 30, 14, 10, 10, 10, 24, 40]
    for i, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = wd
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = ws.dimensions
    tier_fill = {'A': 'D6F5DD', 'B': 'E4F0FF', 'C': 'FFF4CC', 'D': 'EEEEEE'}
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical='top')
        t = str(row[13].value)[0]
        row[13].fill = PatternFill('solid', fgColor=tier_fill.get(t, 'FFFFFF'))

    wm = wb.create_sheet('Карта запросов и страниц')
    wm.append(MH)
    for r in rows:
        if not r['path'] or r['status'] == 'Не таргетируется': continue
        inb = sorted(inbound.get(r['path'], []))
        wm.append([r['q'], LANGNAME.get(r['lang'], r['lang']), CLUSTERS[r['cluster']], f"{r['tier']} ({r['score']})", r['path'],
                   DEFAULT_BASE + r['path'].lstrip('/'), page_type(r['page']), 'Основная страница для запроса', r['where'], r['status'], len(inb), '; '.join(inb[:4])])
    for c in wm[1]:
        c.font = Font(bold=True, color='FFFFFF'); c.fill = hdr_fill; c.alignment = Alignment(wrap_text=True)
    for i, wd in enumerate([44, 14, 30, 12, 46, 70, 16, 28, 26, 44, 12, 60], 1):
        wm.column_dimensions[get_column_letter(i)].width = wd
    wm.freeze_panes = 'B2'; wm.auto_filter.ref = wm.dimensions

    wc = wb.create_sheet('Сводка')
    wc.append(['Показатель', 'Значение'])
    wc.append(['Всего запросов в таблице', len(rows)])
    wc.append(['Таргетируется (есть целевая страница)', len(tg)])
    for k, v in sorted(summ['by_tier'].items()): wc.append([f'Уровень {k}', v])
    for k, v in summ['targeted_status'].items(): wc.append([f'Среди таргетируемых: {k}', v])
    for k, v in summ['by_lang'].items(): wc.append([f'Язык {k}', v])
    for k, v in sorted(summ['by_cluster'].items()): wc.append([CLUSTERS[k], v])
    for c in wc[1]: c.font = Font(bold=True)
    wc.column_dimensions['A'].width = 80; wc.column_dimensions['B'].width = 14
    wb.save(OUT / 'SEO_KEYWORD_RESEARCH.xlsx')
except ImportError:
    print('openpyxl missing; xlsx not written')

print(json.dumps({k: (dict(v) if hasattr(v, 'items') else v) for k, v in summ.items() if k not in ('uncovered', 'excluded')}, ensure_ascii=False, indent=1))
print('UNCOVERED / PARTIAL:')
for u in summ['uncovered']: print(' ', u)
