"""Checks of the markdown content in src/content (run from the project root): python3 qa/check_content.py
- front matter is valid YAML; the same ids and the same structure in en, ru, sr (keys, list lengths);
- body structure matches across languages (number of H2 headings, table rows, links);
- title (without the " | Dmitry Astakhov" suffix) <= 60, description <= 160 characters; articles have a date and at least one source;
- no letter yo, no long or medium dashes anywhere; no Cyrillic in the Serbian Latin files."""
import re, sys, pathlib, yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent / 'src' / 'content'
LANGS = ['en', 'ru', 'sr']
problems = []
def bad(m): problems.append(m)

def shape(v):
    if isinstance(v, dict): return {k: shape(x) for k, x in v.items()}
    if isinstance(v, list): return [len(v)] + ([shape(v[0])] if v else [])
    return type(v).__name__

data = {}
for lang in LANGS:
    for f in sorted((ROOT / lang).glob('*.md')):
        t = f.read_text(encoding='utf-8')
        m = re.match(r'^---\n(.*?)\n---\n(.*)$', t, re.S)
        if not m: bad(f'{lang}/{f.name}: no front matter'); continue
        try: fm = yaml.safe_load(m.group(1))
        except Exception as e: bad(f'{lang}/{f.name}: YAML error {e}'); continue
        body = m.group(2)
        data[(lang, f.stem)] = (fm, body)
        if re.search('[ёЁ]', t): bad(f'{lang}/{f.name}: contains the letter yo')
        if re.search('[–—]', t): bad(f'{lang}/{f.name}: contains a dash character')
        if lang == 'sr' and re.search('[Ѐ-ӿ]', t): bad(f'{lang}/{f.name}: Cyrillic in Serbian Latin file')
        title = fm.get('title', ''); desc = fm.get('description', '')
        if len(title.replace(' | Dmitry Astakhov', '')) > 60: bad(f'{lang}/{f.name}: title (without suffix) {len(title)} chars')
        if len(desc) > 160: bad(f'{lang}/{f.name}: description {len(desc)} chars')
        if 'date' in fm:
            if not fm.get('sources'): bad(f'{lang}/{f.name}: article without sources')
            if not re.match(r'^\d{4}-\d{2}-\d{2}$', str(fm['date'])): bad(f'{lang}/{f.name}: date format')

ids = {i for (_, i) in data}
for i in sorted(ids):
    for lang in LANGS:
        if (lang, i) not in data: bad(f'{lang}/{i}.md missing'); 
    if all((l, i) in data for l in LANGS):
        base = shape(data[('en', i)][0])
        for lang in ('ru', 'sr'):
            if shape(data[(lang, i)][0]) != base: bad(f'{lang}/{i}.md: front matter structure differs from en')
        b = {l: data[(l, i)][1] for l in LANGS}
        def cnt(rx, s): return len(re.findall(rx, s, re.M))
        for name, rx in (('H2 headings', r'^## '), ('table rows', r'^\|'), ('links', r'\]\(')):
            vals = {l: cnt(rx, b[l]) for l in LANGS}
            if len(set(vals.values())) != 1: bad(f'{i}: {name} differ {vals}')
print(f'files: {len(data)} ({len(ids)} ids x {len(LANGS)} languages)')
print('PROBLEMS: none' if not problems else 'PROBLEMS:\n' + '\n'.join(problems))
sys.exit(1 if problems else 0)
