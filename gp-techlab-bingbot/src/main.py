import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import requests
import urllib.request
import socket
import json

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

def main(request):

    # Fake Real Browser
    headers = { 'User-agent' : 'Mozilla/11.0' }

    payload = { 'q' : 'sport', 'first' : '11' }

    searchquery_ref = db.collection(u'searchquery')
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = urllib.parse.quote_plus(query)

        # start at the first search tab
        payload = { 'q' : query, 'first' : '11' }
        url = 'https://www.bing.com/search?'

        page_nr = 0 # a counter for page number
        total = 0 # a counter for total links found per search term

        while url:
            counter = 0 # a counter for links per page

            page = requests.get(url, payload, headers=headers)

            if page.status_code == 429:
                logging.info('Exceeded Rate Limit: {}')

            soup = BeautifulSoup(page.text, 'html.parser')

            for item in soup.findAll('li', { "class" : "b_algo" }):
                link_href = item.find('cite').get_text()

                docsurl = db.collection(u'searchlinks').where(u'url', u'==', link_href).stream()
                
                if not (len(list(docsurl))): # only continue if url does not exist in database yet

                    # get the hostname
                    urlname = urlparse(link_href).netloc

                    try:
                        ip = socket.gethostbyname(urlname)
                        try:
                            with urllib.request.urlopen("https://geolocation-db.com/jsonp/" + ip) as geourl:
                                geodata = geourl.read().decode()
                                geodata = geodata.split("(")[1].strip(")")
                                #print(geodata)
                                geodata = json.loads(geodata)
                                country = geodata['country_code']
                                geolat = geodata['latitude']
                                geolong = geodata['longitude']
                        except:
                            country = "Not Found"
                    except socket.error:
                        ip = 'Not Found'
                        country = 'Not Found'

                    # parse the url to get the name of the shop/site
                    shop = strip_url(link_href)

                    data = {
                        'title': 'title',
                        'description': 'description',
                        'shop': shop,
                        'date': _now(), # datetime object containing current date and time
                        'url': link_href,
                        'country': country,
                        'category': 'Bing Search',
                        'search': query,
                        'ip_address': ip,
                        'status': True
                    }
                    db.collection('searchlinks').document().set(data)  # Add a new doc in collection links with ID shop 
                    counter += 1 
            
            logging.info(f"Added {counter} links for page {page_nr} of search term {query}")
            
            total += counter
            page_nr += 1
           
            # get next page url
            result = soup.find('a', { "class" : "sb_pagN sb_pagN_bp b_widePag sb_bp" })
            try:
                url = result['href']
                url = "https://www.bing.com" + url
                payload = None

            except:
                logging.info(f'Search completed at page {page_nr-1}, added {total} links in total')
                
            if page_nr == 5:  # quit if 5 pages were searched        
                break
    return f"All Done, we added {total} links"

def _now():
    return datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')

def strip_url(link):
    if "https://www" in link:
        shop = link.split('.')[1]
    elif "https://" in link:
        shop = link.split('.')[0]
        shop = shop.split('//')[1]
    else:
        shop = link.split('.')[1]
    return shop




# call function, only needed locally
try:
    from config import PROJECT # only cloud
except:
    main('request')