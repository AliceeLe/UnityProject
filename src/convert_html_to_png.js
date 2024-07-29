const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    const filePath = path.join(__dirname, 'email_template.html');
    await page.goto(`file://${filePath}`, { waitUntil: 'networkidle2' });
    await page.screenshot({ path: path.join(__dirname, 'email.png'), fullPage: true });
    await browser.close();
})();
