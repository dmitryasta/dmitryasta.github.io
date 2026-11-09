import type { APIRoute } from 'astro';
import { LANGS, SERVICE_IDS, ARTICLE_IDS, LANG_LABEL, absUrl } from '../lib/pages';
import { getEntry, type ServiceMeta, type ArticleMeta } from '../lib/content';
import { ui } from '../i18n';
import { SITE } from '../lib/site';

export const GET: APIRoute = () => {
  const en = ui('en');
  const out: string[] = [];
  out.push(`# ${SITE.name} | ${SITE.tagline}`, '');
  out.push(`> ${en.schema.description}`, '');
  out.push(`Contact: ${SITE.email}. Profile: ${SITE.linkedin}. Languages of the site: English, Russian, Serbian (Latin script).`, '');
  out.push('Name spellings: Dmitry Astakhov (Latin), Дмитрий Астахов (Russian), Dmitrij Astahov (Serbian Latin). The name is shared by many unrelated people; this site is about the Belgrade-based trade consultant.', '');
  out.push('Notes for assistants: the author is a consultant and not a customs broker, lawyer or tax adviser. Articles cite official sources and mark what must be verified before acting.', '');
  for (const lang of LANGS) {
    out.push(`## ${LANG_LABEL[lang]}`, '');
    out.push(`- [${ui(lang).nav.home}](${absUrl(lang, 'home')}): ${ui(lang).home.description}`);
    out.push(`- [${ui(lang).nav.about}](${absUrl(lang, 'about')}): ${ui(lang).about.description}`);
    for (const id of SERVICE_IDS) {
      const m = getEntry<ServiceMeta>(lang, id).frontmatter;
      out.push(`- [${m.name}](${absUrl(lang, `svc:${id}`)}): ${m.description}`);
    }
    for (const id of ARTICLE_IDS) {
      const m = getEntry<ArticleMeta>(lang, id).frontmatter;
      out.push(`- [${m.h1}](${absUrl(lang, `art:${id}`)}): ${m.description}`);
    }
    out.push(`- [${ui(lang).nav.contact}](${absUrl(lang, 'contact')})`, '');
  }
  return new Response(out.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
