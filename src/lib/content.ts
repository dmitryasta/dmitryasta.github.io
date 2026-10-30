import type { Lang } from './pages';

export interface Faq { q: string; a: string }
export interface Step { t: string; d: string }
export interface SourceRef { title: string; url: string; note?: string }

export interface ServiceMeta {
  name: string;           // short label for navigation and cards
  title: string;          // <title>
  description: string;    // meta description
  h1: string;
  lead: string;
  short: string;          // card text
  serviceType: string;    // schema.org serviceType
  forWhom: string[];
  included: string[];
  steps: Step[];
  outcomes: string[];
  limits: string[];
  faq: Faq[];
  related: string[];      // article ids
}

export interface ArticleMeta {
  title: string;
  description: string;
  h1: string;
  topic: string;
  date: string;           // ISO
  updated?: string;
  keyPoints: string[];
  faq: Faq[];
  sources: SourceRef[];
  relatedServices: string[];
  relatedArticles: string[];
}

interface MdModule<T> { frontmatter: T; Content: any; rawContent: () => string }

const modules = import.meta.glob('../content/*/*.md', { eager: true }) as Record<string, MdModule<any>>;

export function getEntry<T = any>(lang: Lang, id: string): MdModule<T> {
  const key = `../content/${lang}/${id}.md`;
  const mod = modules[key];
  if (!mod) throw new Error(`Missing content file: src/content/${lang}/${id}.md`);
  return mod as MdModule<T>;
}

export function readingMinutes(raw: string): number {
  const words = raw.split(/\s+/).filter(Boolean).length;
  return Math.max(2, Math.round(words / 200));
}
