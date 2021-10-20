import logging
import requests
from bs4 import BeautifulSoup
import re
import urllib

import firebase_admin
from firebase_admin import credentials, firestore

# configure local or cloud
try:
    from config import PROJECT # only cloud
except:
    PROJECT = 'torbjorn-zetterlund' # only local
    logging.basicConfig(filename='test.log', level=logging.INFO) # log only local

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

keywords = [] 

def main(request):

    # Fake Real Browser
    headers = { 'User-agent' : 'Mozilla/11.0' }

    searchquery_ref = db.collection(u'searchquery')
    
    total = 0
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = urllib.parse.quote_plus(query)

        # start at the first search tab
        url = 'https://www.cafepress.com/+' + query

        counter = 0
        try:
            page = requests.get(url, headers=headers)

            # Get web page
            soup = BeautifulSoup(page.content, "html.parser")

            # Regular Expression for a css class that ha dynamic values
            regex = re.compile('listing-item flex-item ptn-*')
            
            # Get All links in the css class defined by regex
            products = soup.find_all("a", class_=regex)
            
            for product in products:
            
                item_url = product['href']
                item_url = "https://www.cafepress.com" + item_url
                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                
                if not (len(list(docsurl))):

                    item_image_title = product.find('img')
                    item_image_title = item_image_title['alt']

                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords') 

                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):
                        item_image_url = product.find('img')
                        try:
                            item_image_url = item_image_url['data-src']
                        except:
                            item_image_url = item_image_url['src']

                        # Fill in unavailable data
                        contact_seller = ''
                        store_url = ''
                        seller = ''
                        shop = 'cafepress'
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
                        
                    else:
                        continue
                    
            logging.info(f"We added {counter} links for search term {query}")
            total += counter
        except:
            logging.info("Error Getting main product page")
         
    return f"All Done, we added {total} links"

# call function, only needed locally
try:
    from config import PROJECT # only cloud
except:
    main('request')
