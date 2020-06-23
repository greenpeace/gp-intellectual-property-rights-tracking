import logging
from datetime import datetime
import requests
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import pytz
import re
import os
from lxml import html

import firebase_admin
from firebase_admin import credentials, firestore

# Get the sites environment credentials
PROJECT_NAME = os.environ["PROJECT_NAME"]

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT_NAME,
})

# get firestore client
db = firestore.client()

# Keyword Check
keywords = []
def etsybot_http(link):

    # Fake Real Browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}

    results = 100 # valid options 10, 20, 30, 40, 50, and 100

    searchlink_ref = db.collection(u'searchlinks')
    
    for doc in searchlink_ref.where(u'shop', u'==', 'etsy').stream():
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
#        url = cleanurl(url)
        print(url)

        try:
            page = requests.get(url, headers=headers)

            # Get web page
            ebaysoup = BeautifulSoup(page.text, "html5lib")

            regex = re.compile('block-grid-item *')
            # Get All links in the css class defined by regex
            for divs in ebaysoup.find_all("li", class_=regex):
               
                find_a = divs.find('a')
                item_url = find_a['href']
                item_url = cleanurl(item_url)
                item_image_title = find_a['title']
            
                # Check if Keywords Exixst in Product title
                searchkeywords_ref = db.collection(u'searchquerykeywords')        
                # Request data from Firestore
                for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                    keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))

                # Check if Keywords Exixst in Product title
                if any(x in item_image_title for x in keywords):
                    # Duplicate check
                    docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                    if (len(list(docsurl))):
                        logging.info("URL Exist, we will ignore")
                    else:
                        logging.info("URL Not found, we will add to databse")


                        item_image_url = divs.find('img')
                        try:
                            item_image_url = item_image_url['data-src']
                        except:
                            item_image_url = item_image_url['src']

                        # Get data from sub page
                        subpage = requests.get(item_url, headers=headers)

                        ebayitemsoup = BeautifulSoup(subpage.text, "html5lib")

                        regex = re.compile('wt-display-inline-flex-* *')
                        # Get All links in the css class defined by regex
                        for subdivs in ebayitemsoup.find_all("div", class_=regex):

                            sellerdetail = subdivs.find("a")    
                            #  for link in ebaysoup.find_all("a"):
                            try:
                                store_url = sellerdetail['href']
                            except:
                                store_url = ''

                            #  for link in ebaysoup.find_all("a"):
                            try:
                                seller = sellerdetail.span.text
                            except:
                                seller = ''

                            # Strip White Space
                            re.sub('\s+',' ',seller)

                            # Get data from shop page
                            try:
                                contact_seller = subdivs.find('div', class_='si-pd-a').a['href']
                            except:
                                contact_seller = ''

                            # Get data from shop page
                            shop = 'Etsy'
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

etsybot_http('request')