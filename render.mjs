// render.mjs — screenshot render.html (1024x1024) to entry.png with Playwright.
// Run: node render.mjs  (writes entry.png beside this file)
// playwright-core is resolved from the local install or /tmp/pw-test;
// Chromium comes from ~/.cache/ms-playwright.
import { createRequire } from 'node:module';
import { existsSync, readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const out = process.argv[2] ?? join(here, 'entry.png');
const html = 'file://' + join(here, 'render.html');

function loadPlaywright() {
  const req = createRequire(import.meta.url);
  try { return req('playwright-core'); } catch { /* fall through */ }
  for (const base of ['/tmp/pw-test/node_modules']) {
    try {
      const r = createRequire(join(base, 'playwright-core', 'package.json'));
      return r('playwright-core');
    } catch { /* fall through */ }
  }
  throw new Error('playwright-core not found');
}
const { chromium } = loadPlaywright();

function findChrome() {
  const cache = join(homedir(), '.cache', 'ms-playwright');
  const cands = [];
  try {
    for (const d of readdirSync(cache)) {
      if (d.startsWith('chromium-')) {
        cands.push(join(cache, d, 'chrome-linux64', 'chrome'));
        cands.push(join(cache, d, 'chrome-linux', 'chrome'));
        cands.push(join(cache, d, 'chrome-linux64', 'headless_shell'));
        cands.push(join(cache, d, 'chrome-linux', 'headless_shell'));
      }
      if (d.startsWith('chromium_headless_shell-')) {
        cands.push(join(cache, d, 'chrome-headless-shell-linux64', 'headless_shell'));
        cands.push(join(cache, d, 'chrome-linux', 'headless_shell'));
      }
    }
  } catch { /* no cache */ }
  return cands.find((p) => existsSync(p));
}

const executablePath = process.env.CHROME_PATH || findChrome();
if (!executablePath) throw new Error('no Chromium found in ~/.cache/ms-playwright');
const browser = await chromium.launch({ executablePath, args: ['--no-sandbox', '--force-color-profile=srgb'] });
const page = await browser.newPage({ viewport: { width: 1024, height: 1024 }, deviceScaleFactor: 1 });
await page.goto(html, { waitUntil: 'load' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(400);
await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1024, height: 1024 } });
await browser.close();
console.log('wrote', out);
