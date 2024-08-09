const puppeteer = require('puppeteer');
const path = require('path');

const args = process.argv.slice(2);
const htmlFile = args[0];
const pngFile = args[1];

// Ensure the paths are correctly resolved
const filePath = path.resolve(__dirname, '..', htmlFile); // Ensures no double "src"
const outputPath = path.resolve(__dirname, '..',  pngFile);

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: outputPath, fullPage: true });
    await browser.close();
})();
