import type { APIRoute } from 'astro';
import { asset } from '../lib/pages';

const BOTS = ['OAI-SearchBot', 'GPTBot', 'ChatGPT-User', 'PerplexityBot', 'Perplexity-User', 'ClaudeBot', 'Claude-SearchBot', 'Claude-User', 'Google-Extended', 'Applebot', 'Bingbot', 'Googlebot', 'YandexBot'];

export const GET: APIRoute = ({ site }) => {
  const origin = (site ?? new URL('https://example.com')).toString().replace(/\/$/, '');
  const lines = ['# Public information site: all crawlers, including search and AI assistants, are welcome.', ''];
  for (const b of BOTS) lines.push(`User-agent: ${b}`, 'Allow: /', '');
  lines.push('User-agent: *', 'Allow: /', '', `Sitemap: ${origin}${asset('sitemap.xml')}`, '');
  return new Response(lines.join('\n'), { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
