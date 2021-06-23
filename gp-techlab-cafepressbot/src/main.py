import logging
from datetime import datetime
import requests
import urllib.request
from urllib.parse import urlparse
from bs4 import BeautifulSoup, SoupStrainer
import pytz
import re
import os
import OpenSSL.crypto
from lxml import html

from config import PROJECT

import firebase_admin
from firebase_admin import credentials, firestore

# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

# Keyword Array filled in by daya in Firestore
keywords = []

# The url in cafepress product pages do not have the baseurl - setting it here 
baseurl = 'https://cafepress.com'

def main(request):

    # Fake Real Browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}

    searchlink_ref = db.collection(u'searchlinks')
    
    for doc in searchlink_ref.where(u'shop', u'==', 'cafepress').stream():
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        #        url = cleanurl(url)
        print(url)

        try:
            page = requests.get(url, headers=headers)

            # Get web page
            ebaysoup = BeautifulSoup(page.content, "html5lib")
            # Regular Expression for a css class that ha dynamic values
            regex = re.compile('listing-item flex-item ptn-*')
            # Get All links in the css class defined by regex
            for divs in ebaysoup.find_all("a", class_=regex):
                print(divs['href'])
                item_url = divs['href']
                item_url = cleanurl(item_url)
                print(divs)
                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                if (len(list(docsurl))):
                    logging.info("URL Exist, we will ignore")
                else:
                    logging.info("URL Not found, we will add to databse")

                    item_image_title = divs.find('img')
                    item_image_title = item_image_title['alt']

                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):
                        item_image_url = divs.find('img')
                        try:
                            item_image_url = item_image_url['data-src']
                        except:
                            item_image_url = item_image_url['src']

                        # Get data from sub page
                        subpage = requests.get(item_url, headers=headers)

                        ebayitemsoup = BeautifulSoup(subpage.text, "html5lib")

                        for subdivs in ebayitemsoup.find_all("div", class_="si-content"):

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

                            # Get data from shop page
                            try:
                                contact_seller = subdivs.find('div', class_='si-pd-a').a['href']
                            except:
                                contact_seller = ''

                            shop = 'Cafepress'
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
        return baseurl + url
    matches = re.findall('(.+\?)([^#]*)(.*)', url)
    if len(matches) == 0:
        return baseurl + url
    match = matches[0]
    query = match[1]
#    sanitized_query = '&'.join([p for p in query.split('&') if not p.startswith('?hash')])
#    return match[0]+sanitized_query+match[2]
    return baseurl + match[0]

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
