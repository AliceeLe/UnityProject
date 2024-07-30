const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  const htmlFilePath = path.resolve(__dirname, 'email_template.html');
  const htmlContent = fs.readFileSync(htmlFilePath, 'utf8');

  await page.setContent(htmlContent, { waitUntil: 'networkidle0' });

  await page.screenshot({
    path: 'src/email.png',
    fullPage: true
  });

  await browser.close();
})();
