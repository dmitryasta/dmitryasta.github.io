export const LANGS = ['en', 'ru', 'sr'] as const;
export type Lang = (typeof LANGS)[number];
export const DEFAULT_LANG: Lang = 'en';

export const HTML_LANG: Record<Lang, string> = { en: 'en', ru: 'ru', sr: 'sr-Latn' };
export const HREFLANG: Record<Lang, string> = { en: 'en', ru: 'ru', sr: 'sr-Latn' };
export const OG_LOCALE: Record<Lang, string> = { en: 'en_US', ru: 'ru_RU', sr: 'sr_RS' };
export const LANG_LABEL: Record<Lang, string> = { en: 'English', ru: 'Русский', sr: 'Srpski' };
export const LANG_SHORT: Record<Lang, string> = { en: 'EN', ru: 'RU', sr: 'SR' };

export type PageKind =
  | 'home' | 'about' | 'services' | 'service' | 'insights' | 'article' | 'contact' | 'privacy';

export interface PageDef { id: string; kind: PageKind; path: string }

export const SERVICE_IDS = [
  'serbia-market-entry',
  'find-distributors-in-serbia',
  'import-to-serbia',
  'export-from-serbia',
  'local-commercial-representation',
  'serbia-market-research',
  'business-automation',
] as const;

export const ARTICLE_IDS = [
  'how-to-enter-the-serbian-market',
  'finding-distributors-in-serbia',
  'importing-food-products-into-serbia',
  'selling-to-serbian-retail-chains',
  'serbia-market-research-before-you-ship',
  'local-commercial-representation-in-serbia',
  'russia-serbia-trade-agreements-for-exporters',
] as const;

export const PAGES: PageDef[] = [
  { id: 'home', kind: 'home', path: '' },
  { id: 'about', kind: 'about', path: 'about/' },
  { id: 'services', kind: 'services', path: 'services/' },
  ...SERVICE_IDS.map((id) => ({ id: `svc:${id}`, kind: 'service' as const, path: `services/${id}/` })),
  { id: 'insights', kind: 'insights', path: 'insights/' },
  ...ARTICLE_IDS.map((id) => ({ id: `art:${id}`, kind: 'article' as const, path: `insights/${id}/` })),
  { id: 'contact', kind: 'contact', path: 'contact/' },
  { id: 'privacy', kind: 'privacy', path: 'privacy/' },
];

export const PAGE_MAP: Record<string, PageDef> = Object.fromEntries(PAGES.map((p) => [p.id, p]));

const BASE: string = import.meta.env.BASE_URL.endsWith('/') ? import.meta.env.BASE_URL : import.meta.env.BASE_URL + '/';

/** Site-relative URL of a page in a language, including the GitHub Pages sub-path. */
export function href(lang: Lang, id: string): string {
  const def = PAGE_MAP[id];
  if (!def) throw new Error(`Unknown page id: ${id}`);
  return BASE + (lang === DEFAULT_LANG ? '' : `${lang}/`) + def.path;
}

/** Absolute URL, used for canonical, hreflang, Open Graph, sitemap and structured data. */
export function absUrl(lang: Lang, id: string): string {
  return new URL(href(lang, id), import.meta.env.SITE).toString();
}

/** URL of a file in /public (fonts, images, robots) with the sub-path applied. */
export function asset(path: string): string {
  return BASE + path.replace(/^\//, '');
}

export function absAsset(path: string): string {
  return new URL(asset(path), import.meta.env.SITE).toString();
}
