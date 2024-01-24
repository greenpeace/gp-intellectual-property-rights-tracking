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
    PROJECT = 'techlab-coding-team' # only local
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
        url = 'https://www.redbubble.com/shop/?query=' + query

        counter = 0
        try:
            page = requests.get(url, headers=headers)

            # Get web page
            soup = BeautifulSoup(page.content, "html.parser")

            # Regular Expression for a css class that ha dynamic values
            regex = re.compile('styles__link--3QJ5N')
            products = soup.find_all("a", class_=regex)

            # Get All links in the css class defined by regex
            for product in products:
                
                item_url = product['href']

                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                if not (len(list(docsurl))):

                    regeximg = re.compile('styles__image--G1zaZ styles__productImage--3ZNPD*')
                    item_image = product.find('img',  class_=regeximg)
                    item_image_title = item_image['alt']

                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')   

                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):

                        try:
                            item_image_url = item_image['src']
                        except:
                            item_image_url = ''

                        # Get data from item page
                        subpage = requests.get(item_url, headers=headers)
                        item_soup = BeautifulSoup(subpage.text, "html.parser")
                        sellerdetail = item_soup.find("a", class_="ProductConfiguration__artistLink--wueCo")    

                        try:
                            store_url = sellerdetail['href']
                        except:
                            store_url = ''

                        try:
                            seller = sellerdetail.text
                        except:
                            seller = ''

                        # Get data from store page
                        storepage = requests.get(store_url, headers=headers)
                        store_soup = BeautifulSoup(storepage.text, "html.parser")
                        regex = re.compile('styles__box--2Ufmy*')
                        storedetail = store_soup.find("li", class_=regex) 

                        try:
                            location = storedetail.text
                        except:
                            location = ''

                        shop = 'redbubble' 
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
                        continue
            
            logging.info(f"We added {counter} links for search term {query}")
            total += counter
        
        except Exception as e:
            logging.info(f"Error Getting main product page: {e}")
   
    return f"All Done, we added {total} links"

# call function, only needed locally
try:
    from config import PROJECT # only cloud
except:
    main('request')
