# Intellectual Property Rigths Tracking Bot

The Intellectual Property Rigths Tracking Bot is triggered by Cloud schedule, and will read the Firestore to get the search terms, search through the Google Serach Engine to find links based on the search term.

# The solution 
The bot will read a Firestore database to find the links to be used for scraping a webpage. The bots work as follows:
- Cloud Scheduler triggers all different e-commerce bots (Ali, Etsy, etc)
- The e-commerce bot loops over the search terms and searches on this specific e-commerce website. It places all results in the database, with Status = False
- Then the e-commerce bot sends a message to PubSub saying that it added new items to the databases
- Then the Selector bot wakes up, and check for all newly added items whether they fulfill our criteria: no duplicates, no vintage, keywords present in title
- The Selector bot deletes the non-relevant links from the database and sets the Status of the relevant links to True

# Creating the Cloud Function
Go to the Cloud Functions page of the Google Cloud Platform Console. Create a new function and give it a name that is meaningful.

# How to deply
Read the individual README.md file in the sub directory

# Technical Documentation
You can read 

The technical documentaiton - https://docs.google.com/document/d/1fSuS0o8UUY_VuMa1361BmhIbubQh1EWPtyVWK3-v4gI/edit?usp=sharing

User Manual - https://docs.google.com/document/d/1We8rM7G9D1rLSnaZh5aykOUoYivDtRC1h_ZPdJ7RNok/edit?usp=sharing

# Code Explanation in Colab Notebook

https://colab.research.google.com/drive/1yDw8WsXj7E2x5Gn2880jLT871WjF3KDj?usp=sharing

A Jupyter Notebook is provided for educational purposes.

# Checking Projects
gcloud config configurations list

gcloud config configurations activate [NAME]

On command line set the Google variable GOOGLE_APPLICATION_CREDENTIALS by entering 

    export GOOGLE_APPLICATION_CREDENTIALS="/Users/tzetterl/Documents/<service account>.json"

To check that it is set

    echo $GOOGLE_APPLICATION_CREDENTIALS


