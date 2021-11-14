const puppeteer = require('puppeteer');
const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue, WriteBatch } = require('firebase-admin/firestore');
const {PubSub} = require('@google-cloud/pubsub');
// const serviceAccount = require('/home/ankebod/gp-intellectual-property-rights-tracking/torbjorn-zetterlund-e9d45e69e6a8.json');

// initializeApp({
//   credential: cert(serviceAccount)
// });

initializeApp()

const db = getFirestore();
let browserPromise = puppeteer.launch({
    args:[
        '--no-sandbox',
        '--shm-size=1gb'
    ]
});


exports.main = async (req, res) => {
    try { 
        const queryArray = await getQueries()
        
        for (const query of queryArray) {  

            var url = 'https://www.aliexpress.com/w/wholesale-' + query + '.html'
            console.log(url);
            
            // Open a page
            const browser = await browserPromise;
            const context = await browser.createIncognitoBrowserContext();
            const page = await context.newPage();
            
            page.setDefaultNavigationTimeout(0);  
            await page.goto(url);

            try {
                await page.waitForSelector('._1OUGS');

                // Scrape the page
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
                // Store the results  
                const merchDb = db.collection('illegalmerchandise');
                for (const doc of results) {
                    const docRef = await merchDb.add(doc);
                    await docRef.update({
                        timestamp: FieldValue.serverTimestamp()
                    })
                }

            } catch {
                console.log("No results for this query");
            }  
            await context.close()

        }

        // Publish a message to PubSub to trigger the selector
        await pubMessage("items-added")

        console.log("Success");
        res.status(200).send('Great we found results and published a message');
        
    } catch(error) {

        console.log(error);
        res.status(418).send("Oeps, something went wrong");
    }
}

async function getQueries(){
    // Get query data
    const queryDb = db.collection('searchquery'); 
    const queries = await queryDb.where('active', '==', true).get(); 
    
    
    var queryArray = [];

    queries.forEach(doc => {
        const query = doc.data()['queryterm']
        const term = encodeURIComponent(query)
        queryArray.push(term)
    })
    return queryArray;
}

async function pubMessage(topic){
    // Publish a message to PubSub to trigger the selector
    const pubsub = new PubSub();

    try {
        var topic = pubsub.topic(topic); 
    } catch {
        var topic = await pubSub.createTopic(topic);
    }

    const messageBuffer = Buffer.from(JSON.stringify({data: 'Run Selector'}));
    await topic.publish(messageBuffer)
}