import logging
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import threading

# import asyncio # only local
PROJECT = 'torbjorn-zetterlund' # only local
logging.basicConfig(filename='test.log', level=logging.INFO) # only local

# from config import PROJECT # only cloud
# PROJECT = 'torbjorn-zetterlund' # only local


# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

def request_task(url, payload):
    requests.post(url, params=payload)

def fire_and_forget(url, payload):
    threading.Thread(target=request_task, args=(url, payload)).start()

def main(request):
    
    # Database Details
    searchquery_ref = db.collection(u'searchquery')

    # Read from Database the aliexpress url that are active
    for doc in searchquery_ref.where(u'active', u'==', True).stream():
        term = u'{}'.format(doc.to_dict()['queryterm'])
        term = term.replace(" ", "+")
        bot = "alibot"
        cf_url = "https://us-central1-torbjorn-zetterlund.cloudfunctions.net/" + bot
        payload = {'term': term}
        
        fire_and_forget(cf_url, payload=payload)

    return "All Done"


main('request') # only local

