import logging
import requests
from urllib.parse import urlparse
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

filename = "teepublic.html"
def main(request):

    # Fake Real Browser
#    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}
    # Set headers
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})# Set headers

    searchlink_ref = db.collection(u'searchlinks')
    
    for doc in searchlink_ref.where(u'shop', u'==', 'teepublic').stream():
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        print(url)
        baseurl = urlparse(url).netloc

        try:
            page = requests.get(url, headers=headers)
            # Get web page
            teepublic_data = BeautifulSoup(page.content, "html.parser")
            print(teepublic_data.prettify())
            html_data = teepublic_data.prettify()
            with open(filename, "a+") as file:
                file.write(html_data)
            # Regular Expression for a css class that ha dynamic values
            regex = re.compile('greenpeace')
            # Get All links in the css class defined by regex
            #title = amazonsoup.find(id="productTitle").get_text()
            #price = amazonsoup.find(id="priceblock_ourprice").get_text()
            for divs in teepublic_data.find_all('a').get('href'):
                item_url = divs.find('a')  
                item_url = item_url['href']
                item_url = convert(item_url, baseurl)
                # Duplicate check
                docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
                if (len(list(docsurl))):
                    logging.info("URL Exist, we will ignore")
                else:
                    logging.info("URL Not found, we will add to databse")

                    item_image_title = divs.find('h2', class_="m-tiles__title m-tiles__info")
                    item_image_title = item_image_title.a.text

                    # Check if Keywords Exixst in Product title
                    searchkeywords_ref = db.collection(u'searchquerykeywords')        
                    # Request data from Firestore
                    for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
                        keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))
                        
                    if any(x in item_image_title for x in keywords):
                        try:
                            item_image_url = divs.find('img')
                            item_image_url = item_image_url['src']
                        except:
                            item_image_url = item_image_url['src']

                        item_image_url = convert(item_image_url)
                        # Get data from sub page
                        subpage = requests.get(item_url, headers=headers)

                        spreadshirtsoup = BeautifulSoup(subpage.text, "html5lib")

                        for subdivs in spreadshirtsoup.find_all("div", class_="detail-header__designer-link"):

                            data = {
                                'contact_seller': contact_seller,
                                'item_image_title': item_image_title,
                                'item_image_url': item_image_url,
                                'item_url': item_url,
                                'location': location,
                                'seller': seller(subdivs),
                                'shop': 'Teepublic',
                                'site': url(),
                                'status': True,
                                'store_url': store_url(subdivs),
                                'note': ''
                            }
                            db.collection('illegalmerchandise').document().set(data)  # Add a new doc in collection links with ID shop
                    else:
                        logging.info("No match on Keywords")    # -> <match object>
        except:
            logging.info("Error Getting main product page")
   
    return "All Done"

def contact_seller(link):
    contact_seller = ''
    return contact_seller

def getTitle(link):
    """Attempt to get a title."""
    title = ''
    if link.title.string is not None:
        title = link.title.string
    elif link.find("h1") is not None:
        title = link.find("h1")
    return title

def item_image_title(): 
    item_image_title = ''
    return item_image_title

def item_image_url(): 
    item_image_url = ''
    return item_image_url

def item_url(): 
    item_url = ''
    return item_url

def location(): 
    location = ''
    return location

def seller(subdivs): 
    seller = ''
    sellerdetail = subdivs.find("a")    
    seller = sellerdetail.text
    return seller

def site(): 
    url = ''
    return url

def store_url(subdivs):
    store_url = ''
    
    sellerdetail = subdivs.find("a")    
    store_url = sellerdetail['href']
    store_url = convert(store_url)
    return store_url

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
