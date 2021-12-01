import logging
import firebase_admin
from firebase_admin import credentials, firestore
import re
import google.cloud.logging

from config import PROJECT # only cloud


# initialize firebase sdk
CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(CREDENTIALS, {
    'projectId': PROJECT,
})

# get firestore client
db = firestore.client()

# get logging client
client = google.cloud.logging.Client()
client.setup_logging()


def main(event, context):
    # Get newly added items
    new_items = db.collection(u'illegalmerchandise').where(u'status', u'==', False).stream()
    added, deleted = 0, 0
    
    for item in new_items:
        item_url = item.to_dict()['item_url']
        item_image_title = item.to_dict()['item_image_title']

        # Duplicate check
        docsurl = db.collection(u'illegalmerchandise').where(u'item_url', u'==', item_url).stream()
        docsname = db.collection(u'illegalmerchandise').where(u'item_image_title', u'==', item_image_title).stream()

        if (len(list(docsurl))) or (len(list(docsname))):
            duplicate = True
        else:
            duplicate = False
            
        # Check if keywords exists in Product title
        searchkeywords_ref = db.collection(u'searchquerykeywords')    
        keywords = []   

        for doc in searchkeywords_ref.where(u'active', u'==', True).stream():
            keywords.append(u'{}'.format(doc.to_dict()['querykeywords']))

        if any(x in item_image_title for x in keywords):
            keywords = True
        else:
            keywords = False

        # Check if vintage
        if re.search('vintage', item_image_title, re.IGNORECASE):
            vintage = True
        else:
            vintage = False

        # Delete record or set to active
        if duplicate == False and keywords == True and vintage == False:
            item.update({u'status': True})
            added += 1
        else:
            db.collection(u'illegalmerchandise').document(item.id).delete()
            deleted += 1
    
    logging.info(f"Added {added} items \nDeleted {deleted} items")
    return f"Success"


# main('request') # only local

