import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

// NOTE: `site` is overwritten at deploy time by the real production URL.
// After the first Vercel deploy, replace it with the canonical domain.
export default defineConfig({
  site: 'https://ancient-chinawonder.vercel.app',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: 'github-light', wrap: true },
  },
  build: {
    format: 'directory',
    inlineStylesheets: 'auto',
  },
});
