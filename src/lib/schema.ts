import { SITE } from './site';
import { absUrl, HREFLANG, type Lang } from './pages';
import { ui } from '../i18n';

const ROOT = () => absUrl('en', 'home');
export const personId = () => `${ROOT()}#person`;
export const websiteId = () => `${ROOT()}#website`;

export function personNode(lang: Lang, full = true) {
  const t = ui(lang);
  const ref = { '@type': 'Person', '@id': personId(), name: SITE.name };
  if (!full) return ref;
  return {
    ...ref,
    url: absUrl(lang, 'about'),
    jobTitle: t.schema.jobTitle,
    description: t.schema.description,
    email: `mailto:${SITE.email}`,
    alternateName: ['Дмитрий Астахов', 'Dmitrij Astahov'],
    address: { '@type': 'PostalAddress', addressLocality: SITE.city, addressCountry: SITE.countryCode },
    homeLocation: { '@type': 'Place', name: `${SITE.city}, ${SITE.country}` },
    sameAs: [SITE.linkedin],
    knowsAbout: t.schema.knowsAbout,
    knowsLanguage: ['ru', 'en', 'sr'],
    alumniOf: [
      { '@type': 'CollegeOrUniversity', name: 'National Research University Higher School of Economics' },
      { '@type': 'EducationalOrganization', name: 'Moscow Business School' },
    ],
  };
}

export function websiteNode(lang: Lang) {
  return {
    '@type': 'WebSite',
    '@id': websiteId(),
    name: `${SITE.name} | ${SITE.tagline}`,
    url: absUrl(lang, 'home'),
    inLanguage: HREFLANG[lang],
    publisher: { '@id': personId() },
  };
}

export function breadcrumbNode(items: { name: string; url: string }[]) {
  return {
    '@type': 'BreadcrumbList',
    itemListElement: items.map((it, i) => ({ '@type': 'ListItem', position: i + 1, name: it.name, item: it.url })),
  };
}

export function faqNode(items: { q: string; a: string }[]) {
  const strip = (s: string) => s.replace(/\*\*/g, '');
  return {
    '@type': 'FAQPage',
    mainEntity: items.map((it) => ({ '@type': 'Question', name: it.q, acceptedAnswer: { '@type': 'Answer', text: strip(it.a) } })),
  };
}

export function graph(nodes: unknown[]) {
  return { '@context': 'https://schema.org', '@graph': nodes };
}
