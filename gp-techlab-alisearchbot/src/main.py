import logging
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re
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

# Get the settings data
searchlink_ref = db.collection(u'settings')
# Read from Database the aliexpress url that are active
for doc in searchlink_ref.stream():
    aliexpressuserid = u'{}'.format(doc.to_dict()['aliexpressuserid'])
    aliexpresspassword = u'{}'.format(doc.to_dict()['aliexpresspassword'])

# Keyword Array filled in by daya in Firestore
keywords = []
# Debug Filename
#filename = "aliexpress.html"

def main(request):

    # Fake Real Browser
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1)'}
#   headers = requests.utils.default_headers()
#    headers.update({
#        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
#    })

    payload = {
        "loginId": aliexpressuserid, 
        "password": aliexpresspassword,
    }

    LOGIN_URL='https://login.aliexpress.com/?from=sm&return_url="+encodeURIComponent("https://www.aliexpress.com:443//w/wholesale-greenpeace%2520t%2520shirt.html/_____tmd_____/punish?x5secdata=5e0c8e1365474455070961b803bd560607b52cabf5960afff39b64ce58073f78a189947e9a397fdf240c55d920f623b02aeb9455a7e24af28ac2e97b74ad2a6176cfd69fc6855cfd606bf150111a78ac0480def1935cf7544236ad19f2057552a162a340699158048a0de1331e905e5a49d5db805b9215f9db44920987df88e4697d6d94e20741d1bf4b0faf27a4ced18fe364c98ed349eab9624e944cbdeddf53cbc44eb678a97533ab39d4512f9911518363df3084b8222e427500f5867a927cf926208454823246599c933e5598893b327e27af767b2c979c28d443c20fe7a45cd1d5904b1bb4682fc4a7583178c398171b3a2160f2cf84f0987a2b6115f0fbd23888ffe90d57c5f5517984b37bfadc93e71969a440df72b2d6771a63cf7b3aa2d89a5041c02775e6c780c7057afc1efeec2199cac5656669a307252132dcc8a5376d5eeb10e4b18bc286a166d1630ba2afb0aa610bf7ac271d0799152c50b1a6c671ad10550e185470c7625171c3753bba2b27d926f4ed3154636b8549b1cded84058d29410ed41039ac304616b4b6331059e8961c310fedf6d5911c9357c056fec688c643d58c9a1d5879badb8ded6630689fdcabf3777399702932b39e4945c9a16c66d06ebc00e45b4f20af38a6b1baf3f8f8cb142c2b0f35bd47fa637e35e29e895dd5559881ed86fa34fa7b&x5step=100'
    # Create a session Object
    session_requests = requests.session()
    # Extract the csrf token
    login_result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(login_result.text)
#    authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]
    # Login Phase
    login_result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))
    
    # Database Details
    searchlink_ref = db.collection(u'searchlinks')
    # Read from Database the aliexpress url that are active
    for doc in searchlink_ref.where(u'status', u'==', True).where(u'shop', u'==', 'aliexpress').stream():    
        url = u'{}'.format(doc.to_dict()['url'])
        shop = u'{}'.format(doc.to_dict()['shop'])
        print(url)
        baseurl = urlparse(url).netloc

        try:
            page = session_requests.get(url, data=payload,  headers = dict(referer = url))
            # Get web page
            aliexpresssoup = BeautifulSoup(page.text, "html5lib")
            # For debug purpose
#            print(aliexpresssoup.prettify())
            # create a new debug file
            html_data = aliexpresssoup.prettify()
            with open(filename, "w") as file:
                file.write(html_data)

            for listitems in aliexpresssoup.find_all(attrs={"ae_button_type": "cross link"}):
#            for listitems in aliexpresssoup.find_all('li', class_='list-item'):
            
                #item_url = listitems.find('a')
                item_url = item_url.href
                item_url = cleanurl(item_url)

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

                    # Check if Keywords Exixst in Product title
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

                            # Get data from shop page
                            try:
                                shop = subdivs.find('div', class_='si-cleanup').a['href']
                            except:
                                shop = ''

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
    else:
        logging.info("Friendly Shop", url)
   
    return "All Done"

def cleanurl(url):
    if "?hash" not in url:
        return url
    matches = re.findall('(.+\?)([^#]*)(.*)', url)
    if len(matches) == 0:
        return url
    match = matches[0]
    query = match[1]
#    sanitized_query = '&'.join([p for p in query.split('&') if not p.startswith('?hash')])
#    return match[0]+sanitized_query+match[2]
    return match[0]

#aliexpressbot_http('request')