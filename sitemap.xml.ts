import type { APIRoute } from 'astro';
import { LANGS, PAGES, HREFLANG, absUrl } from '../lib/pages';
import { SITE } from '../lib/site';

export const GET: APIRoute = () => {
  const urls = LANGS.flatMap((lang) =>
    PAGES.map((p) => {
      const alts = LANGS.map((l) => `    <xhtml:link rel="alternate" hreflang="${HREFLANG[l]}" href="${absUrl(l, p.id)}"/>`).join('\n');
      const def = `    <xhtml:link rel="alternate" hreflang="x-default" href="${absUrl('en', p.id)}"/>`;
      const prio = p.kind === 'home' ? '1.0' : p.kind === 'service' || p.kind === 'services' ? '0.9' : p.kind === 'privacy' ? '0.2' : '0.7';
      return `  <url>\n    <loc>${absUrl(lang, p.id)}</loc>\n    <lastmod>${SITE.published}</lastmod>\n    <priority>${prio}</priority>\n${alts}\n${def}\n  </url>`;
    }),
  );
  const xml = `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${urls.join('\n')}\n</urlset>\n`;
  return new Response(xml, { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
};
