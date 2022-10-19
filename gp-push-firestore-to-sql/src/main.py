import logging
from typing import Any, List, Dict, Union

import firebase_admin
from firebase_admin import credentials, firestore

# configure local or cloud
from google.cloud.firestore_v1 import Client, DocumentSnapshot

try:
    from config import PROJECT  # only cloud
except:
    PROJECT = "techlab-coding-team"  # only local
    logging.basicConfig(filename="test.log", level=logging.INFO)

CREDENTIALS = credentials.ApplicationDefault()
firebase_admin.initialize_app(
    CREDENTIALS,
    {
        "projectId": "techlab-coding-team",
    },
)

# get firestore client
db = firestore.client()


def get_all_firestore_documents(
    db: Client, collection_name: str = "searchlinks"
) -> List[DocumentSnapshot]:
    return db.collection(collection_name).get()


def check_db_duplicates():
    pass


def db_writer():
    pass


def main(request) -> str:
    firestore_contents: List[DocumentSnapshot] = get_all_firestore_documents(db)
    fire_store_contents_data: List[Dict[str, Union[str, bool]]] = [
        document._data for document in firestore_contents
    ]
    return f"Finished writing {len(firestore_contents)} documents to DB."
