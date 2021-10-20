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

# Keyword Array filled in by daya in Firestore
keywords = []

def main(request):

    # Fake Real Browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}

    searchquery_ref = db.collection(u'searchquery')
    
    total = 0
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = urllib.parse.quote_plus(query)

        # start at the first search tab
        url = 'https://www.spreadshirt.com/shop/' + query

        counter = 0
        try:
            page = requests.get(url, headers=headers)

            # Get web page
            soup = BeautifulSoup(page.content, "html.parser")

            products = soup.find_all('a', class_='article thumb-font article--label')

            # Get All links in the css class defined by regex
            for product in products: 
                item_url = convert(product['href'])

                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                if not (len(list(docsurl))):

                    item_image = product.find('img')
                    item_image_title = item_image['alt']

                    # Check if Keywords Exist in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):
                                               
                        item_image_url = item_image['src']

                        # Rest of the data is behind dynamic JavaScript:(
       
                        seller = ''
                        store_url = ''
                        location = ''
                        shop = 'spreadshirt'
                        contact_seller = ''

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
                        logging.info(f"No match on Keywords for {item_image_title}")    # -> <match object>
            
            total += counter 
            logging.info(f"We added {counter} links for search term {query}")   
        except Exception as e:
            logging.info(f"Error Getting main product page: {e}")
   
    return f"All Done, we added {total} links"

def cleanurl(url):
    matches = re.findall('(.+\?)([^#]*)(.*)', url)
    if len(matches) == 0:
        return url
    match = matches[0]
    query = match[1]
    return match[0]

def convert(url):
    if url.startswith('http://www.'):
        return 'http://' + url[len('http://www.'):]
    if url.startswith('//www.'):
        return 'https://www' + url[len('//www'):]
    if url.startswith('//image.'):
        return 'https://' + url[len('//'):]
    if url.startswith('www.'):
        return 'https://' + url[len('www.'):]
    if not url.startswith('http://'):
        return 'http://' + url
    return url

# call function, only needed locally
try:
    from config import PROJECT # only cloud
except:
    main('request')
