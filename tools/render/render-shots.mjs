// Opens the site's live-render pages in headless Chrome, lets js/scene.js draw
// every box photo exactly as it would for a visitor, and saves each one to
// img/shots/<key>.webp. Run through tools/render-shots.sh, not directly.
import { chromium } from "playwright";
import { writeFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const base = process.argv[2] || "http://127.0.0.1:8799/";
const out = join(dirname(fileURLToPath(import.meta.url)), "..", "..", "img", "shots");
mkdirSync(out, { recursive: true });

// system Chrome if present (no extra download), else Playwright's Chromium
const browser = await chromium.launch({ channel: "chrome" }).catch(() => chromium.launch());
const page = await browser.newPage({ viewport: { width: 1280, height: 900 } });
const saved = new Set();
for (const path of ["index.html", "plans.html", "how-it-works.html", "about.html", "cities.html"]) {
  await page.goto(base + path, { waitUntil: "load" });
  await page.waitForFunction(
    () => [...document.querySelectorAll("img[data-shot]")].every((i) => i.src.startsWith("data:")),
    null, { timeout: 60000 });
  // Re-encode each PNG as WebP in the page (Chrome can; keeps transparency, ~70% smaller).
  const shots = await page.evaluate(async () => {
    const res = {};
    for (const img of document.querySelectorAll("img[data-shot]")) {
      const key = img.dataset.shot === "city" ? `city-${img.dataset.num}` : img.dataset.shot;
      if (res[key]) continue;
      const bmp = await createImageBitmap(await (await fetch(img.src)).blob());
      const c = document.createElement("canvas"); c.width = bmp.width; c.height = bmp.height;
      c.getContext("2d").drawImage(bmp, 0, 0);
      res[key] = c.toDataURL("image/webp", 0.86);
    }
    return res;
  });
  for (const [key, url] of Object.entries(shots)) {
    if (saved.has(key)) continue;
    writeFileSync(join(out, `${key}.webp`), Buffer.from(url.split(",")[1], "base64"));
    saved.add(key);
  }
  console.log(`${path}: ${Object.keys(shots).length} shots`);
}
await browser.close();
console.log(`saved ${saved.size} files to img/shots/`);
