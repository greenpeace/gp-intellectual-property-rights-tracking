const puppeteer = require('puppeteer');
const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue, WriteBatch } = require('firebase-admin/firestore');
const {PubSub} = require('@google-cloud/pubsub');
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


exports.main = async (req, res) => {
    try { 
        const queryArray = await getQueries()
        
        for (const query of queryArray) {  

            var url = 'https://www.ebay.com/sch/i.html?_&_nkw=' + query
            console.log(url);
            
            // Open a page
            const browser = await browserPromise;
            const context = await browser.createIncognitoBrowserContext();
            const page = await context.newPage();
            
            page.setDefaultNavigationTimeout(0);  
            await page.goto(url);

            try {
                await page.waitForSelector('a.s-item__link');

                // Scrape the page
                let results = await page.evaluate(() => {
                    var base = 'https://www.ebay.com'
                    var productList = document.querySelectorAll('a.s-item__link[target]');
                    var imageList = document.querySelectorAll('img.s-item__image-img');
                    var locationList = document.querySelectorAll('span.s-item__location.s-item__itemLocation');
                    var resultArray = [];

                    for (var i = 0; i < productList.length; i++){
                        try {
                            var loc = locationList[i].innerHTML.trim().split(' ');
                            loc.shift()
                            loc = loc.join(' ')
                        }
                        catch {
                            var loc = ''
                        }
                        
                        resultArray[i] = {
                            contact_seller : '',
                            item_image_title : imageList[i].getAttribute('alt'),
                            item_image_url : imageList[i].getAttribute('src'),
                            item_url : productList[i].getAttribute('href'),
                            location : loc,
                            seller : '',
                            shop : 'ebay',
                            site : base,
                            status : false,
                            store_url : '',
                            note : ''
                        }
                    }
                    return resultArray
                })
                
                // Store the results  
                const merchDb = db.collection('illegalmerchandise');
                for (const doc of results) {
                    console.log(doc);
                    const docRef = await merchDb.add(doc);
                    await docRef.update({
                        timestamp: FieldValue.serverTimestamp()
                    })
                }
                console.log("We found " + results.length + " results")

            } catch (error) {
                console.log(error);
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