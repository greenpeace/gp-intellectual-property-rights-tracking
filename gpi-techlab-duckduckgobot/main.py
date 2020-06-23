import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import re
import requests
import urllib.request
import socket
import tldextract
import json
import os

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

def duckduckgo_http(request):

    # Fake Real Browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}

    results = 100 # valid options 10, 20, 30, 40, 50, and 100

    # Variables used
    ip = ''
    country = ''
    geolat = ''
    geolong = ''
    title = ''
    description = '' 

    searchquery_ref = db.collection(u'searchquery')
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = urllib.parse.quote_plus(query)
        print(query)

        url = 'https://duckduckgo.com/html/?q=' + query + '&ia=web'

#            page = requests.get(url, headers = {'User-agent': 'my bot 0.1'})
        page = requests.get(url, headers=headers)
        if page.status_code == 429:
            logging.info('Exceeded Rate Limit: {}')

        duckducksoup = BeautifulSoup(page.content, "html5lib")
        # Debug Message
        # print(duckducksoup.prettify())

        for link in duckducksoup.findAll("a", class_="result__snippet"):
            link_href = link['href']
            # Parse URL
            #link_href = urllib.parse.unquote(link_href)
            # convert the url
            urllink = convert(urllib.parse.unquote(link_href))

            title = link.text
            title = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', title, flags=re.MULTILINE)

            # Check if Keywords Exixst in Product title
            searchkeywords_ref = db.collection(u'searchquerykeywords')        
            # Request data from Firestore
            for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))                        
            if any(x in title for x in keywords):

                # check for duplicates
                docsurl = db.collection(u'searchlinks').where(u'url', u'==', urllink).stream()
                if (len(list(docsurl))):
                    logging.info("URL Exist, we will ignore")
                else:
                    logging.info("URL Not found, we will add to databse")

                    # parse the url to get the name of the shop/site
                    # Get the Shop name
                    shopurl = tldextract.extract(urllink)
                    shop = shopurl.domain

                    # Find out what Country the IP address is from
                    hostname = socket.gethostname()
                    # get the hostname
                    urlname = urlparse(urllink).netloc

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

                    data = {
                        'title': title,
                        'description': 'description',
                        'shop': shop,
                        'date': _now(), # datetime object containing current date and time
                        'url': urllink,
                        'country': country,
                        'category': 'e-commerce',
                        'search': query,
                        'ip_address': ip,
                        'status': True
                    }
                    db.collection('searchlinks').document().set(data)  # Add a new doc in collection links with ID shop
            else:
                logging.info("No match on Keywords")    # -> <match object>
#   return "All Done"
        # get next page url
        url = duckducksoup.find('div', class_='nav-link')
        if url:
            url = 'https://duckduckgo.com/html/?q=' + query + '&ia=web'
        else:
            logging.info('DuckDuckGo  Search Completed: {}')

def _now():
    return datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')

# Convert URL correctly
def convert(converturl):
    converturl = urllib.parse.unquote(converturl)
    if converturl.startswith('http://www.'):
        return 'http://' + converturl[len('http://www.'):]
    if converturl.startswith('/l/?kh=-1&uddg='):
        return 'https://' + converturl[len('/l/?kh=-1&uddg=https://'):]
    if converturl.startswith('//www.'):
        return 'https://www' + converturl[len('//www'):]
    if converturl.startswith('//image.'):
        return 'https://' + converturl[len('//'):]
    if converturl.startswith('www.'):
        return 'https://' + converturl[len('www.'):]
    if not converturl.startswith('http://'):
        return 'http://' + converturl
    return converturl

duckduckgo_http('request')