const puppeteer = require('puppeteer');
const { initializeApp, applicationDefault, cert } = require('firebase-admin/app');
const { getFirestore, Timestamp, FieldValue, WriteBatch } = require('firebase-admin/firestore');
const {PubSub} = require('@google-cloud/pubsub');
const { logger } = require('firebase-functions/v1');
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

            var url = 'https://www.ebay.com/sch/i.html?_&_nkw=' + query
            
            // Open a page
            const browser = await browserPromise;
            const context = await browser.createIncognitoBrowserContext();
            const page = await context.newPage();
            
            page.setDefaultNavigationTimeout(0);  
            await page.goto(url);

            try {
                await page.waitForSelector('a.s-item__link');

                // Scrape the result page
                let results = await page.evaluate(() => {
                    var base = 'https://www.ebay.com'
                    var productList = document.querySelectorAll('a.s-item__link[target]');
                    var imageList = document.querySelectorAll('img.s-item__image-img');
                    var resultArray = [];

                    for (var i = 0; i < productList.length; i++){                        
                        resultArray[i] = {
                            contact_seller : '',
                            item_image_title : imageList[i].getAttribute('alt'),
                            item_image_url : imageList[i].getAttribute('src'),
                            item_url : productList[i].getAttribute('href'),
                            shop : 'ebay',
                            site : base,
                            status : false,
                            note : '',
                            location : '',
                            seller : '',
                            store_url : ''
                        }
                      
                    }
                    return resultArray
                })

                // // Scrape the product pages
                // for (var i = 0; i < results.length; i++){
                //     var link = results[i]['item_url']
                //     startTime = new Date();
                //     console.log(link);
                //     let site = await fulfillWithTimeLimit(2000, page.goto(link), null);
                    
                //     // await page.waitForSelector('div.iti-eu-bld-gry span[itemprop]');
                //     if(site != null){
                //         let info = await page.evaluate(() => {
                //             var infoArray = []

                //             infoArray = {
                //                 location : document.querySelector('div.iti-eu-bld-gry span[itemprop]').innerHTML.trim(),
                //                 seller : document.querySelector('div.bdg-90 a span.mbg-nw').innerHTML.trim(),
                //                 store_url : document.querySelector('div.si-pd-a a')['href']
                //             }

                //             return infoArray
                //         })    

                //         results[i]['location'] = info['location']
                //         results[i]['seller'] = info['seller']
                //         results[i]['store_url'] = info['store_url']
                //         endTime = new Date();
                //     }
                // } 
                
                // Store the results  
                const merchDb = db.collection('illegalmerchandise');
                for (const doc of results) {
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
        var topic = await pubsub.createTopic(topic);
    }

    const messageBuffer = Buffer.from(JSON.stringify({data: 'Run Selector'}));
    await topic.publish(messageBuffer)
}

async function fulfillWithTimeLimit(timeLimit, task, failureValue){
    let timeout;
    const timeoutPromise = new Promise((resolve, reject) => {
        timeout = setTimeout(() => {
            resolve(failureValue);
        }, timeLimit);
    });
    const response = await Promise.race([task, timeoutPromise]);
    if(timeout){ //the code works without this but let's be safe and clean up the timeout
        clearTimeout(timeout);
    }
    return response;
}