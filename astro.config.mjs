import { defineConfig } from 'astro/config';

// Public address and sub-path of the published site.
// Default: the site sits at the root of https://dmitryasta.github.io/ (repository named dmitryasta.github.io).
// On GitHub Pages the workflow in .github/workflows/deploy.yml sets both values
// automatically from the repository. For a local build the defaults below are used.
// With a custom domain set SITE_URL=https://your-domain.com and BASE_PATH=/
const site = (process.env.SITE_URL || 'https://dmitryasta.github.io').replace(/\/$/, '');
let base = process.env.BASE_PATH ?? '/';
if (!base.startsWith('/')) base = '/' + base;
base = base.replace(/\/$/, '');
if (base === '') base = '/';

export default defineConfig({
  site,
  base,
  trailingSlash: 'always',
  compressHTML: true,
  build: { format: 'directory', inlineStylesheets: 'auto' },
  devToolbar: { enabled: false },
  server: { host: true },
});
