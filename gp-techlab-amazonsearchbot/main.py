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

# Keyword Array filled in by daya in Firestore
keywords = []

# Set Default
baseurl = ''

def amazonbot_http(request):

    searchlink_ref = db.collection(u'searchlinks')
    
    for doc in searchlink_ref.where(u'shop', u'==', 'amazon').stream():
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        print(url)
        baseurl = urlparse(url).netloc

        try:

            session = requests.Session()

            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}
            page = session.get(url, headers=headers)
            page.raise_for_status()  # omit this if you dont want an exception on a non-200 response

            # Get web page
            amazonsoup = BeautifulSoup(page.content, "html5lib")
            # For debug purpose
            #print(amazonsoup.prettify())
            regex = re.compile('sg-col-4-of-24 sg-col-4-of-12 sg-col-4-of-36 s-result-item *')
            # Get All links in the css class defined by regex
            for divs in amazonsoup.find_all('div', class_=regex):

                item_url_data = divs.find('a')
                item_url = item_url_data['href']
                #item_url = cleanurl(item_url)
                item_url = convert(item_url, baseurl)

                item_image_url = item_url_data.img['src']

                item_image_data = divs.find('h2')                    
                item_image_title = item_image_data.span.text

                # Check if Keywords Exixst in Product title
                searchkeywords_ref = db.collection(u'searchquerykeywords')        
                # Request data from Firestore
                for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                    keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                if any(x in item_image_title for x in keywords):
                    # Duplicate check
                    docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                    if (len(list(docsurl))):
                        logging.info("URL Exist, we will ignore")
                    else:
                        logging.info("URL Not found, we will add to databse")

                        # Get data from sub page
                        subpage = requests.get(item_url, headers=headers)

                        ebayitemsoup = BeautifulSoup(subpage.text, "html5lib")

                        for subdivs in ebayitemsoup.find_all(id="titleBlock"):

                            sellerdetail = subdivs.find("a")    
                            #  for link in ebaysoup.find_all("a"):
                            try:
                                store_url = sellerdetail['href']
                                baseurl = urlparse(url).netloc
                                store_url = convert(store_url, baseurl)
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

                            # Get data from shop page
                            shop = 'Amazon'
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
    matches = re.findall('(.+\?)([^#]*)(.*)', url)
    if len(matches) == 0:
        return url
    match = matches[0]
    query = match[1]
    return match[0]

def convert(url, baseurl):
    if url.startswith('http://www.'):
        return 'http://' + url[len('http://www.'):]
    if url.startswith('/'):
        return 'https://' + baseurl + url
    if url.startswith('//www.'):
        return 'https://www' + baseurl + url
    if url.startswith('//image.'):
        return 'https://' + url[len('//'):]
    if url.startswith('www.'):
        return 'https://' + url[len('www.'):]
    if not url.startswith('http://'):
        return 'http://' + url
    return url

amazonbot_http('request')