# Cafepress Bot

The Cafepress Bot is triggered by Cloud schedule, and will read the Firestore to get the search terms, search through the Google Serach Engine to find links based on the search term.

# The solution in few words
The bot will read a Firestore database to find the links to be used for scraping a webpage.


# Creating the Cloud Function
Go to the Cloud Functions page of the Google Cloud Platform Console. Create a new function and give it a name that is meaningful.

# Deploy
gcloud functions deploy <cloud function name> --runtime python37 --set-env-vars PROJECT_NAME=<gcp_project_name> --trigger-http --allow-unauthenticated --region=europe-west1 --memory=128MB

# You may have to alter the IAM if you can not gett the function to work
gcloud functions add-iam-policy-binding <function name> --region=<region> --member=allUsers --role=roles/cloudfunctions.invoker