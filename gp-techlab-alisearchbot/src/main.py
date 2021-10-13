import logging
import re
import firebase_admin
from firebase_admin import credentials, firestore
from pyppeteer import launch

# import asyncio # only local
# PROJECT = 'torbjorn-zetterlund' # only local
# logging.basicConfig(filename='test.log', level=logging.INFO) # only local

from config import PROJECT # only cloud



# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

async def main(request):
    
    # Database Details
    searchquery_ref = db.collection(u'searchquery')

    # Empty list to store keywords in
    keywords = [] 
    shop = "aliexpress"

    # Read from Database the aliexpress url that are active
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = query.replace(" ", "+")
        counter = 0

        url = 'https://www.aliexpress.com/w/wholesale-' + query + '.html'
        try:
            # Start a session
            browser = await launch(headless=True, ignoreHTTPSErrors=True, args=['--no-sandbox'])
            page = await browser.newPage()
            await page.goto(url)

            products = await page.querySelectorAll('._1OUGS')

            # Get products
            logging.info(f"Found {len(products)} products")

            for product in products:
                # Grab item url
                l = await product.querySelector('a._9tla3[href]')
                item_url = await page.evaluate('(element) => element.href', l)
                # item_url = cleanurl(item_url)
                
                # Grab image title
                i = await product.querySelector('img.A3Q1M[alt]')
                item_image_title = await page.evaluate('(element) => element.alt', i)

                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                docsname = db.collection(u'illegalmerchandise').where(u'item_image_title', u'==', item_image_title).stream()

                if (len(list(docsurl))) or (len(list(docsname))):
                    logging.info("URL Exist, we will ignore")
                
                else:
                    logging.info("URL Not found, we will add to database")
                        
                    # Retrieve keywords to check them in product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))

                    # Check if keywords exists in Product title
                    if not any(x in item_image_title for x in keywords):
                        logging.info("No match on Keywords")

                    #  Do not catch vintage with case insensitive search
                    elif re.search('vintage', item_image_title, re.IGNORECASE):
                        logging.info("Word vintage in title, skip")

                    # Otherwise add to database    
                    else:
                        u = await product.querySelector('img.A3Q1M[src]')
                        item_image_url = await page.evaluate('(element) => element.src', u) 
                        
                        try:
                            u = await product.querySelector('a._2lsU7[href]')
                            store_url = await page.evaluate('(element) => element.href', u) 
                        except:
                            store_url = ''

                        try:
                            u = await product.querySelector('a._2lsU7')
                            seller = await page.evaluate('(element) => element.textContent', u) 
                        except:
                            seller = ''

                        # Seller contact not available on this site
                        contact_seller = ''

                        # Location not available on this site (only protected with slider)
                        location = ''

                        data = {
                            'contact_seller': contact_seller,
                            'item_image_title': item_image_title,
                            'item_image_url': item_image_url,
                            'item_url': item_url,
                            'location': location,
                            'seller': seller,
                            'shop': shop,
                            'site': url,
                            'status': True,
                            'store_url': store_url,
                            'note': ''
                        }
                    
                        db.collection('illegalmerchandise').document().set(data)  # Add a new doc in collection links with ID shop
                        counter += 1
                        logging.info(f"Added a product")                   
                        
            info = f"Added {counter} products to the database for url {url}"
            logging.info(info)
            await browser.close()

        except Exception as e:
            logging.info(f"Unexpected error: {str(e)}")

    return "All Done"

# def cleanurl(url):
#     base = 'https://aliexpress.com'
    
#     # Remove part after question mark
#     matches = re.findall('(.+\?)([^#]*)(.*)', url)

#     if len(matches) == 0:
#         newurl = base + url
#     else:
#         newurl = base + matches[0][0][:-1] # We take all but the last character (the ?) from the first item in the tuple that is the first item of the matches list
    
#     return newurl

# asyncio.get_event_loop().run_until_complete(main('request')) # only local

#  main('request') # only local