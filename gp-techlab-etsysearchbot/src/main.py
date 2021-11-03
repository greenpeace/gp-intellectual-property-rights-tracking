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
        url = 'https://www.etsy.com/ca/market/' + query

        counter = 0
        try:
            page = requests.get(url, headers=headers)

            # Get web page
            soup = BeautifulSoup(page.content, "html.parser")
            regex = re.compile('listing-link*')

            products = soup.find_all("a", class_= regex)

            # Get all links in the css class defined by regex
            for product in products:
               
                item_url = product['href']
                item_img = product.find("img")
                item_image_title = item_img['alt']
            
                # Check if Keywords Exixst in Product title
                searchkeywords_ref = db.collection(u'searchquerykeywords')        
                # Request data from Firestore
                for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                    keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))

                # Check if Keywords Exist in Product title
                if any(x in item_image_title for x in keywords):
                    
                    # Duplicate check
                    docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                    
                    if not (len(list(docsurl))):

                        try:
                            item_image_url = item_img['data-src']
                        except:
                            item_image_url = item_img['src']

                        # Get data on the seller from item page
                        subpage = requests.get(item_url, headers=headers)

                        itemsoup = BeautifulSoup(subpage.text, "html.parser")
                        
                        sellerinfo = itemsoup.find("p", class_='wt-text-body-01 wt-mr-xs-1')
                        sellerinfo = sellerinfo.find("a", class_='wt-text-link-no-underline')    
                       
                        try:
                            store_url = sellerinfo['href']
                        except:
                            store_url = ''
                        
                        # Get data on the seller from seller page 
                        sellerpage = requests.get(store_url, headers=headers)
                        sellersoup = BeautifulSoup(sellerpage.text, "html.parser")
                        sellerdetail = sellersoup.find("div", class_='shop-name-and-title-container wt-mb-xs-1')  
                        sellerdetail = sellerdetail.find("h1")  
                        
                        try:
                            seller = sellerdetail.text
                        except:
                            seller = ''

                        sellerdetail = sellersoup.find("div", class_='wt-display-flex-xs wt-text-truncate wt-align-items-center')
                        sellerdetail = sellerdetail.find("span")

                        # Get data from shop page
                        try:
                            location = sellerdetail.text
                        except:
                            location = ''

                        # Get data from shop page
                        shop = 'etsy'
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
                        logging.info(f"We added {counter} links for search term {query}")
                else:
                    logging.info(f"No match on Keywords for title {item_image_title}") 
            total += counter
        except:
            logging.info("Error Getting main product page")
   
    return f"All Done, we added {total} links"


# call function, only needed locally
try:
    from config import PROJECT # only cloud
except:
    main('request')
