const puppeteer = require('puppeteer');

let browserPromise = puppeteer.launch({
    args:[
        '--no-sandbox',
    ]
});

exports.screenshot = async (req, res) => {
    const url = req.query.url || 'https://aliexpress.com/';

    const browser = await browserPromise;
    const context = await browser.createIncognitoBrowserContext();
    const page = await context.newPage();

    await page.goto(url);

    const image = await page.screenshot();

    res.setHeader('Content-Type', 'image/png')
    res.send(image)

    context.close()
}