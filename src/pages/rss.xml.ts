import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { SITE } from '../consts';

const esc = (s: string) =>
  s
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');

export const GET: APIRoute = async (context) => {
  const stories = (await getCollection('stories'))
    .sort((a, b) => b.data.published.valueOf() - a.data.published.valueOf())
    .slice(0, 40);

  const site = (context.site ?? new URL(SITE.url)).toString().replace(/\/$/, '');
  const abs = (u: string) => new URL(u, `${site}/`).toString();

  const items = stories
    .map((s) => {
      const url = `${site}/stories/${s.id}/`;
      return `    <item>
      <title>${esc(s.data.title)} (${esc(s.data.titleZh)})</title>
      <link>${url}</link>
      <guid isPermaLink="true">${url}</guid>
      <pubDate>${new Date(s.data.published).toUTCString()}</pubDate>
      <description>${esc(s.data.excerpt)}</description>
      <category>${esc(s.data.sourceZh)}</category>
${s.data.tags.map((t) => `      <category>${esc(t)}</category>`).join('\n')}
${s.data.image ? `      <enclosure url="${abs(s.data.image)}" type="image/jpeg" />` : ''}
    </item>`;
    })
    .join('\n');

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${esc(SITE.name)}</title>
    <link>${site}/</link>
    <description>${esc(SITE.description)}</description>
    <language>en</language>
    <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
    <atom:link href="${site}/rss.xml" rel="self" type="application/rss+xml" />
${items}
  </channel>
</rss>
`;

  return new Response(xml, {
    headers: {
      'Content-Type': 'application/rss+xml; charset=utf-8',
      'Cache-Control': 'public, max-age=0, s-maxage=3600',
    },
  });
};
