import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime
import pytz
import requests
import urllib.request
import socket
import json

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

def bingbot_http(request):

    # Fake Real Browser
    headers = { 'User-agent' : 'Mozilla/11.0' }

    payload = { 'q' : 'sport', 'first' : '11' }

    searchquery_ref = db.collection(u'searchquery')
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        query = urllib.parse.quote_plus(query)
        print(query)

        payload = { 'q' : query, 'first' : '11' }
        url = 'https://www.bing.com/search?'
    
        while url:
            print(url)
            page = requests.get(url, payload, headers=headers)
            
            if page.status_code == 429:
                logging.info('Exceeded Rate Limit: {}')
            soup = BeautifulSoup(page.text, 'html.parser')

            urls4 = soup.find_all('li', { "class" : "b_algo" })
            print(urls4)
            
            for link in soup.findAll('li', { "class" : "b_algo" }):
                link_href = link.get('href')

                results = soup.findAll('li', { "class" : "b_algo" })
                for result in results:
                    if not "/?FORM=Z9FD1" in link_href:
                        docsurl = db.collection(u'searchlinks').where(u'url', u'==', link.get('href').split("?q=")[1].split("&sa=U")[0]).stream()
                        if (len(list(docsurl))):
                            logging.info("URL Exist, we will ignore")
                        else:
                            logging.info("URL Not found, we will add to databse")
                            
                            # Create a query against the collection
                            urllink = urlparse(link.get('href').split("?q=")[1].split("&sa=U")[0]).netloc
                            
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

                            # parse the url to get the name of the shop/site
                            urllink = urllink.split('.')[1]

                            data = {
                                'title': 'title',
                                'description': 'description',
                                'shop': urllink,
                                'date': _now(), # datetime object containing current date and time
                                'url': link.get('href').split("?q=")[1].split("&sa=U")[0],
                                'country': country,
                                'category': 'e-commerce',
                                'search': query,
                                'ip_address': ip,
                                'status': True
                            }
                            db.collection('searchlinks').document().set(data)  # Add a new doc in collection links with ID shop

                    else:
                        logging.info('Search Completed: {}')            
            # get next page url
            url = soup.find('a', id='pnnext')
            if url:
                url = 'https://www.google.com/' + url['href'] + '&source=lnms&sa=X'
            else:
                logging.info('Search Completed: {}')
    return "All Done"
def _now():
    return datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')

bingbot_http('request')