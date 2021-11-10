const puppeteer = require('puppeteer');
const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue, WriteBatch } = require('firebase-admin/firestore');
const serviceAccount = require('/home/ankebod/gp-intellectual-property-rights-tracking/torbjorn-zetterlund-e9d45e69e6a8.json');

initializeApp({
  credential: cert(serviceAccount)
});

// initializeApp()

const db = getFirestore();
let browserPromise = puppeteer.launch({
    args:[
        '--no-sandbox',
        '--shm-size=1gb'
    ]
});


exports.alibot = async (req, res) => {
    try {    
        var term = req.query.term || "greenpeace+shirt";
        var url = 'https://www.aliexpress.com/w/wholesale-' + term + '.html'
        console.log(url);

        const browser = await browserPromise;
        const context = await browser.createIncognitoBrowserContext();
        const page = await context.newPage();
        
        page.setDefaultNavigationTimeout(0);  
        await page.goto(url);

        await page.waitForSelector('._1OUGS');

        let results = await page.evaluate(() => {
            var base = 'https://www.aliexpress.com'
            var productList = document.querySelectorAll('a._9tla3');
            var imageList = document.querySelectorAll('img.A3Q1M');
            var storeList = document.querySelectorAll('a._2lsU7');
            var resultArray = [];

            for (var i = 0; i < productList.length; i++){
                resultArray[i] = {
                    contact_seller : '',
                    item_image_title : imageList[i].getAttribute('alt'),
                    item_image_url : imageList[i].getAttribute('src'),
                    item_url : base + productList[i].getAttribute('href'),
                    location : '',
                    seller : storeList[i].innerHTML.trim(),
                    shop : 'aliexpress',
                    site : base,
                    status : false,
                    store_url : storeList[i].getAttribute('href'),
                    note : 'test'
                }
            }
            return resultArray
        })

        await context.close()
        
        const merch_db = db.collection('illegalmerchandise');
        for (const doc of results) {
            await merch_db.add(doc);
        }

        console.log("Success");
        res.status(200).send(JSON.stringify(results));
    
    } catch(error) {

        console.log(error);
        res.status(418).send("Oeps, something went wrong");
    }
}