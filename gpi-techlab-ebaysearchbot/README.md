# Aliexpress Bot

The Google Search Bot is triggered by Cloud schedule, and will read the Firestore to get the search terms, search through the Google Serach Engine to find links based on the search term.

# The solution in few words

# Cloud Function
The Cloud Function implementation will 

# Google Cloud APIs Python client libraries
While you can use Google Cloud APIs by making direct HTTP requests (or RPC calls where available), Google provide client library for all its Cloud APIs. This makes it easier to access them from your favorite languages. But there is a subtlety : there are different types of client libraries provided and here are the 2 that we will use :

# Why Cloud Firestore
Cloud Firestore has a start free then pay as you go pricing model and its free tier is very generous
No other Google Cloud storage solution for random access apart from Cloud Datastore has the pay as you go pricing model.
It’s very easy to browse Cloud Firestore data through Google Cloud Console


# Creating the Cloud Function
Go to the Cloud Functions page of the Google Cloud Platform Console. Create a new function and give it a name that is meaningful.

# Proper authorization for the Cloud Function
At runtime, our Cloud Functions uses a service account. It is listed at the bottom of our Cloud Function details page.


# Cost

# Debug
If you debug locally you may have to install Beatifulsoup and the parser html5lib

you can check your libraries installed with 

$ pip list

$ pip install beautifulsoup4

$ pip install html5lib

If you use vs code, install the standard Python debug script.

# Deploy
gcloud functions deploy _ebaybot_http --runtime python37 --trigger-http --allow-unauthenticated --region=europe-west1 --memory=128MB


--set-env-vars COLLECTION_NAME_PREFIX=budget-notifs  --trigger-topic=budgets-notifications

# gcloud commands
Get Project List 

$ gcloud projects list

Login to account
$ gcloud auth login

Get Project
$ gcloud config get-value project

List the config
$ gcloud config list

List all properties active project
$ gcloud config list --all

List Config
$ gcloud config configurations list

Activate a config 
$ gcloud config configurations activate

Create a config
$ gcloud config configurations create techlab

Set Values - https://cloud.google.com/sdk/gcloud/reference/config/set
$ 

# To run add
gcloud functions add-iam-policy-binding <function name> --region=<region> --member=allUsers --role=roles/cloudfunctions.invoker

# Reading

https://www.crummy.com/software/BeautifulSoup/bs4/doc/#installing-a-parser
https://firebase.google.com/docs/firestore/query-data/queries
https://medium.com/better-programming/the-only-step-by-step-guide-youll-need-to-build-a-web-scraper-with-python-e79066bd895a