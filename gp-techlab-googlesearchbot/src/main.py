import logging
from urllib.parse import urlparse
from bs4 import BeautifulSoup as soup
from datetime import datetime
import pytz
import re
import requests
import urllib.request
import socket
import tldextract
import json

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

    results = 100 # valid options 10, 20, 30, 40, 50, and 100

    # Variables used
    ip = ''
    country = ''
    geolat = ''
    geolong = ''
    title = ''
    description = '' 

    # Get available proxies
    #cworking_proxies = check_proxies()

    searchquery_ref = db.collection(u'searchquery')
#    for prox in list(working_proxies):
    
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        query = u'{}'.format(doc.to_dict()['queryterm'])
        print(query)
        url = 'https://google.com/search?hl=en&q=' + query + '&source=lnms&sa=X' + '&num={}'.format(results)
    
        while url:
            print(url)

            page = requests.get(url, headers=headers)
            if page.status_code == 429:
                logging.info('Exceeded Rate Limit: {}')

            searchsoup = soup(page.text, "html.parser")
            # searchsoup = soup(page.text, "html5lib")

            mydivs = searchsoup.find_all("div", class_="g") # for debugging purpose
            # print(searchsoup.get_text()) # for debugging purpose   
    
            for link in searchsoup.find_all("a"):
                # get link details
                link_href = link.get('href')
                #Find the Title and Description

                if "url?q=" in link_href and not "webcache" in link_href:
                    # Try if Link is Active
                    try:
                        response = requests.get(link.get('href').split("?q=")[1].split("&sa=U")[0], timeout = 5)
                        active = True
                        logging.info("Link is active")
                    except:
                        active = False
                        logging.info("Link is inactive")

                    title = link.text
                    title = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', title, flags=re.MULTILINE)
                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                                
                    if any(x in title for x in keywords):

                        # Duplicate check
                        docsurl = db.collection(u'searchlinks').where(u'url', u'==', link.get('href').split("?q=")[1].split("&sa=U")[0]).stream()
                        if (len(list(docsurl))):
                            logging.info("URL Exist, we will ignore")
                        else:
                            logging.info("URL Not found, we will add to databse")
                                
                            # Create a query against the collection
                            urllink = urlparse(link.get('href').split("?q=")[1].split("&sa=U")[0]).netloc
                            
                            # Find out what Country the IP address is from
                            hostname = socket.gethostname()
                            try:
                                ip = socket.gethostbyname(urllink)
                                try:
                                    with urllib.request.urlopen("https://geolocation-db.com/jsonp/" + ip) as geourl:
                                        geodata = geourl.read().decode()
                                        geodata = geodata.split("(")[1].strip(")")
                                        #print(geodata)
                                        geodata = json.loads(geodata)
                                        country = geodata["country_name"]
                                        geolat = geodata["latitude"]
                                        geolong = geodata["longitude"]
                                except:
                                    logging.info("Problem getting Country Details")
                            except socket.error:
                                logging.info("Socket Error IP could not be obtained")

                            # remove www/http or https from url
                            # Get the Shop name
                            shopurl = tldextract.extract(urllink)
                            shop = shopurl.domain

                            data = {
                                'title': title,
                                'description': description,
                                'shop': shop,
                                'date': _now(), # datetime object containing current date and time
                                'url': link.get('href').split("?q=")[1].split("&sa=U")[0],
                                'country': country,
                                'category': 'Google Search',
                                'search': query,
                                'ip_address': ip,
                                'status': active,
                                'lat': geolat,
                                'long': geolong
                            }
                            db.collection('searchlinks').document().set(data)  # Add a new doc in collection links with ID shop
                    else:
                        logging.info("No match on Keywords")    # -> <match object>
            # get next page url
            url = searchsoup.find('a', id='pnnext')
            if url:
                url = 'https://www.google.com/' + url['href'] + '&source=lnms&sa=X'
            else:
                logging.info('Search Completed: {}')
    #return "All Done"

    # Send a message
   # _sendmessage()
def _now():
    return datetime.utcnow().replace(tzinfo=pytz.utc).strftime('%Y-%m-%d %H:%M:%S %Z')

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

googlecloudbot_http('request')