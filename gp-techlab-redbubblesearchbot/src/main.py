import logging
import requests
from bs4 import BeautifulSoup
import re

import firebase_admin
from firebase_admin import credentials, firestore

from config import PROJECT

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

    searchlink_ref = db.collection(u'searchlinks')
    
    for doc in searchlink_ref.where(u'shop', u'==', 'redbubble').stream():
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        #        url = cleanurl(url)
        print(url)

        try:
            page = requests.get(url, headers=headers)

            # Get web page
            redbubble = BeautifulSoup(page.content, "html5lib")
            # Regular Expression for a css class that ha dynamic values
            regex = re.compile('styles__link--2sYi3')
            # Get All links in the css class defined by regex
            for divs in redbubble.find_all("a", class_=regex):
                item_url = divs['href']
                item_url = cleanurl(item_url)
                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                if (len(list(docsurl))):
                    logging.info("URL Exist, we will ignore")
                else:
                    logging.info("URL Not found, we will add to databse")

                    regeximg = re.compile('styles__box--206r9 styles__ratioInner--KvIFM')
                    product_item = divs.find('div',  class_=regeximg)
                    item_image_title = product_item.img['alt']

                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):

                        try:
                            item_image_url = product_item.img['src']
                        except:
                            item_image_url = product_item.img['src']

                        # Get data from sub page
                        subpage = requests.get(item_url, headers=headers)

                        redbubblesoup = BeautifulSoup(subpage.text, "html5lib")

                        for subdivs in redbubblesoup.find_all("div", class_="DesktopProductPage__config--3xaTv"):

                            sellerdetail = subdivs.find("a")    
                            #  for link in ebaysoup.find_all("a"):
                            try:
                                store_url = sellerdetail['href']
                            except:
                                store_url = ''

                            #  for link in ebaysoup.find_all("a"):
                            try:
                                seller = sellerdetail.text
                            except:
                                seller = ''

                            # Get data from shop page
                            try:
                                contact_seller = ''
                            except:
                                contact_seller = ''

                            shop = 'Redbubble'
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
                    else:
                        logging.info("No match on Keywords")    # -> <match object>
        except:
            logging.info("Error Getting main product page")
   
    return "All Done"

def cleanurl(url):
    if "?hash" not in url:
        return url
    matches = re.findall('(.+\?)([^#]*)(.*)', url)
    if len(matches) == 0:
        return url
    match = matches[0]
    query = match[1]
    return match[0]
