#!/usr/bin/env node
// Renderiza cada <section class="slide"> de um HTML em um PNG separado.
// Uso: node render.js <arquivo.html> <pasta-saida> [largura] [altura]
// Padrão 1080x1350 (retrato 4:5, o formato que ocupa mais tela no feed).
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

(async () => {
  const [input, outDir, w = '1080', h = '1350'] = process.argv.slice(2);
  if (!input || !outDir) {
    console.error('Uso: node render.js <arquivo.html> <pasta-saida> [largura] [altura]');
    process.exit(1);
  }
  const width = Number(w), height = Number(h);
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(input), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);

  const slides = await page.$$('.slide');
  if (!slides.length) {
    console.error('Nenhum elemento .slide encontrado no HTML.');
    process.exit(1);
  }
  for (let i = 0; i < slides.length; i++) {
    const box = await slides[i].boundingBox();
    if (Math.round(box.width) !== width || Math.round(box.height) !== height) {
      console.warn(`Aviso: slide ${i + 1} mede ${Math.round(box.width)}x${Math.round(box.height)}, esperado ${width}x${height}`);
    }
    const file = path.join(outDir, `slide-${String(i + 1).padStart(2, '0')}.png`);
    await slides[i].screenshot({ path: file });
    console.log(file);
  }
  await browser.close();
})();
