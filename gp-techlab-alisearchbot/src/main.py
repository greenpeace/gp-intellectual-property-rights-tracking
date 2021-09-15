import logging
import re
from requests_html import HTMLSession 
import firebase_admin
from firebase_admin import credentials, firestore

from config import PROJECT # only cloud
# PROJECT = 'torbjorn-zetterlund' # only local


# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

def main(request):
    
    # Database Details
    searchlink_ref = db.collection(u'searchlinks')

    # Empty list to store keywords in
    keywords = [] 

    # Read from Database the aliexpress url that are active
    for doc in searchlink_ref.where(u'status', u'==', True).where(u'shop', u'==', 'aliexpress').stream():    
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        counter = 0

        try:
            # Start a session
            session = HTMLSession()

            # Get the webpage
            r = session.get(url)
            r.html.render(sleep = 1, keep_page=True, scrolldown=10) # Set scroll down 10 to catch all products
            divs = r.html

            # Get products
            products = divs.find('._1OUGS')

            for product in products:
                # Grab item url
                item_attrs = product.find('a._9tla3')[0].attrs         
                item_url = item_attrs['href'] 
                item_url = cleanurl(item_url)
                
                # Grab image title
                image_attrs = product.find('img.A3Q1M')[0].attrs # Retrieve image div
                item_image_title = image_attrs['alt']

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
                        item_image_url = image_attrs['src']
                        
                        sellerdetail = product.find("a._2lsU7")[0]    

                        try:
                            store_url = sellerdetail.attrs['href']
                        except:
                            store_url = ''

                        try:
                            seller = sellerdetail.text
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
                        
            info = f"Added {counter} products to the database for url {url}"
            logging.info(info)
            session.close()

        except:
            logging.info(f"Error getting main product page, response was {r.status_code}")
   
    return "All Done"

def cleanurl(url):
    base = 'https://aliexpress.com'
    
    # Remove part after question mark
    matches = re.findall('(.+\?)([^#]*)(.*)', url)

    if len(matches) == 0:
        newurl = base + url
    else:
        newurl = base + matches[0][0][:-1] # We take all but the last character (the ?) from the first item in the tuple that is the first item of the matches list
    
    return newurl

# main('request') # only local